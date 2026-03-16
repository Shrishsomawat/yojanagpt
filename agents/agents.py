"""
YojanaGPT - Agent Definitions
Four specialized agents that work together to help citizens find government schemes.
"""

import json
import re
import logging
from typing import Optional
from config.settings import prompts, Prompts
from utils.llm_client import llm_client
from knowledge_base.vector_store import vector_store
from data.schemes_database import get_scheme_by_id, get_all_schemes

logger = logging.getLogger(__name__)


def _get_language_instruction(language: str) -> str:
    """Get language-specific instruction for prompts."""
    return Prompts.LANGUAGE_INSTRUCTION.get(language, Prompts.LANGUAGE_INSTRUCTION["en"])


def _extract_json(text: str) -> Optional[dict]:
    """Extract JSON from LLM response (handles markdown code blocks)."""
    # Try to find JSON in code blocks
    patterns = [
        r'```json\s*([\s\S]*?)\s*```',
        r'```\s*([\s\S]*?)\s*```',
        r'\{[\s\S]*\}',
        r'\[[\s\S]*\]',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue
    
    # Try parsing the whole text
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


# ═══════════════════════════════════════════════════════════════════════
# AGENT 1: PROFILE BUILDER
# ═══════════════════════════════════════════════════════════════════════
class ProfileBuilderAgent:
    """Conversationally gathers citizen information to build a structured profile."""
    
    REQUIRED_FIELDS = [
        "name", "age", "gender", "state", "area_type", "category",
        "income", "occupation", "education_level"
    ]
    
    OPTIONAL_FIELDS = [
        "district", "marital_status", "dependents", "land_ownership",
        "land_size", "has_disability", "disability_type", "disability_percentage",
        "is_widow", "is_single_mother", "is_pregnant", "is_minority",
        "minority_community", "is_ex_serviceman", "is_ward_of_esm",
        "is_bpl", "has_ration_card", "has_bank_account",
        "needs_housing", "has_pucca_house", "crop_type"
    ]
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.conversation_history = []
        self.collected_data = {}
        self.profile_complete = False
        
    def get_system_prompt(self) -> str:
        lang_instruction = _get_language_instruction(self.language)
        return prompts.PROFILE_BUILDER.format(language_instruction=lang_instruction)
    
    def chat(self, user_message: str) -> str:
        """Process user message and return agent response."""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            *self.conversation_history
        ]
        
        # Add context about what we've collected so far
        if self.collected_data:
            context = f"\n\n[INTERNAL: Data collected so far: {json.dumps(self.collected_data)}. Continue gathering remaining information.]"
            messages[-1]["content"] += context
        
        response = llm_client.chat(messages, temperature=0.5)
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Check if profile JSON is in the response
        extracted = _extract_json(response)
        if extracted and isinstance(extracted, dict):
            # Verify it has minimum required fields
            has_required = sum(1 for f in self.REQUIRED_FIELDS if f in extracted)
            if has_required >= 6:  # At least 6 of 9 required fields
                self.collected_data = extracted
                self.profile_complete = True
        
        return response
    
    def build_profile_from_form(self, form_data: dict) -> dict:
        """Build profile directly from form data (skip conversation)."""
        profile = {}
        
        # Map and normalize form data
        field_mapping = {
            "name": str,
            "age": int,
            "gender": lambda x: x.lower(),
            "state": lambda x: x.lower().replace(" ", "_"),
            "district": str,
            "area_type": lambda x: x.lower(),
            "category": lambda x: x.lower(),
            "income": lambda x: int(str(x).replace(",", "").replace("₹", "")),
            "occupation": lambda x: x.lower().replace(" ", "_"),
            "education_level": lambda x: x.lower().replace(" ", "_"),
            "marital_status": lambda x: x.lower(),
            "dependents": int,
            "land_ownership": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "has_disability": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "is_widow": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "is_pregnant": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "is_minority": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "is_bpl": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "is_ex_serviceman": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "is_ward_of_esm": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "has_ration_card": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "has_bank_account": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
            "needs_housing": lambda x: x if isinstance(x, bool) else str(x).lower() in ["yes", "true", "1"],
        }
        
        for field, converter in field_mapping.items():
            if field in form_data and form_data[field] is not None and form_data[field] != "":
                try:
                    profile[field] = converter(form_data[field])
                except (ValueError, TypeError):
                    profile[field] = form_data[field]
        
        self.collected_data = profile
        self.profile_complete = True
        return profile
    
    def get_profile(self) -> Optional[dict]:
        """Return the collected profile if complete."""
        return self.collected_data if self.profile_complete else None


