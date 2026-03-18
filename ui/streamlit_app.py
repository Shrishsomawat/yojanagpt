"""
YojanaGPT - Streamlit UI
Production-grade interface for the Government Scheme Navigator.
"""

import os
import sys
import json
import time
import logging
import streamlit as st
from pathlib import Path
from datetime import date, datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import app_config, llm_config, LLMProvider
from agents.orchestrator import YojanaGPTOrchestrator
from utils.pdf_generator import generate_report
from utils.llm_client import llm_client
from data.schemes_database import get_scheme_count, get_scheme_by_id, get_verified_scheme_count
from scripts.review_verified_schemes import build_review_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="YojanaGPT - Government Scheme Navigator",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Sidebar fix (dark mode compatible) ── */
    section[data-testid="stSidebar"] {
        background: #0E1117 !important;
        border-right: 1px solid #2a2d35;
    }
    section[data-testid="stSidebar"] * {
        color: #E0E0E0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stCaption p {
        color: #C8CCD0 !important;
    }
    section[data-testid="stSidebar"] .stAlert {
        background: #1a3a2a !important;
        border: 1px solid #2d6b45 !important;
    }
    section[data-testid="stSidebar"] .stAlert p {
        color: #6fcf97 !important;
    }
    section[data-testid="stSidebar"] .stMetric label {
        color: #9CA3AF !important;
    }
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #FF9933 !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: #1E3A5F !important;
        color: #E0E0E0 !important;
        border: 1px solid #2D5A8E !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #2D5A8E !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #2a2d35 !important;
    }

    /* ── Main header (tricolor gradient) ── */
    .main-header {
        background: linear-gradient(135deg, #FF9933 0%, #1a1a2e 50%, #138808 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: #FFFFFF;
        font-size: 2.4rem;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: #D4D4D4;
        font-size: 1.05rem;
        margin-top: 0.4rem;
    }

    /* ── Stats cards ── */
    .stat-card {
        text-align: center;
        padding: 1.2rem 1rem;
        border-radius: 12px;
        background: #161B22;
        border: 1px solid #30363D;
    }
    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF9933;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #9CA3AF;
        margin-top: 0.25rem;
    }

    /* ── Confidence meter ── */
    .confidence-bar {
        height: 8px;
        border-radius: 4px;
        background: #30363D;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }

    /* ── Status badges ── */
    .badge-eligible {
        background: #1a3a2a;
        color: #6fcf97;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #2d6b45;
    }
    .badge-likely {
        background: #3a2a0a;
        color: #F0B429;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #6b5a2d;
    }
    .badge-partial {
        background: #0d2137;
        color: #58A6FF;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #1f4a7a;
    }

    /* ── Document checklist ── */
    .doc-item {
        padding: 0.7rem 0.9rem;
        border-left: 3px solid #FF9933;
        margin-bottom: 0.6rem;
        background: #161B22;
        border-radius: 0 8px 8px 0;
        border-top: 1px solid #30363D;
        border-right: 1px solid #30363D;
        border-bottom: 1px solid #30363D;
    }
    .doc-item strong {
        color: #E0E0E0;
    }
    .doc-item small {
        color: #9CA3AF;
    }

    /* ── Scheme cards ── */
    .scheme-card {
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        background: #161B22;
    }
    .scheme-name {
        color: #E0E0E0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .scheme-ministry {
        color: #9CA3AF;
        font-size: 0.85rem;
    }

    /* ── Global tweaks ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Form styling */
    .stForm {
        border: 1px solid #30363D !important;
        border-radius: 12px;
        padding: 1rem;
    }
    .intro-panel, .action-panel, .trust-panel {
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        background: linear-gradient(180deg, rgba(22,27,34,0.98), rgba(13,17,23,0.98));
        margin-bottom: 1rem;
    }
    .intro-panel h3, .action-panel h4, .trust-panel h4 {
        color: #F3F4F6;
        margin: 0 0 0.45rem 0;
    }
    .intro-panel p, .action-panel p, .trust-panel p {
        color: #C8CCD0;
        margin: 0;
        line-height: 1.45;
    }
    .step-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.65rem;
        margin: 0.9rem 0 1rem 0;
    }
    .step-chip {
        border: 1px solid #30363D;
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
        background: #161B22;
    }
    .step-chip strong {
        display: block;
        color: #F9FAFB;
        margin-bottom: 0.2rem;
    }
    .step-chip span {
        color: #9CA3AF;
        font-size: 0.86rem;
    }
    .wizard-shell {
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 1rem;
        background: #10151d;
        margin-bottom: 1rem;
    }
    .wizard-step-title {
        color: #F9FAFB;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .wizard-step-copy {
        color: #9CA3AF;
        margin-bottom: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State ────────────────────────────────────────────────────
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "orchestrator": None,
        "stage": "input",  # input -> processing -> results
        "results": None,
        "selected_scheme": None,
        "chat_messages": [],
        "chat_mode": False,
        "language": "en",
        "profile_submitted": False,
        "error_message": None,
        "admin_view": False,
        "form_step": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
        elif st.session_state[key] is None and isinstance(value, (list, dict, str)):
            st.session_state[key] = value.copy() if isinstance(value, (list, dict)) else value

# ─── Helper Functions ─────────────────────────────────────────────────
def get_orchestrator() -> YojanaGPTOrchestrator:
    """Get or create orchestrator instance."""
    if st.session_state.orchestrator is None:
        st.session_state.orchestrator = YojanaGPTOrchestrator(
            language=st.session_state.language
        )
    return st.session_state.orchestrator


def has_remote_llm() -> bool:
    """Check whether a hosted LLM provider is configured."""
    return llm_client.has_remote_llm()


def get_confidence_color(confidence: int) -> str:
    if confidence >= 80:
        return "#4caf50"
    elif confidence >= 60:
        return "#ff9800"
    elif confidence >= 40:
        return "#2196f3"
    return "#9e9e9e"


def get_status_badge(status: str) -> str:
    class_map = {
        "ELIGIBLE": "badge-eligible",
        "LIKELY_ELIGIBLE": "badge-likely",
        "PARTIALLY_ELIGIBLE": "badge-partial",
    }
    css_class = class_map.get(status, "badge-partial")
    display = status.replace("_", " ")
    return f'<span class="{css_class}">{display}</span>'


def get_verification_badge(scheme: dict) -> str:
    """Render a simple freshness badge for a scheme."""
    status = scheme.get("verification_status", "needs_review")
    verified_on = scheme.get("last_verified_on")
    review_due_on = scheme.get("review_due_on")
    due_date = None
    if review_due_on:
        try:
            due_date = datetime.strptime(review_due_on, "%Y-%m-%d").date()
        except ValueError:
            due_date = None

    if status == "verified":
        if due_date and due_date < date.today():
            label = f"Overdue review since {review_due_on}"
            color = "#FFB4B4"
            border = "#A94442"
            background = "#3A1F1F"
        elif due_date and (due_date - date.today()).days <= 7:
            label = f"Review due {review_due_on}"
            color = "#F0B429"
            border = "#6b5a2d"
            background = "#3a2a0a"
        else:
            label = f"Verified {verified_on}" if verified_on else "Verified"
            color = "#6fcf97"
            border = "#2d6b45"
            background = "#1a3a2a"
    else:
        label = "Needs review"
        color = "#F0B429"
        border = "#6b5a2d"
        background = "#3a2a0a"

    return (
        f'<span style="background:{background};color:{color};padding:3px 10px;'
        f'border-radius:12px;font-size:0.78rem;font-weight:600;border:1px solid {border};">'
        f"{label}</span>"
    )


def reset_app():
    """Reset the application state."""
    st.session_state.orchestrator = None
    st.session_state.results = None
    st.session_state.selected_scheme = None
    st.session_state.chat_messages = []
    st.session_state.error_message = None
    st.session_state.stage = "input"
    st.session_state.profile_submitted = False
    st.session_state.chat_mode = False
    st.session_state.form_step = 0


FORM_STEPS = [
    ("Personal", "Basic identity and family context"),
    ("Background", "Location, category, and income"),
    ("Work & Study", "Occupation and education details"),
    ("Special Needs", "Conditions that unlock targeted schemes"),
]

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh",
]


