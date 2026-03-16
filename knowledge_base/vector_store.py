"""
YojanaGPT - Vector Store Manager
Manages ChromaDB for semantic search over government schemes.
Uses ChromaDB's built-in embedding (all-MiniLM-L6-v2 via onnxruntime — no PyTorch needed).
"""

import json
import logging
from typing import Optional
import chromadb
from chromadb.config import Settings
from config.settings import vector_config

logger = logging.getLogger(__name__)


class SchemeVectorStore:
    """Manages the ChromaDB vector store for government schemes."""
    
    def __init__(self):
        self.config = vector_config
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True,
        ))
        self.collection = None
        self._initialized = False
    
    def initialize(self, schemes: list):
        """Ingest schemes into vector store."""
        if self._initialized:
            return
        
        logger.info(f"Initializing vector store with {len(schemes)} schemes...")
        
        # Create or get collection
        try:
            self.client.delete_collection(self.config.collection_name)
        except Exception:
            pass
        
        self.collection = self.client.create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        documents = []
        metadatas = []
        ids = []
        
        for scheme in schemes:
            # Create multiple chunks per scheme for better retrieval
            chunks = self._create_scheme_chunks(scheme)
            
            for i, (chunk_text, chunk_meta) in enumerate(chunks):
                doc_id = f"{scheme['id']}_chunk_{i}"
                documents.append(chunk_text)
                metadatas.append(chunk_meta)
                ids.append(doc_id)
        
        # Batch insert (ChromaDB handles embeddings automatically)
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size],
            )
        
        self._initialized = True
        logger.info(f"Vector store initialized: {len(documents)} chunks from {len(schemes)} schemes")
    
    def _create_scheme_chunks(self, scheme: dict) -> list:
        """Create semantic chunks from a scheme for better retrieval."""
        chunks = []
        base_meta = {
            "scheme_id": scheme["id"],
            "scheme_name": scheme["name"],
            "category": scheme["category"],
            "ministry": scheme["ministry"],
            "type": scheme.get("type", ""),
            "tags": ",".join(scheme.get("tags", [])),
        }
        
        # Chunk 1: Overview + Description
        overview = (
            f"Scheme: {scheme['name']}. "
            f"Ministry: {scheme['ministry']}. "
            f"Type: {scheme.get('type', 'N/A')}. "
            f"Category: {scheme['category']}. "
            f"Description: {scheme['description']} "
            f"Benefits: {json.dumps(scheme.get('benefits', {}))}. "
            f"Tags: {', '.join(scheme.get('tags', []))}."
        )
        chunks.append((overview, {**base_meta, "chunk_type": "overview"}))
        
        # Chunk 2: Eligibility Criteria (most important for matching)
        eligibility = scheme.get("eligibility", {})
        elig_text = f"Eligibility for {scheme['name']}: "
        
        if eligibility.get("occupation"):
            elig_text += f"Occupation: {', '.join(eligibility['occupation'])}. "
        if eligibility.get("min_age"):
            elig_text += f"Minimum age: {eligibility['min_age']}. "
        if eligibility.get("max_age"):
            elig_text += f"Maximum age: {eligibility['max_age']}. "
        if eligibility.get("gender") and eligibility["gender"] != "any":
            elig_text += f"Gender: {eligibility['gender']}. "
        if eligibility.get("category"):
            elig_text += f"Category: {', '.join(eligibility['category'])}. "
        if eligibility.get("area_type"):
            elig_text += f"Area: {', '.join(eligibility['area_type'])}. "
        if eligibility.get("max_income"):
            elig_text += f"Maximum annual income: ₹{eligibility['max_income']:,}. "
        if eligibility.get("states") and eligibility["states"] != "all":
            elig_text += f"States: {', '.join(eligibility['states'])}. "
        if eligibility.get("special_conditions"):
            elig_text += f"Special conditions: {'; '.join(eligibility['special_conditions'])}. "
        if eligibility.get("education_level"):
            elig_text += f"Education level: {', '.join(eligibility['education_level'])}. "
        if eligibility.get("exclusions"):
            elig_text += f"Exclusions: {'; '.join(eligibility['exclusions'])}. "
        if eligibility.get("land_ownership") is True:
            elig_text += "Must own agricultural land. "
        
        # Add income meta for filtering
        elig_meta = {**base_meta, "chunk_type": "eligibility"}
        if eligibility.get("max_income"):
            elig_meta["max_income"] = str(eligibility["max_income"])
        
        chunks.append((elig_text, elig_meta))
        
        # Chunk 3: Documents Required
        docs = scheme.get("required_documents", [])
        if docs:
            docs_text = f"Documents required for {scheme['name']}: "
            for doc in docs:
                docs_text += f"{doc['name']} ({'mandatory' if doc['mandatory'] else 'optional'}, get from: {doc['where_to_get']}). "
            chunks.append((docs_text, {**base_meta, "chunk_type": "documents"}))
        
        # Chunk 4: Application Process
        app = scheme.get("application_process", {})
        if app:
            app_text = f"How to apply for {scheme['name']}: "
            app_text += f"Mode: {app.get('mode', 'N/A')}. "
            if app.get("portal"):
                app_text += f"Portal: {app['portal']}. "
            if app.get("offline"):
                app_text += f"Offline: {app['offline']}. "
            if app.get("steps"):
                app_text += "Steps: " + " → ".join(app["steps"]) + ". "
            if app.get("helpline"):
                app_text += f"Helpline: {app['helpline']}. "
            if app.get("processing_time"):
                app_text += f"Processing time: {app['processing_time']}."
            chunks.append((app_text, {**base_meta, "chunk_type": "application"}))
        
        return chunks
    
    def search(self, query: str, n_results: int = None, 
               category_filter: str = None,
               tag_filter: str = None) -> list:
        """
        Search for relevant scheme chunks.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            category_filter: Filter by scheme category
            tag_filter: Filter by tag
            
        Returns:
            List of dicts with scheme info and relevance scores
        """
        if not self._initialized or not self.collection:
            return []
        
        n = n_results or self.config.top_k
        
        # Build where filter
        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(n, self.collection.count()),
                where=where_filter if where_filter else None,
            )
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
        
        # Process results
        processed = []
        seen_schemes = set()
        
        if results and results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results["distances"] else 1.0
                relevance = 1 - distance  # Convert distance to similarity
                
                scheme_id = meta.get("scheme_id", "")
                
                # Apply tag filter post-query
                if tag_filter and tag_filter not in meta.get("tags", ""):
                    continue
                
                processed.append({
                    "scheme_id": scheme_id,
                    "scheme_name": meta.get("scheme_name", ""),
                    "category": meta.get("category", ""),
                    "chunk_type": meta.get("chunk_type", ""),
                    "content": results["documents"][0][i],
                    "relevance_score": round(relevance, 4),
                    "is_new_scheme": scheme_id not in seen_schemes,
                })
                seen_schemes.add(scheme_id)
        
        return processed
    
    def search_for_profile(self, citizen_profile: dict, n_results: int = 30) -> list:
        """
        Smart search based on citizen profile — builds multiple targeted queries
        to maximize relevant scheme retrieval.
        """
        queries = []
        
        # Base demographic query
        base_parts = []
        if citizen_profile.get("occupation"):
            base_parts.append(f"schemes for {citizen_profile['occupation']}")
        if citizen_profile.get("category"):
            base_parts.append(f"{citizen_profile['category']} category")
        if citizen_profile.get("area_type"):
            base_parts.append(f"{citizen_profile['area_type']} area")
        if citizen_profile.get("state"):
            base_parts.append(citizen_profile["state"])
        if base_parts:
            queries.append(" ".join(base_parts))
        
        # Income-based query
        if citizen_profile.get("income"):
            income = citizen_profile["income"]
            if income < 100000:
                queries.append("BPL below poverty line low income welfare assistance")
            elif income < 250000:
                queries.append("economically weaker section low income subsidy")
            elif income < 500000:
                queries.append("middle income family financial assistance")
        
        # Gender-specific queries
        if citizen_profile.get("gender", "").lower() == "female":
            queries.append("women welfare scheme girl child maternity benefit empowerment")
            if citizen_profile.get("is_widow"):
                queries.append("widow pension financial assistance")
            if citizen_profile.get("is_pregnant"):
                queries.append("pregnancy maternity benefit prenatal postnatal")
        
        # Occupation-specific queries
        occupation = citizen_profile.get("occupation", "").lower()
        if occupation in ["farmer", "agriculture"]:
            queries.append("farmer agriculture kisan crop insurance credit subsidy")
            queries.append("solar pump farm equipment agriculture land")
        elif occupation in ["student"]:
            queries.append("scholarship education student financial assistance")
            edu_level = citizen_profile.get("education_level", "")
            if edu_level:
                queries.append(f"scholarship for {edu_level} students")
        elif occupation in ["unemployed"]:
            queries.append("employment guarantee skill training job placement")
            queries.append("business loan entrepreneur self employment")
        elif occupation in ["street_vendor", "vendor"]:
            queries.append("street vendor loan micro credit urban livelihood")
        elif occupation in ["construction_worker", "daily_wage", "labour"]:
            queries.append("unorganized worker labour welfare pension construction")
        
        # Category-specific queries
        category = citizen_profile.get("category", "").lower()
        if category == "sc":
            queries.append("scheduled caste SC welfare scholarship reservation")
        elif category == "st":
            queries.append("scheduled tribe ST tribal welfare forest rights")
        elif category == "obc":
            queries.append("OBC other backward classes scholarship welfare")
        
        # Age-specific queries
        age = citizen_profile.get("age")
        if age:
            if age >= 60:
                queries.append("senior citizen pension old age retirement benefit")
            elif age < 25:
                queries.append("youth skill development apprenticeship training")
        
        # Disability query
        if citizen_profile.get("has_disability"):
            queries.append("disability handicapped assistive devices pension welfare")
        
        # Housing query
        if citizen_profile.get("needs_housing"):
            area = citizen_profile.get("area_type", "")
            queries.append(f"housing pucca house construction {area} awas yojana")
        
        # Insurance/banking query
        queries.append("insurance pension banking financial inclusion")
        
        # Special conditions
        if citizen_profile.get("is_minority"):
            queries.append("minority community Muslim Christian Sikh Buddhist scholarship")
        if citizen_profile.get("is_ex_serviceman") or citizen_profile.get("is_ward_of_esm"):
            queries.append("ex-serviceman defence ward scholarship welfare")
        if citizen_profile.get("is_bpl"):
            queries.append("BPL below poverty line free ration housing toilet")
        
        # Execute all queries and deduplicate
        all_results = []
        seen_scheme_ids = set()
        
        for query in queries:
            results = self.search(query, n_results=10)
            for r in results:
                if r["scheme_id"] not in seen_scheme_ids:
                    all_results.append(r)
                    seen_scheme_ids.add(r["scheme_id"])
        
        # Sort by relevance
        all_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return all_results[:n_results]
    
    @property
    def scheme_count(self) -> int:
        """Return number of indexed chunks."""
        if self.collection:
            return self.collection.count()
        return 0


# Singleton
vector_store = SchemeVectorStore()
