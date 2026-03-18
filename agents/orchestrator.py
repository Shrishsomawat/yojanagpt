"""
YojanaGPT - LangGraph Orchestrator
Manages the multi-agent workflow: Profile → Match → Documents → Application Guide.
"""

import json
import logging
from typing import TypedDict, Optional, Annotated
from dataclasses import dataclass, field
from enum import Enum

from langgraph.graph import StateGraph, END

from agents.agents import (
    ProfileBuilderAgent,
    EligibilityMatcherAgent,
    DocumentAdvisorAgent,
    ApplicationGuideAgent,
)
from knowledge_base.vector_store import vector_store
from data.schemes_database import get_all_schemes

logger = logging.getLogger(__name__)


class WorkflowStage(str, Enum):
    PROFILE = "profile"
    MATCHING = "matching"
    DOCUMENTS = "documents"
    APPLICATION = "application"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class YojanaGPTState:
    """State object passed through the LangGraph workflow."""
    # User inputs
    language: str = "en"
    
    # Stage tracking
    current_stage: WorkflowStage = WorkflowStage.PROFILE
    
    # Profile data
    citizen_profile: dict = field(default_factory=dict)
    profile_complete: bool = False
    
    # Matching results
    matched_schemes: list = field(default_factory=list)
    match_count: int = 0
    
    # Document advice
    document_advice: list = field(default_factory=list)
    
    # Application summaries
    application_summaries: list = field(default_factory=list)
    
    # Conversation
    conversation_history: list = field(default_factory=list)
    
    # Errors
    errors: list = field(default_factory=list)


class YojanaGPTOrchestrator:
    """
    Orchestrates the multi-agent pipeline using LangGraph.
    
    Flow:
    1. Profile Building (conversational or form-based)
    2. Eligibility Matching (rule-based + RAG + LLM)
    3. Document Advisory
    4. Application Guidance
    """
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.state = YojanaGPTState(language=language)
        
        # Initialize agents
        self.profile_agent = ProfileBuilderAgent(language)
        self.matcher_agent = EligibilityMatcherAgent(language)
        self.document_agent = DocumentAdvisorAgent(language)
        self.application_agent = ApplicationGuideAgent(language)
        
        # Ensure vector store is initialized
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize the vector store with scheme data."""
        try:
            schemes = get_all_schemes()
            vector_store.initialize(schemes)
            logger.info(f"Vector store ready with {vector_store.scheme_count} chunks")
        except Exception as e:
            logger.error(f"Vector store initialization error: {e}")
            self.state.errors.append(f"Knowledge base error: {e}")
    
    # ─── Profile Stage ────────────────────────────────────────────────
    def chat_for_profile(self, user_message: str) -> str:
        """Chat with profile builder agent."""
        self.state.current_stage = WorkflowStage.PROFILE
        response = self.profile_agent.chat(user_message)
        
        profile = self.profile_agent.get_profile()
        if profile:
            self.state.citizen_profile = profile
            self.state.profile_complete = True
        
        return response
    
    def submit_profile_form(self, form_data: dict) -> dict:
        """Submit profile directly from form (skip conversation)."""
        profile = self.profile_agent.build_profile_from_form(form_data)
        self.state.citizen_profile = profile
        self.state.profile_complete = True
        self.state.current_stage = WorkflowStage.MATCHING
        return profile
    
    # ─── Matching Stage ───────────────────────────────────────────────
    def run_matching(self) -> list:
        """Run eligibility matching against all schemes."""
        if not self.state.profile_complete:
            raise ValueError("Profile not complete. Gather profile first.")
        
        self.state.current_stage = WorkflowStage.MATCHING
        
        try:
            matches = self.matcher_agent.match(self.state.citizen_profile)
            self.state.matched_schemes = matches
            self.state.match_count = len(matches)
            
            logger.info(f"Found {len(matches)} matching schemes")
            return matches
        except Exception as e:
            logger.error(f"Matching error: {e}")
            self.state.errors.append(f"Matching error: {e}")
            return []
    
    # ─── Document Stage ───────────────────────────────────────────────
    def run_document_advisory(self) -> list:
        """Generate document advice for matched schemes."""
        if not self.state.matched_schemes:
            return []
        
        self.state.current_stage = WorkflowStage.DOCUMENTS
        
        try:
            advice = self.document_agent.advise(
                self.state.citizen_profile,
                self.state.matched_schemes
            )
            self.state.document_advice = advice
            return advice
        except Exception as e:
            logger.error(f"Document advisory error: {e}")
            self.state.errors.append(f"Document error: {e}")
            return []
    
    def get_detailed_document_advice(self, scheme_id: str) -> str:
        """Get detailed LLM-generated document advice for one scheme."""
        return self.document_agent.get_detailed_advice(
            self.state.citizen_profile, scheme_id
        )
    
    # ─── Application Stage ────────────────────────────────────────────
    def run_application_guidance(self) -> list:
        """Generate application summaries for matched schemes."""
        if not self.state.matched_schemes:
            return []
        
        self.state.current_stage = WorkflowStage.APPLICATION
        
        try:
            summaries = self.application_agent.get_summary(self.state.matched_schemes)
            self.state.application_summaries = summaries
            return summaries
        except Exception as e:
            logger.error(f"Application guidance error: {e}")
            self.state.errors.append(f"Application error: {e}")
            return []
    
    def get_detailed_application_guide(self, scheme_id: str) -> str:
        """Get detailed LLM-generated application guide for one scheme."""
        return self.application_agent.guide(
            self.state.citizen_profile, scheme_id
        )
    
    # ─── Full Pipeline ────────────────────────────────────────────────
    def run_full_pipeline(self, profile: dict = None) -> dict:
        """
        Run the complete pipeline end-to-end.
        
        Args:
            profile: Pre-built citizen profile (skip conversation)
            
        Returns:
            Complete results dict
        """
        if profile:
            self.submit_profile_form(profile)
        
        if not self.state.profile_complete:
            return {"error": "Profile not complete"}
        
        # Run all stages
        matches = self.run_matching()
        documents = self.run_document_advisory()
        applications = self.run_application_guidance()
        
        self.state.current_stage = WorkflowStage.COMPLETE
        
        return {
            "profile": self.state.citizen_profile,
            "matched_schemes": matches,
            "match_count": len(matches),
            "document_advice": documents,
            "application_summaries": applications,
            "errors": self.state.errors,
        }
    
    # ─── State Access ─────────────────────────────────────────────────
    @property
    def current_stage(self) -> str:
        return self.state.current_stage.value
    
    @property
    def profile(self) -> dict:
        return self.state.citizen_profile
    
    @property
    def matches(self) -> list:
        return self.state.matched_schemes
    
    @property
    def is_profile_complete(self) -> bool:
        return self.state.profile_complete
    
    def reset(self):
        """Reset the orchestrator state."""
        self.state = YojanaGPTState(language=self.language)
        self.profile_agent = ProfileBuilderAgent(self.language)