# ═══════════════════════════════════════════════════════════════════════
# AGENT 2: ELIGIBILITY MATCHER
# ═══════════════════════════════════════════════════════════════════════
class EligibilityMatcherAgent:
    """Matches citizen profile against schemes using RAG + LLM reasoning."""
    
    def __init__(self, language: str = "en"):
        self.language = language
    
    def _rule_based_pre_filter(self, profile: dict, scheme: dict) -> tuple:
        """Fast rule-based pre-filtering before LLM analysis. Returns (pass, reason)."""
        elig = scheme.get("eligibility", {})
        
        # Age check
        age = profile.get("age")
        if age:
            if elig.get("min_age") and age < elig["min_age"]:
                return False, f"Age {age} below minimum {elig['min_age']}"
            if elig.get("max_age") and age > elig["max_age"]:
                return False, f"Age {age} above maximum {elig['max_age']}"
        
        # Gender check
        if elig.get("gender") and elig["gender"] != "any":
            if profile.get("gender") and profile["gender"] != elig["gender"]:
                return False, f"Scheme is for {elig['gender']} only"
        
        # Category check
        if elig.get("category"):
            user_cat = profile.get("category", "").lower()
            if user_cat and user_cat not in [c.lower() for c in elig["category"]]:
                # Special handling: Stand Up India is for SC/ST + women
                if scheme.get("id") == "STAND-UP-INDIA" and profile.get("gender") == "female":
                    pass  # Women of all categories eligible
                else:
                    return False, f"Category '{user_cat}' not in eligible categories"
        
        # Income check
        if elig.get("max_income"):
            user_income = profile.get("income", 0)
            if user_income and user_income > elig["max_income"]:
                return False, f"Income ₹{user_income:,} exceeds maximum ₹{elig['max_income']:,}"
        
        # Area type check
        if elig.get("area_type"):
            user_area = profile.get("area_type", "").lower()
            if user_area and user_area not in [a.lower() for a in elig["area_type"]]:
                return False, f"Scheme for {', '.join(elig['area_type'])} area only"
        
        # State check
        states = elig.get("states", "all")
        if states != "all" and isinstance(states, list):
            user_state = profile.get("state", "").lower()
            if user_state and user_state not in [s.lower() for s in states]:
                return False, f"Scheme not available in {profile.get('state')}"
        
        # Occupation check (soft match)
        if elig.get("occupation"):
            user_occ = profile.get("occupation", "").lower()
            elig_occs = [o.lower() for o in elig["occupation"]]
            if user_occ and "any" not in elig_occs:
                # Check for partial match
                occ_match = any(
                    user_occ in elig_occ or elig_occ in user_occ 
                    for elig_occ in elig_occs
                )
                if not occ_match:
                    # Some schemes have broad eligibility
                    if user_occ not in ["any", "unemployed"] and "unemployed" not in elig_occs:
                        return False, f"Occupation '{user_occ}' not matching scheme requirements"
        
        # Education level check
        if elig.get("education_level"):
            user_edu = profile.get("education_level", "").lower()
            if user_edu:
                elig_edu = [e.lower() for e in elig["education_level"]]
                if user_edu not in elig_edu:
                    return False, f"Education level '{user_edu}' not matching"
        
        return True, "Passed pre-filter"
    
    def match(self, profile: dict) -> list:
        """
        Match citizen profile against all schemes.
        Uses hybrid approach: rule-based pre-filter + RAG + LLM reasoning.
        Falls back to rule-based results if LLM is unavailable.
        """
        all_schemes = get_all_schemes()
        
        # Step 1: Rule-based pre-filtering
        candidates = []
        for scheme in all_schemes:
            passed, reason = self._rule_based_pre_filter(profile, scheme)
            if passed:
                candidates.append(scheme)
        
        logger.info(f"Pre-filter: {len(candidates)}/{len(all_schemes)} schemes passed")
        
        # Step 2: RAG search for additional relevant schemes
        try:
            rag_results = vector_store.search_for_profile(profile, n_results=20)
            rag_scheme_ids = {r["scheme_id"] for r in rag_results}
            candidate_ids = {s["id"] for s in candidates}
            
            for scheme_id in rag_scheme_ids:
                if scheme_id not in candidate_ids:
                    scheme = get_scheme_by_id(scheme_id)
                    if scheme:
                        passed, _ = self._rule_based_pre_filter(profile, scheme)
                        if passed:
                            candidates.append(scheme)
            
            logger.info(f"After RAG enrichment: {len(candidates)} candidate schemes")
        except Exception as e:
            logger.warning(f"RAG search failed, using rule-based only: {e}")
        
        # Step 3: Try LLM-based detailed matching
        matched_schemes = []
        
        try:
            batch_size = 8
            for i in range(0, len(candidates), batch_size):
                batch = candidates[i:i+batch_size]
                batch_results = self._llm_match_batch(profile, batch)
                matched_schemes.extend(batch_results)
            
            # Sort by confidence score
            matched_schemes.sort(key=lambda x: x.get("confidence", 0), reverse=True)
            
            # Filter out low-confidence matches
            matched_schemes = [m for m in matched_schemes if m.get("confidence", 0) >= 40]
        except Exception as e:
            logger.warning(f"LLM matching failed: {e}")
            matched_schemes = []
        
        # Step 4: FALLBACK — if LLM returned nothing, use rule-based results
        if not matched_schemes and candidates:
            logger.info(f"Using rule-based fallback for {len(candidates)} candidates")
            matched_schemes = self._rule_based_to_results(profile, candidates)
        
        return matched_schemes
    
    def _rule_based_to_results(self, profile: dict, candidates: list) -> list:
        """Convert rule-based candidates to the standard results format."""
        results = []
        
        for scheme in candidates:
            elig = scheme.get("eligibility", {})
            benefits = scheme.get("benefits", {})
            
            # Calculate a confidence score based on how many criteria match
            confidence = 65  # Base confidence for passing pre-filter
            reasons_eligible = ["Passed automated eligibility checks"]
            reasons_uncertain = []
            priority = "MEDIUM"
            
            # Boost confidence for strong matches
            user_occ = profile.get("occupation", "").lower()
            scheme_occs = [o.lower() for o in elig.get("occupation", ["any"])]
            if user_occ in scheme_occs or "any" in scheme_occs:
                confidence += 10
                reasons_eligible.append(f"Occupation '{user_occ}' matches")
            
            user_cat = profile.get("category", "").lower()
            scheme_cats = [c.lower() for c in elig.get("category", [])]
            if user_cat in scheme_cats:
                confidence += 5
                reasons_eligible.append(f"Category '{user_cat.upper()}' eligible")
            
            user_area = profile.get("area_type", "").lower()
            scheme_areas = [a.lower() for a in elig.get("area_type", [])]
            if user_area in scheme_areas:
                confidence += 5
                reasons_eligible.append(f"{user_area.title()} area eligible")
            
            user_income = profile.get("income", 0)
            if elig.get("max_income") and user_income:
                if user_income <= elig["max_income"]:
                    confidence += 5
                    reasons_eligible.append(f"Income ₹{user_income:,} within limit")
            
            # Check special conditions
            if profile.get("is_bpl") and any("bpl" in t for t in scheme.get("tags", [])):
                confidence += 5
                reasons_eligible.append("BPL status matches")
                priority = "HIGH"
            
            if profile.get("is_widow") and any("widow" in t for t in scheme.get("tags", [])):
                confidence += 10
                priority = "HIGH"
            
            if profile.get("has_disability") and scheme.get("category") == "disability":
                confidence += 10
                priority = "HIGH"
            
            # Determine status
            confidence = min(confidence, 95)
            if confidence >= 80:
                status = "ELIGIBLE"
            elif confidence >= 65:
                status = "LIKELY_ELIGIBLE"
            else:
                status = "PARTIALLY_ELIGIBLE"
            
            # High priority for high-impact schemes
            benefit_amount = benefits.get("amount", "")
            if any(x in benefit_amount.lower() for x in ["lakh", "5,00,000", "free"]):
                priority = "HIGH"
            
            reasons_uncertain.append("Full verification recommended at official portal")
            
            results.append({
                "id": scheme["id"],
                "name": scheme["name"],
                "status": status,
                "confidence": confidence,
                "reasons_eligible": reasons_eligible,
                "reasons_uncertain": reasons_uncertain,
                "estimated_benefit": benefits.get("amount", "N/A"),
                "priority": priority,
                "full_scheme": scheme,
            })
        
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
    
    def _llm_match_batch(self, profile: dict, schemes: list) -> list:
        """Use LLM to analyze eligibility for a batch of schemes."""
        lang_instruction = _get_language_instruction(self.language)
        
        schemes_summary = []
        for s in schemes:
            schemes_summary.append({
                "id": s["id"],
                "name": s["name"],
                "description": s["description"][:200],
                "eligibility": s.get("eligibility", {}),
                "benefits": s.get("benefits", {}),
                "type": s.get("type", ""),
            })
        
        prompt = f"""Analyze the eligibility of this citizen for each government scheme.

CITIZEN PROFILE:
{json.dumps(profile, indent=2)}

SCHEMES TO EVALUATE:
{json.dumps(schemes_summary, indent=2)}

For EACH scheme, determine eligibility and return a JSON array. Each element should have:
- "id": scheme ID
- "name": scheme name  
- "status": "ELIGIBLE" or "LIKELY_ELIGIBLE" or "PARTIALLY_ELIGIBLE"
- "confidence": number 0-100
- "reasons_eligible": list of criteria the citizen meets
- "reasons_uncertain": list of criteria that need verification
- "estimated_benefit": string describing the benefit
- "priority": "HIGH" or "MEDIUM" or "LOW" based on impact

Only include schemes where the citizen has a reasonable chance of eligibility (confidence >= 40).
Return ONLY the JSON array, no other text.

{lang_instruction}"""
        
        messages = [
            {"role": "system", "content": prompts.SYSTEM_BASE},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = llm_client.chat(messages, temperature=0.2, json_mode=True)
            results = _extract_json(response)
            
            if isinstance(results, list):
                # Enrich with full scheme data
                for result in results:
                    scheme = get_scheme_by_id(result.get("id", ""))
                    if scheme:
                        result["full_scheme"] = scheme
                return results
            elif isinstance(results, dict) and "schemes" in results:
                for result in results["schemes"]:
                    scheme = get_scheme_by_id(result.get("id", ""))
                    if scheme:
                        result["full_scheme"] = scheme
                return results["schemes"]
            return []
        except Exception as e:
            logger.error(f"LLM matching error: {e}")
            # Fallback: return all candidates with moderate confidence
            return [{
                "id": s["id"],
                "name": s["name"],
                "status": "LIKELY_ELIGIBLE",
                "confidence": 60,
                "reasons_eligible": ["Passed automated eligibility checks"],
                "reasons_uncertain": ["Detailed verification pending"],
                "estimated_benefit": s.get("benefits", {}).get("amount", "N/A"),
                "priority": "MEDIUM",
                "full_scheme": s,
            } for s in schemes]


# ═══════════════════════════════════════════════════════════════════════
# AGENT 3: DOCUMENT ADVISOR
# ═══════════════════════════════════════════════════════════════════════
class DocumentAdvisorAgent:
    """Provides document requirements and procurement guidance."""
    
    def __init__(self, language: str = "en"):
        self.language = language
    
    def advise(self, profile: dict, matched_schemes: list) -> list:
        """Generate document advice for matched schemes."""
        results = []
        
        for match in matched_schemes:
            scheme = match.get("full_scheme") or get_scheme_by_id(match.get("id", ""))
            if not scheme:
                continue
            
            docs = scheme.get("required_documents", [])
            
            # Categorize documents
            likely_have = []
            need_to_get = []
            
            for doc in docs:
                doc_name = doc["name"].lower()
                
                # Assume most people have Aadhaar and basic ID
                if any(x in doc_name for x in ["aadhaar", "mobile"]):
                    likely_have.append(doc)
                elif any(x in doc_name for x in ["photo", "passport size"]):
                    likely_have.append(doc)
                elif profile.get("has_bank_account") and "bank" in doc_name:
                    likely_have.append(doc)
                else:
                    need_to_get.append(doc)
            
            results.append({
                "scheme_id": scheme["id"],
                "scheme_name": scheme["name"],
                "documents": {
                    "likely_have": likely_have,
                    "need_to_get": need_to_get,
                    "total_required": len(docs),
                    "all_documents": docs,
                }
            })
        
        return results
    
    def get_detailed_advice(self, profile: dict, scheme_id: str) -> str:
        """Get detailed LLM-generated document advice for a specific scheme."""
        scheme = get_scheme_by_id(scheme_id)
        if not scheme:
            return "Scheme not found."
        
        lang_instruction = _get_language_instruction(self.language)
        
        prompt = f"""Provide detailed document guidance for this citizen applying to {scheme['name']}.

CITIZEN PROFILE:
{json.dumps(profile, indent=2)}

SCHEME DOCUMENTS REQUIRED:
{json.dumps(scheme.get('required_documents', []), indent=2)}

For each document, explain:
1. What it is and why it's needed
2. Where exactly to get it (specific office, portal URL)
3. How long it typically takes
4. Any costs involved
5. Common rejection reasons and how to avoid them
6. Digital alternatives (DigiLocker, UMANG app, etc.)

Also suggest the optimal order to collect these documents (some may be prerequisites for others).

{lang_instruction}"""
        
        messages = [
            {"role": "system", "content": prompts.SYSTEM_BASE},
            {"role": "user", "content": prompt}
        ]
        
        return llm_client.chat(messages, temperature=0.3)


# ═══════════════════════════════════════════════════════════════════════
# AGENT 4: APPLICATION GUIDE
# ═══════════════════════════════════════════════════════════════════════
class ApplicationGuideAgent:
    """Provides step-by-step application instructions."""
    
    def __init__(self, language: str = "en"):
        self.language = language
    
    def guide(self, profile: dict, scheme_id: str) -> str:
        """Generate detailed application guide for a specific scheme."""
        scheme = get_scheme_by_id(scheme_id)
        if not scheme:
            return "Scheme not found."
        
        lang_instruction = _get_language_instruction(self.language)
        app_process = scheme.get("application_process", {})
        
        prompt = f"""Provide a VERY DETAILED step-by-step application guide for {scheme['name']}.

CITIZEN PROFILE:
{json.dumps(profile, indent=2)}

SCHEME APPLICATION INFO:
- Mode: {app_process.get('mode', 'N/A')}
- Portal: {app_process.get('portal', 'N/A')}
- Offline: {app_process.get('offline', 'N/A')}
- Steps: {json.dumps(app_process.get('steps', []))}
- Helpline: {app_process.get('helpline', 'N/A')}
- Processing Time: {app_process.get('processing_time', 'N/A')}

SCHEME BENEFITS:
{json.dumps(scheme.get('benefits', {}))}

Please provide:
1. Complete step-by-step instructions (assume the person is not tech-savvy)
2. For online: which website, which buttons, what to type, where to upload
3. For offline: which office, what to carry, best timing to visit, who to ask for
4. Common mistakes and how to avoid them
5. What happens after submission
6. How to track application status
7. Helpline numbers and escalation path
8. Timeline expectations

Make it as simple and hand-holding as possible.

{lang_instruction}"""
        
        messages = [
            {"role": "system", "content": prompts.SYSTEM_BASE},
            {"role": "user", "content": prompt}
        ]
        
        return llm_client.chat(messages, temperature=0.3, max_tokens=4096)
    
    def get_summary(self, matched_schemes: list) -> list:
        """Get application summaries for all matched schemes (no LLM call)."""
        summaries = []
        
        for match in matched_schemes:
            scheme = match.get("full_scheme") or get_scheme_by_id(match.get("id", ""))
            if not scheme:
                continue
            
            app = scheme.get("application_process", {})
            summaries.append({
                "scheme_id": scheme["id"],
                "scheme_name": scheme["name"],
                "mode": app.get("mode", "N/A"),
                "portal": app.get("portal"),
                "offline_location": app.get("offline"),
                "helpline": app.get("helpline"),
                "processing_time": app.get("processing_time"),
                "steps_count": len(app.get("steps", [])),
                "steps_preview": app.get("steps", [])[:3],
            })
        
        return summaries
