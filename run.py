#!/usr/bin/env python3
"""
YojanaGPT - Main Runner
Usage:
    streamlit run:    streamlit run ui/streamlit_app.py
    CLI demo:         python run.py --demo
    Test matching:    python run.py --test
    Review freshness: python run.py --review
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def run_demo():
    """Run a quick CLI demo with sample profiles — works WITHOUT any API key."""
    print("\n" + "=" * 70)
    print("🇮🇳  YojanaGPT — Government Scheme Navigator (Demo Mode)")
    print("=" * 70)
    
    from data.schemes_database import get_all_schemes, get_scheme_count
    from knowledge_base.vector_store import vector_store
    from agents.agents import EligibilityMatcherAgent
    
    print(f"\n📊 Loaded {get_scheme_count()} government schemes")
    
    # Initialize vector store
    print("🔄 Building knowledge base...")
    schemes = get_all_schemes()
    vector_store.initialize(schemes)
    print(f"✅ Knowledge base ready ({vector_store.scheme_count} chunks indexed)")
    
    # Sample profiles for demo
    sample_profiles = [
        {
            "name": "Ramesh Kumar",
            "age": 45,
            "gender": "male",
            "state": "rajasthan",
            "area_type": "rural",
            "category": "obc",
            "income": 150000,
            "occupation": "farmer",
            "education_level": "class_10",
            "land_ownership": True,
            "is_bpl": True,
            "has_ration_card": True,
            "has_bank_account": True,
            "needs_housing": True,
        },
        {
            "name": "Priya Sharma",
            "age": 20,
            "gender": "female",
            "state": "uttar_pradesh",
            "area_type": "urban",
            "category": "sc",
            "income": 200000,
            "occupation": "student",
            "education_level": "undergraduate",
            "is_bpl": False,
            "has_bank_account": True,
        },
        {
            "name": "Fatima Begum",
            "age": 35,
            "gender": "female",
            "state": "west_bengal",
            "area_type": "rural",
            "category": "general",
            "income": 80000,
            "occupation": "homemaker",
            "education_level": "below_10",
            "is_bpl": True,
            "is_widow": True,
            "is_minority": True,
            "has_ration_card": True,
            "needs_housing": True,
            "dependents": 3,
        },
    ]
    
    for profile in sample_profiles:
        print(f"\n{'─' * 70}")
        print(f"👤 Profile: {profile['name']}")
        print(f"   Age: {profile['age']} | Gender: {profile['gender'].title()}")
        print(f"   State: {profile['state'].replace('_', ' ').title()}")
        print(f"   Occupation: {profile['occupation'].replace('_', ' ').title()}")
        print(f"   Category: {profile['category'].upper()} | Income: ₹{profile['income']:,}")
        print(f"   Area: {profile['area_type'].title()}")
        
        special = []
        if profile.get("is_bpl"): special.append("BPL")
        if profile.get("is_widow"): special.append("Widow")
        if profile.get("is_minority"): special.append("Minority")
        if profile.get("land_ownership"): special.append("Land Owner")
        if special:
            print(f"   Special: {', '.join(special)}")
        
        # Run rule-based matching (no LLM needed)
        matcher = EligibilityMatcherAgent()
        
        # Quick rule-based filter
        from data.schemes_database import get_all_schemes
        all_schemes = get_all_schemes()
        matched = []
        
        for scheme in all_schemes:
            passed, reason = matcher._rule_based_pre_filter(profile, scheme)
            if passed:
                matched.append(scheme)
        
        print(f"\n   🎯 Matched {len(matched)} schemes (rule-based):")
        
        for i, scheme in enumerate(matched, 1):
            benefits = scheme.get("benefits", {}).get("amount", "N/A")
            print(f"      {i:2d}. {scheme['name']}")
            print(f"          💰 {benefits}")
            print(f"          📋 {scheme['ministry']}")
        
        if not matched:
            print("      No schemes matched. Try adjusting the profile.")
    
    print(f"\n{'=' * 70}")
    print("✅ Demo complete! To use the full AI-powered system:")
    print("   1. Set your GROQ_API_KEY in .env (free at console.groq.com)")
    print("   2. Run: streamlit run ui/streamlit_app.py")
    print("=" * 70 + "\n")


def run_test():
    """Quick test to verify all modules load correctly."""
    print("\n🧪 Running YojanaGPT system tests...\n")
    
    errors = []
    
    # Test 1: Config
    try:
        from config.settings import llm_config, vector_config, app_config, prompts
        print("  ✅ Config module loaded")
    except Exception as e:
        errors.append(f"Config: {e}")
        print(f"  ❌ Config: {e}")
    
    # Test 2: Schemes database
    try:
        from data.schemes_database import get_all_schemes, get_scheme_by_id, get_scheme_count
        count = get_scheme_count()
        assert count > 30, f"Expected 30+ schemes, got {count}"
        
        scheme = get_scheme_by_id("PM-KISAN")
        assert scheme is not None, "PM-KISAN not found"
        assert "eligibility" in scheme, "Missing eligibility"
        assert "required_documents" in scheme, "Missing documents"
        assert "application_process" in scheme, "Missing application process"
        
        print(f"  ✅ Schemes database: {count} schemes loaded")
    except Exception as e:
        errors.append(f"Schemes: {e}")
        print(f"  ❌ Schemes: {e}")
    
    # Test 3: Vector store
    try:
        from knowledge_base.vector_store import vector_store
        from data.schemes_database import get_all_schemes
        
        vector_store.initialize(get_all_schemes())
        
        results = vector_store.search("farmer agriculture scheme")
        assert len(results) > 0, "No search results"
        assert results[0]["relevance_score"] > 0, "Bad relevance score"
        
        print(f"  ✅ Vector store: {vector_store.scheme_count} chunks, search working")
    except Exception as e:
        errors.append(f"Vector store: {e}")
        print(f"  ❌ Vector store: {e}")
    
    # Test 4: LLM client (just initialization, no API call)
    try:
        from utils.llm_client import llm_client
        provider = llm_client.get_active_provider()
        print(f"  ✅ LLM client: active provider = {provider}")
    except Exception as e:
        errors.append(f"LLM client: {e}")
        print(f"  ❌ LLM client: {e}")
    
    # Test 5: Agents (initialization only)
    try:
        from agents.agents import (
            ProfileBuilderAgent, EligibilityMatcherAgent,
            DocumentAdvisorAgent, ApplicationGuideAgent
        )
        
        pb = ProfileBuilderAgent("en")
        em = EligibilityMatcherAgent("en")
        da = DocumentAdvisorAgent("en")
        ag = ApplicationGuideAgent("en")
        
        # Test form-based profile building
        profile = pb.build_profile_from_form({
            "name": "Test User", "age": "30", "gender": "male",
            "state": "delhi", "area_type": "urban", "category": "general",
            "income": "500000", "occupation": "salaried",
            "education_level": "undergraduate"
        })
        assert profile["age"] == 30
        assert profile["income"] == 500000
        assert pb.profile_complete is True
        
        print("  ✅ All 4 agents initialized and profile builder working")
    except Exception as e:
        errors.append(f"Agents: {e}")
        print(f"  ❌ Agents: {e}")
    
    # Test 6: Rule-based matching
    try:
        test_profile = {
            "name": "Test Farmer", "age": 40, "gender": "male",
            "state": "rajasthan", "area_type": "rural", "category": "obc",
            "income": 150000, "occupation": "farmer", "land_ownership": True,
        }
        
        from agents.agents import EligibilityMatcherAgent
        matcher = EligibilityMatcherAgent()
        
        from data.schemes_database import get_all_schemes
        passed = 0
        for scheme in get_all_schemes():
            result, _ = matcher._rule_based_pre_filter(test_profile, scheme)
            if result:
                passed += 1
        
        assert passed > 5, f"Expected 5+ matches for farmer, got {passed}"
        print(f"  ✅ Rule-based matching: {passed} schemes matched for test farmer")
    except Exception as e:
        errors.append(f"Matching: {e}")
        print(f"  ❌ Matching: {e}")
    
    # Test 7: PDF generator
    try:
        from utils.pdf_generator import generate_report
        
        test_matches = [{
            "id": "PM-KISAN",
            "name": "PM-KISAN Samman Nidhi",
            "status": "ELIGIBLE",
            "confidence": 90,
            "reasons_eligible": ["Is a farmer", "Owns land"],
            "reasons_uncertain": [],
            "estimated_benefit": "Rs 6,000/year",
            "priority": "HIGH",
            "full_scheme": get_scheme_by_id("PM-KISAN"),
        }]
        
        test_docs = [{
            "scheme_id": "PM-KISAN",
            "scheme_name": "PM-KISAN",
            "documents": {
                "likely_have": [{"name": "Aadhaar", "mandatory": True, "where_to_get": "UIDAI"}],
                "need_to_get": [{"name": "Land records", "mandatory": True, "where_to_get": "Revenue office"}],
                "all_documents": get_scheme_by_id("PM-KISAN")["required_documents"],
            }
        }]
        
        pdf_path = generate_report(
            profile=test_profile,
            matched_schemes=test_matches,
            document_advice=test_docs,
            output_path="/tmp/yojanagpt_test.pdf"
        )
        
        file_size = os.path.getsize(pdf_path)
        assert file_size > 1000, f"PDF too small: {file_size} bytes"
        
        print(f"  ✅ PDF generator: {file_size:,} bytes written to {pdf_path}")
    except Exception as e:
        errors.append(f"PDF: {e}")
        print(f"  ❌ PDF: {e}")
    
    # Summary
    print(f"\n{'─' * 50}")
    if errors:
        print(f"  ⚠️  {len(errors)} test(s) failed:")
        for err in errors:
            print(f"     • {err}")
    else:
        print("  🎉 All tests passed!")
    print(f"{'─' * 50}\n")
    
    return len(errors) == 0


def run_review():
    """Print a freshness review report for all schemes."""
    from scripts.review_verified_schemes import print_review_report

    print_review_report()


def main():
    parser = argparse.ArgumentParser(description="YojanaGPT - Government Scheme Navigator")
    parser.add_argument("--demo", action="store_true", help="Run CLI demo with sample profiles")
    parser.add_argument("--test", action="store_true", help="Run system tests")
    parser.add_argument("--review", action="store_true", help="Review scheme freshness status")
    parser.add_argument("--streamlit", action="store_true", help="Launch Streamlit UI")
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
    elif args.test:
        success = run_test()
        sys.exit(0 if success else 1)
    elif args.review:
        run_review()
    elif args.streamlit:
        os.system(f"streamlit run {PROJECT_ROOT}/ui/streamlit_app.py")
    else:
        # Default: run tests then show usage
        print("\n🇮🇳 YojanaGPT — Government Scheme Navigator\n")
        print("Usage:")
        print("  python run.py --demo       Run CLI demo (no API key needed)")
        print("  python run.py --test       Run system tests")
        print("  python run.py --review     Review verified vs stale schemes")
        print("  python run.py --streamlit  Launch Streamlit UI")
        print("  streamlit run ui/streamlit_app.py  Launch UI directly")
        print("\nQuick start:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your GROQ_API_KEY (free at console.groq.com)")
        print("  3. Run: streamlit run ui/streamlit_app.py\n")


if __name__ == "__main__":
    main()