def render_onboarding_panel():
    st.markdown(
        """
        <div class="intro-panel">
            <h3>Start In 3 Simple Steps</h3>
            <p>Tell us about your situation, review verified scheme matches, and leave with documents plus next actions you can actually follow.</p>
            <div class="step-grid">
                <div class="step-chip"><strong>1. Share profile</strong><span>Income, occupation, category, and needs.</span></div>
                <div class="step-chip"><strong>2. See verified matches</strong><span>Only currently reviewed schemes are shown.</span></div>
                <div class="step-chip"><strong>3. Take action</strong><span>Use official links, documents, and application steps.</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_form_profile() -> dict:
    income_map = {
        "Below Rs 1 Lakh": 80000,
        "Rs 1 - 2.5 Lakh": 175000,
        "Rs 2.5 - 5 Lakh": 375000,
        "Rs 5 - 10 Lakh": 750000,
        "Rs 10 - 18 Lakh": 1400000,
        "Above Rs 18 Lakh": 2500000,
    }
    occ_map = {
        "Student": "student", "Farmer": "farmer", "Unemployed": "unemployed",
        "Self Employed": "self_employed", "Salaried Employee": "salaried",
        "Daily Wage Worker": "daily_wage", "Homemaker": "homemaker",
        "Street Vendor": "street_vendor", "Construction Worker": "construction_worker",
        "Domestic Worker": "domestic_worker", "Retired": "retired", "Other": "other",
    }
    edu_map = {
        "No Formal Education": "no_formal", "Below Class 10": "below_10",
        "Class 10": "class_10", "Class 12": "class_12",
        "ITI / Diploma": "diploma", "Undergraduate": "undergraduate",
        "Postgraduate": "postgraduate", "PhD": "phd",
    }

    return {
        "name": st.session_state.get("wizard_name", "").strip(),
        "age": st.session_state.get("wizard_age", 25),
        "gender": st.session_state.get("wizard_gender", "Male").lower(),
        "state": st.session_state.get("wizard_state", "Delhi").lower().replace(" ", "_"),
        "area_type": st.session_state.get("wizard_area_type", "Urban").lower(),
        "category": st.session_state.get("wizard_category", "General").lower(),
        "occupation": occ_map.get(st.session_state.get("wizard_occupation", "Other"), "other"),
        "income": income_map.get(st.session_state.get("wizard_income", "Rs 2.5 - 5 Lakh"), 375000),
        "education_level": edu_map.get(st.session_state.get("wizard_education", "Undergraduate"), "undergraduate"),
        "marital_status": st.session_state.get("wizard_marital_status", "Single").lower(),
        "dependents": st.session_state.get("wizard_dependents", 0),
        "is_bpl": st.session_state.get("wizard_is_bpl", False),
        "has_ration_card": st.session_state.get("wizard_has_ration_card", False),
        "has_bank_account": st.session_state.get("wizard_has_bank_account", True),
        "land_ownership": st.session_state.get("wizard_land_ownership", False),
        "has_disability": st.session_state.get("wizard_has_disability", False),
        "is_widow": st.session_state.get("wizard_is_widow", False),
        "is_pregnant": st.session_state.get("wizard_is_pregnant", False),
        "is_minority": st.session_state.get("wizard_is_minority", False),
        "is_ex_serviceman": st.session_state.get("wizard_is_ex_serviceman", False),
        "is_ward_of_esm": st.session_state.get("wizard_is_ex_serviceman", False),
        "needs_housing": st.session_state.get("wizard_needs_housing", False),
    }


def validate_current_step() -> bool:
    step = st.session_state.get("form_step", 0)
    if step == 0 and not st.session_state.get("wizard_name", "").strip():
        st.error("Please enter your name before moving ahead.")
        return False
    return True


# ─── Sidebar ──────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Language selection
        languages = app_config.supported_languages
        selected_lang = st.selectbox(
            "Language / भाषा",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=0,
        )
        st.session_state.language = selected_lang
        
        st.divider()
        
        # LLM Provider status
        st.markdown("### 🤖 AI Engine Status")
        provider_display = {
            "groq": "Groq (Llama 3.3 70B)",
            "gemini": "Google Gemini Flash",
        }
        if has_remote_llm():
            provider = llm_config.active_provider.value
            st.success(f"Active: {provider_display.get(provider, provider)}")
            st.caption("Chat mode and detailed guides are enabled.")
        else:
            st.info("Running in rule-based mode.")
            st.caption("Visitors can still use form-based scheme matching. Chat mode and detailed AI guides need a deployed API key.")

            with st.expander("Quick Setup for local testing"):
                api_key = st.text_input("Groq API Key (free)", type="password")
                if api_key:
                    llm_config.groq_api_key = api_key
                    st.success("Key set for this session.")
                    st.rerun()
        
        st.divider()
        
        # Stats
        st.markdown("### 📊 Database Stats")
        st.metric("Total Schemes", f"{get_scheme_count()}+")
        st.metric("Verified Fresh", f"{get_verified_scheme_count()}")
        st.caption("Central & State Government Schemes")

        st.divider()

        st.markdown("### 🛠️ Admin")
        st.session_state.admin_view = st.checkbox(
            "Show freshness dashboard",
            value=st.session_state.admin_view,
            help="View verified, pending, and overdue scheme records.",
        )

        st.divider()
        
        # Mode toggle
        st.markdown("### 📝 Input Mode")
        mode_options = ["📋 Form (Quick)"]
        if has_remote_llm():
            mode_options.append("💬 Chat (Conversational)")

        mode = st.radio(
            "How to provide your details:",
            mode_options,
            index=0,
            help="Form mode is faster. Chat mode lets you describe your situation naturally."
        )
        st.session_state.chat_mode = "Chat" in mode
        
        st.divider()
        
        if st.button("🔄 Start Over", use_container_width=True):
            reset_app()
            st.rerun()
        
        st.divider()
        st.caption("Built with ❤️ by YojanaGPT")
        st.caption("Verify all information at official government portals.")


# ─── Header ───────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🇮🇳 YojanaGPT</h1>
        <p>Your AI-Powered Government Scheme Navigator</p>
        <p style="font-size: 0.9rem; color: #666;">
            Discover government schemes you're eligible for • Get document guidance • Step-by-step application help
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_admin_dashboard():
    """Show a lightweight review dashboard for scheme freshness."""
    report = build_review_report()

    st.markdown("### 🛠️ Scheme Freshness Dashboard")
    st.caption("Use this view to track which schemes are verified, overdue, or still pending manual review.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", report["total"])
    col2.metric("Verified", len(report["verified"]))
    col3.metric("Pending Review", len(report["needs_review"]))
    col4.metric("Overdue", len(report["overdue"]))

    if report["overdue"]:
        st.warning("Some verified schemes are past their review date. Re-check those records before relying on them heavily.")
    else:
        st.success("No verified schemes are currently overdue.")

    tab_verified, tab_pending, tab_overdue, tab_archived = st.tabs(["Verified", "Pending Review", "Overdue", "Archived"])

    with tab_verified:
        preview = report["verified"][:20]
        if not preview:
            st.info("No verified schemes found.")
        else:
            for item in preview:
                st.markdown(
                    f"**{item['id']}**  \n"
                    f"{item['name']}  \n"
                    f"Last verified: `{item['last_verified_on']}` | Review due: `{item['review_due_on']}` | Source: `{item['source']}`"
                )

    with tab_pending:
        if not report["needs_review"]:
            st.info("No pending scheme reviews.")
        else:
            for item in report["needs_review"]:
                st.markdown(f"**{item['id']}**  \n{item['name']}  \nStatus: `{item['status']}`")

    with tab_overdue:
        if not report["overdue"]:
            st.info("No overdue verified schemes.")
        else:
            for item in report["overdue"]:
                st.markdown(
                    f"**{item['id']}**  \n"
                    f"{item['name']}  \n"
                    f"Review due: `{item['review_due_on']}` | Source: `{item['source']}`"
                )

    with tab_archived:
        archived = report.get("archived", [])
        if not archived:
            st.info("No archived schemes.")
        else:
            for item in archived:
                st.markdown(
                    f"**{item['id']}**  \n"
                    f"{item['name']}  \n"
                    f"Status: `{item['status']}` | Source: `{item['source']}`"
                )


# ─── Form Input Mode ─────────────────────────────────────────────────
def render_form_input():
    st.markdown("### Tell us about yourself")
    st.caption("Use the guided form below. It is designed to feel lighter on mobile and more practical for first-time users.")
    render_onboarding_panel()

    if not has_remote_llm():
        st.info("This deployment is currently using rule-based matching, so the guided form is the most reliable option for public visitors.")

    current_step = st.session_state.get("form_step", 0)
    step_labels = [f"{idx + 1}. {title}" for idx, (title, _) in enumerate(FORM_STEPS)]
    selected_label = st.radio(
        "Progress",
        options=step_labels,
        index=current_step,
        horizontal=True,
        key="wizard_step_selector",
    )
    current_step = step_labels.index(selected_label)
    st.session_state.form_step = current_step
    step_title, step_copy = FORM_STEPS[current_step]

    st.markdown(
        f"""
        <div class="wizard-shell">
            <div class="wizard-step-title">Step {current_step + 1}: {step_title}</div>
            <div class="wizard-step-copy">{step_copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if current_step == 0:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name *", key="wizard_name", placeholder="Enter your full name")
            st.number_input("Age *", min_value=0, max_value=120, step=1, key="wizard_age", value=25)
            st.selectbox("Gender *", ["Male", "Female", "Other"], key="wizard_gender")
        with col2:
            st.selectbox(
                "Marital Status",
                ["Single", "Married", "Widowed", "Divorced", "Separated"],
                key="wizard_marital_status",
            )
            st.number_input("Number of Dependents", min_value=0, max_value=20, step=1, key="wizard_dependents", value=0)

    elif current_step == 1:
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("State *", INDIAN_STATES, key="wizard_state")
            st.selectbox("Area Type *", ["Rural", "Urban"], key="wizard_area_type")
        with col2:
            st.selectbox("Category *", ["General", "OBC", "SC", "ST", "EWS"], key="wizard_category")
            st.selectbox(
                "Annual Family Income (approx) *",
                ["Below Rs 1 Lakh", "Rs 1 - 2.5 Lakh", "Rs 2.5 - 5 Lakh", "Rs 5 - 10 Lakh", "Rs 10 - 18 Lakh", "Above Rs 18 Lakh"],
                key="wizard_income",
            )

    elif current_step == 2:
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                "Occupation *",
                [
                    "Student", "Farmer", "Unemployed", "Self Employed",
                    "Salaried Employee", "Daily Wage Worker", "Homemaker",
                    "Street Vendor", "Construction Worker", "Domestic Worker",
                    "Retired", "Other",
                ],
                key="wizard_occupation",
            )
        with col2:
            st.selectbox(
                "Education Level",
                ["No Formal Education", "Below Class 10", "Class 10", "Class 12", "ITI / Diploma", "Undergraduate", "Postgraduate", "PhD"],
                key="wizard_education",
            )

    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("BPL Card Holder", key="wizard_is_bpl")
            st.checkbox("Has Ration Card", key="wizard_has_ration_card")
            st.checkbox("Has Bank Account", key="wizard_has_bank_account", value=True)
            st.checkbox("Owns Agricultural Land", key="wizard_land_ownership")
        with col2:
            st.checkbox("Person with Disability", key="wizard_has_disability")
            st.checkbox("Widow", key="wizard_is_widow")
            st.checkbox("Pregnant / Lactating Mother", key="wizard_is_pregnant")
        with col3:
            st.checkbox("Belongs to Minority Community", key="wizard_is_minority")
            st.checkbox("Ex-Serviceman / Ward of Ex-Serviceman", key="wizard_is_ex_serviceman")
            st.checkbox("Needs Housing / No Pucca House", key="wizard_needs_housing")

    progress_value = int(((current_step + 1) / len(FORM_STEPS)) * 100)
    st.progress(progress_value, text=f"Form completion step {current_step + 1} of {len(FORM_STEPS)}")

    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])
    with nav_col1:
        if current_step > 0 and st.button("Back", use_container_width=True):
            st.session_state.form_step = current_step - 1
            st.rerun()
    with nav_col2:
        if current_step < len(FORM_STEPS) - 1 and st.button("Next", use_container_width=True, type="secondary"):
            if validate_current_step():
                st.session_state.form_step = current_step + 1
                st.rerun()
    with nav_col3:
        if current_step == len(FORM_STEPS) - 1 and st.button("Find My Schemes", use_container_width=True, type="primary"):
            profile = get_form_profile()
            if not profile["name"]:
                st.error("Please enter your name before searching.")
                return
            st.session_state.stage = "processing"
            st.session_state.profile_submitted = True
            process_profile(profile)


# ─── Chat Input Mode ─────────────────────────────────────────────────
def render_chat_input():
    if not has_remote_llm():
        st.warning("Chat mode needs a deployed Groq or Gemini API key. Please use the form mode for now.")
        return

    st.markdown("### 💬 Chat with YojanaGPT")
    st.caption("Tell us about yourself in your own words. I'll ask follow-up questions to understand your situation better.")
    
    orch = get_orchestrator()
    
    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="🇮🇳" if msg["role"] == "assistant" else "👤"):
            st.write(msg["content"])
    
    # Initial greeting
    if not st.session_state.chat_messages:
        greeting = "Namaste! 🙏 I'm YojanaGPT, your government scheme navigator. I'll help you discover all the government schemes you're eligible for.\n\nLet's start — what's your name?"
        st.session_state.chat_messages.append({"role": "assistant", "content": greeting})
        with st.chat_message("assistant", avatar="🇮🇳"):
            st.write(greeting)
    
    # Chat input
    user_input = st.chat_input("Type your response here...")
    
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        
        with st.chat_message("assistant", avatar="🇮🇳"):
            with st.spinner("Thinking..."):
                try:
                    response = orch.chat_for_profile(user_input)
                except Exception as e:
                    logger.error(f"Chat error: {e}", exc_info=True)
                    response = (
                        "I couldn't continue the chat right now because the AI provider is unavailable. "
                        "Please try again in a moment, add a valid API key in deployment secrets, "
                        "or use the form mode instead."
                    )
                st.write(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Check if profile is complete
        if orch.is_profile_complete:
            st.success("✅ Great! I have all the information I need. Let me find schemes for you!")
            if st.button("🔍 Find My Schemes", type="primary", use_container_width=True):
                st.session_state.stage = "processing"
                process_profile(orch.profile)


# ─── Processing ───────────────────────────────────────────────────────
def process_profile(profile: dict):
    """Run the full pipeline and display results."""
    orch = get_orchestrator()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Submit profile
        status_text.markdown("**📋 Analyzing your profile...**")
        progress_bar.progress(10)
        orch.submit_profile_form(profile)
        time.sleep(0.3)
        
        # Step 2: Run matching
        status_text.markdown("**🔍 Searching across 35+ government schemes...**")
        progress_bar.progress(30)
        matches = orch.run_matching()
        
        # Step 3: Document advisory
        status_text.markdown("**📄 Preparing document guidance...**")
        progress_bar.progress(60)
        docs = orch.run_document_advisory()
        
        # Step 4: Application summaries
        status_text.markdown("**📝 Generating application instructions...**")
        progress_bar.progress(80)
        apps = orch.run_application_guidance()
        
        # Step 5: Compile results
        status_text.markdown("**✅ Preparing your personalized report...**")
        progress_bar.progress(100)
        
        st.session_state.results = {
            "profile": profile,
            "matches": matches,
            "documents": docs,
            "applications": apps,
            "remote_llm_available": has_remote_llm(),
        }
        st.session_state.stage = "results"
        
        progress_bar.empty()
        status_text.empty()
        st.rerun()
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        logger.error(f"Processing error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API key settings in the sidebar and try again.")
        st.session_state.stage = "input"


# ─── Results Display ──────────────────────────────────────────────────
def render_results():
    results = st.session_state.results
    if not results:
        st.session_state.stage = "input"
        st.rerun()
        return
    
    profile = results["profile"]
    matches = results["matches"]
    documents = results["documents"]
    remote_llm_available = results.get("remote_llm_available", False)
    
    # ── Summary Stats ─────────────────────────────────────────────
    st.markdown(f"### 🎯 Results for {profile.get('name', 'You')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    eligible_count = len([m for m in matches if m.get("status") == "ELIGIBLE"])
    likely_count = len([m for m in matches if m.get("status") == "LIKELY_ELIGIBLE"])
    high_priority = len([m for m in matches if m.get("priority") == "HIGH"])
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(matches)}</div>
            <div class="stat-label">Schemes Matched</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #4caf50;">{eligible_count}</div>
            <div class="stat-label">Eligible</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #ff9800;">{likely_count}</div>
            <div class="stat-label">Likely Eligible</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #2196f3;">{high_priority}</div>
            <div class="stat-label">High Priority</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    if not remote_llm_available:
        st.info("These results were generated in rule-based mode. Add `GROQ_API_KEY` or `GEMINI_API_KEY` to Streamlit secrets if you want richer AI-written guidance for all visitors.")

    st.success("Only schemes marked as currently verified are shown in results. Older records stay hidden until reviewed.")

    due_soon = []
    overdue = []
    for match in matches:
        scheme = match.get("full_scheme") or get_scheme_by_id(match.get("id", ""))
        if not scheme or not scheme.get("review_due_on"):
            continue
        try:
            due_date = datetime.strptime(scheme["review_due_on"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if due_date < date.today():
            overdue.append(scheme["name"])
        elif (due_date - date.today()).days <= 7:
            due_soon.append(f"{scheme['name']} ({scheme['review_due_on']})")

    if overdue:
        st.warning("Some matched schemes are past their review date: " + ", ".join(overdue))
    elif due_soon:
        st.warning("Some matched schemes need review soon: " + ", ".join(due_soon))

    total_likely_have = sum(len(d.get("documents", {}).get("likely_have", [])) for d in documents)
    total_need_to_get = sum(len(d.get("documents", {}).get("need_to_get", [])) for d in documents)
    top_match_name = matches[0].get("name") if matches else "your top verified scheme"
    st.markdown(
        f"""
        <div class="trust-panel">
            <h4>Recommended Next Move</h4>
            <p>Start with <strong>{top_match_name}</strong>, open the official source before applying, and prepare {total_need_to_get} document(s) you may still need. We estimate you already have {total_likely_have} likely-ready document(s) across your current matches.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        priority_filter = st.selectbox("Priority", ["All", "High only", "High + Medium"], index=0)
    with filter_col2:
        available_categories = sorted(
            {((m.get("full_scheme") or {}).get("category", "")).title() for m in matches if (m.get("full_scheme") or {}).get("category")}
        )
        category_filter = st.selectbox("Category", ["All"] + available_categories, index=0)
    with filter_col3:
        sort_by = st.selectbox("Sort", ["Confidence", "Priority", "Fewer documents", "Alphabetical"], index=0)

    def get_doc_totals(match: dict) -> int:
        info = next((d for d in documents if d.get("scheme_id") == match.get("id")), None)
        if not info:
            return 999
        docs_data = info.get("documents", {})
        return len(docs_data.get("likely_have", [])) + len(docs_data.get("need_to_get", []))

    filtered_matches = []
    for match in matches:
        scheme = match.get("full_scheme") or get_scheme_by_id(match.get("id", ""))
        if not scheme:
            continue
        category_name = scheme.get("category", "").title()
        if priority_filter == "High only" and match.get("priority") != "HIGH":
            continue
        if priority_filter == "High + Medium" and match.get("priority") not in {"HIGH", "MEDIUM"}:
            continue
        if category_filter != "All" and category_name != category_filter:
            continue
        filtered_matches.append(match)

    if sort_by == "Confidence":
        filtered_matches.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    elif sort_by == "Priority":
        priority_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        filtered_matches.sort(key=lambda x: (priority_rank.get(x.get("priority", "LOW"), 3), -x.get("confidence", 0)))
    elif sort_by == "Fewer documents":
        filtered_matches.sort(key=get_doc_totals)
    else:
        filtered_matches.sort(key=lambda x: x.get("name", x.get("id", "")))

    matches = filtered_matches
    eligible_count = len([m for m in matches if m.get("status") == "ELIGIBLE"])
    likely_count = len([m for m in matches if m.get("status") == "LIKELY_ELIGIBLE"])
    high_priority = len([m for m in matches if m.get("priority") == "HIGH"])

    visible_col1, visible_col2, visible_col3 = st.columns(3)
    visible_col1.metric("Visible Matches", len(matches))
    visible_col2.metric("Visible Eligible", eligible_count)
    visible_col3.metric("Visible High Priority", high_priority)
    
    # ── PDF Download ──────────────────────────────────────────────
    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])
    with col_dl2:
        if st.button("📥 Download Full PDF Report", use_container_width=True, type="primary"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_path = generate_report(
                        profile=profile,
                        matched_schemes=matches,
                        document_advice=documents,
                    )
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇️ Click to Download PDF",
                            data=f.read(),
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as e:
                    st.error(f"PDF generation error: {e}")
    
    st.divider()
    
    # ── Filter Tabs ───────────────────────────────────────────────
    tab_all, tab_eligible, tab_high = st.tabs([
        f"📋 All Schemes ({len(matches)})",
        f"✅ Eligible ({eligible_count})",
        f"🔥 High Priority ({high_priority})",
    ])
    
    def render_scheme_list(scheme_list, tab_prefix="all"):
        if not scheme_list:
            st.info("No verified schemes match your current filters. Try changing the category, priority, or sort options above.")
            return
        
        for i, match in enumerate(scheme_list):
            scheme = match.get("full_scheme") or get_scheme_by_id(match.get("id", ""))
            if not scheme:
                continue
            
            confidence = match.get("confidence", 0)
            status = match.get("status", "LIKELY_ELIGIBLE")
            priority = match.get("priority", "MEDIUM")
            
            with st.expander(
                f"{'🟢' if confidence >= 80 else '🟡' if confidence >= 60 else '🔵'} "
                f"**{scheme['name']}** — {status.replace('_', ' ')} ({confidence}%)"
            ):
                # Header with badges
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{scheme['ministry']}** • {scheme.get('type', 'N/A')}")
                    st.markdown(get_verification_badge(scheme), unsafe_allow_html=True)
                with col_b:
                    priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "⚪"}.get(priority, "⚪")
                    st.markdown(f"{priority_emoji} **{priority} Priority**")
                
                # Confidence bar
                color = get_confidence_color(confidence)
                st.markdown(f"""
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence}%; background: {color};"></div>
                </div>
                <small>Confidence: {confidence}%</small>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Benefits
                benefits = scheme.get("benefits", {})
                st.markdown("**💰 Benefits:**")
                st.info(f"**Amount:** {benefits.get('amount', 'N/A')}\n\n**Frequency:** {benefits.get('frequency', 'N/A')}\n\n**Mode:** {benefits.get('mode', 'N/A')}")
                
                # Description
                st.markdown(f"**📝 Description:** {scheme['description']}")
                if scheme.get("official_source_url"):
                    source_name = scheme.get("source_name", "Official source")
                    st.markdown(f"**🔗 Official Source:** [{source_name}]({scheme['official_source_url']})")
                if scheme.get("review_due_on"):
                    st.caption(f"Review due by: {scheme['review_due_on']}")
                
                # Why eligible
                reasons = match.get("reasons_eligible", [])
                if reasons:
                    st.markdown("**✅ Why you qualify:**")
                    for r in reasons:
                        st.markdown(f"  - {r}")
                
                # To verify
                uncertain = match.get("reasons_uncertain", [])
                if uncertain:
                    st.markdown("**⚠️ To verify:**")
                    for u in uncertain:
                        st.markdown(f"  - {u}")
                
                # Documents needed
                doc_info = None
                for d in documents:
                    if d.get("scheme_id") == scheme["id"]:
                        doc_info = d
                        break
                
                if doc_info:
                    docs_data = doc_info.get("documents", {})
                    st.markdown("**📄 Documents Required:**")
                    total_required = max(1, docs_data.get("total_required", 0))
                    readiness = int((len(docs_data.get("likely_have", [])) / total_required) * 100)
                    st.caption(f"Document readiness score: {readiness}%")
                    
                    col_have, col_need = st.columns(2)
                    with col_have:
                        st.markdown("*Likely have:*")
                        for doc in docs_data.get("likely_have", []):
                            st.markdown(f"  ✅ {doc['name']}")
                    with col_need:
                        st.markdown("*Need to get:*")
                        for doc in docs_data.get("need_to_get", []):
                            st.markdown(f"  📋 {doc['name']} — *{doc['where_to_get']}*")
                
                # Application info
                app = scheme.get("application_process", {})
                st.markdown("**🚀 How to Apply:**")
                app_col1, app_col2 = st.columns(2)
                with app_col1:
                    st.markdown(f"**Mode:** {app.get('mode', 'N/A')}")
                    if app.get("portal"):
                        st.markdown(f"**Portal:** [{app['portal']}]({app['portal']})")
                    if app.get("offline"):
                        st.markdown(f"**Offline:** {app['offline']}")
                with app_col2:
                    if app.get("helpline"):
                        st.markdown(f"**📞 Helpline:** {app['helpline']}")
                    if app.get("processing_time"):
                        st.markdown(f"**⏱️ Processing:** {app['processing_time']}")
                
                # Steps
                steps = app.get("steps", [])
                if steps:
                    if st.checkbox("📝 Show step-by-step instructions", key=f"steps_{tab_prefix}_{scheme['id']}"):
                        for j, step in enumerate(steps, 1):
                            st.markdown(f"**Step {j}.** {step}")
                
                # Detailed guide button
                st.markdown("---")
                if st.button(
                    f"📖 Get Detailed Guide for {scheme['name']}",
                    key=f"guide_{tab_prefix}_{scheme['id']}",
                    disabled=not remote_llm_available,
                ):
                    with st.spinner("Generating detailed guide..."):
                        try:
                            orch = get_orchestrator()
                            guide = orch.get_detailed_application_guide(scheme["id"])
                            st.markdown(guide)
                        except Exception as e:
                            st.error(f"Could not generate guide: {e}")

                if not remote_llm_available:
                    st.caption("Detailed AI guides unlock after you add a hosted API key to the deployment.")
    
    with tab_all:
        render_scheme_list(matches, "all")
    
    with tab_eligible:
        eligible_matches = [m for m in matches if m.get("status") == "ELIGIBLE"]
        render_scheme_list(eligible_matches, "elig")
    
    with tab_high:
        high_matches = [m for m in matches if m.get("priority") == "HIGH"]
        render_scheme_list(high_matches, "high")
    
    # ── Consolidated Document Checklist ───────────────────────────
    st.divider()
    st.markdown("### 📋 Consolidated Document Checklist")
    
    all_docs = {}
    for advice in documents:
        for doc in advice.get("documents", {}).get("all_documents", []):
            doc_name = doc["name"]
            if doc_name not in all_docs:
                all_docs[doc_name] = {
                    "mandatory": doc["mandatory"],
                    "where_to_get": doc["where_to_get"],
                    "schemes": [],
                }
            all_docs[doc_name]["schemes"].append(advice.get("scheme_name", ""))
    
    if all_docs:
        for doc_name, info in all_docs.items():
            status = "🔴 Required" if info["mandatory"] else "🟡 Optional"
            scheme_count = len(info["schemes"])
            st.markdown(f"""
            <div class="doc-item">
                <strong>{doc_name}</strong> {status}<br/>
                <small>📍 Get from: {info['where_to_get']} • Needed for {scheme_count} scheme(s)</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No documents to display.")


# ─── Main App ─────────────────────────────────────────────────────────
def main():
    init_session_state()
    render_sidebar()
    render_header()

    if st.session_state.admin_view:
        render_admin_dashboard()
        return
    
    if st.session_state.stage == "input":
        if st.session_state.chat_mode:
            render_chat_input()
        else:
            render_form_input()
    
    elif st.session_state.stage == "processing":
        st.info("Processing... Please wait.")
    
    elif st.session_state.stage == "results":
        render_results()


if __name__ == "__main__":
    main()
