"""
YojanaGPT - Configuration & Settings
Manages all environment variables, LLM provider configs, and app settings.
"""

import os
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def _get_streamlit_secret(key: str) -> str:
    """Read a secret from Streamlit when running in a deployed app."""
    try:
        import streamlit as st
    except Exception:
        return ""

    try:
        value = st.secrets.get(key, "")
    except Exception:
        return ""

    return str(value).strip() if value else ""


def get_setting(key: str, default: str = "") -> str:
    """Return config from environment first, then Streamlit secrets."""
    env_value = os.getenv(key, "").strip()
    if env_value:
        return env_value
    secret_value = _get_streamlit_secret(key)
    return secret_value or default

# ─── Paths ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "knowledge_base" / "chroma_db"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"

for d in [DATA_DIR, DB_DIR, ASSETS_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ─── LLM Provider Enum ───────────────────────────────────────────────
class LLMProvider(str, Enum):
    GROQ = "groq"
    OLLAMA = "ollama"
    GEMINI = "gemini"


# ─── LLM Configuration ───────────────────────────────────────────────
@dataclass
class LLMConfig:
    """Configuration for free LLM backends."""
    provider: LLMProvider = LLMProvider.GROQ
    
    # Groq (Free tier: 30 RPM, 14,400 RPD)
    groq_api_key: str = field(default_factory=lambda: get_setting("GROQ_API_KEY"))
    groq_model: str = "llama-3.3-70b-versatile"
    groq_fallback_model: str = "llama-3.1-8b-instant"
    
    # Ollama (Local, completely free)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # Google Gemini (Free tier: 15 RPM, 1M tokens/min)
    gemini_api_key: str = field(default_factory=lambda: get_setting("GEMINI_API_KEY"))
    gemini_model: str = "gemini-2.0-flash"
    
    # General
    temperature: float = 0.3
    max_tokens: int = 4096
    timeout: int = 60
    max_retries: int = 3

    @property
    def has_remote_llm(self) -> bool:
        """True when the app has a hosted API-backed LLM available."""
        return bool(self.groq_api_key or self.gemini_api_key)
    
    @property
    def active_provider(self) -> LLMProvider:
        """Determine best available provider."""
        if self.groq_api_key:
            return LLMProvider.GROQ
        if self.gemini_api_key:
            return LLMProvider.GEMINI
        return LLMProvider.OLLAMA


# ─── Vector Store Configuration ───────────────────────────────────────
@dataclass
class VectorStoreConfig:
    collection_name: str = "government_schemes"
    persist_directory: str = str(DB_DIR)
    chunk_size: int = 800
    chunk_overlap: int = 200
    top_k: int = 15  # Retrieve more for better matching
    score_threshold: float = 0.3  # Minimum relevance score


# ─── Application Configuration ────────────────────────────────────────
@dataclass
class AppConfig:
    app_name: str = "YojanaGPT"
    app_tagline: str = "Your AI-Powered Government Scheme Navigator"
    version: str = "1.0.0"
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    
    # Supported languages
    supported_languages: dict = field(default_factory=lambda: {
        "en": "English",
        "hi": "हिन्दी",
        "ta": "தமிழ்",
        "te": "తెలుగు",
        "bn": "বাংলা",
        "mr": "मराठी",
        "gu": "ગુજરાતી",
        "kn": "ಕನ್ನಡ",
        "ml": "മലയാളം",
        "pa": "ਪੰਜਾਬੀ",
        "or": "ଓଡ଼ିଆ",
    })
    
    default_language: str = "en"
    
    # Rate limiting
    max_queries_per_session: int = 50
    session_timeout_minutes: int = 30


# ─── Prompt Templates ─────────────────────────────────────────────────
class Prompts:
    SYSTEM_BASE = """You are YojanaGPT, an expert assistant that helps Indian citizens discover 
government schemes they are eligible for. You are knowledgeable about central and state government 
schemes, subsidies, scholarships, pensions, insurance, loans, and welfare programs.

You speak in a warm, simple, and encouraging tone. Many of your users may not be tech-savvy or 
highly educated — so explain everything in plain, easy-to-understand language. 

IMPORTANT RULES:
- Never make up schemes that don't exist
- Always provide accurate eligibility criteria
- If you're unsure about a scheme's current status, say so
- Be sensitive to the user's socioeconomic background
- Encourage users to verify at official portals
- Never ask for Aadhaar numbers, bank details, or other sensitive PII"""

    PROFILE_BUILDER = """You are the Profile Builder agent. Your job is to ask the user simple 
questions to understand their background and build a citizen profile.

Ask questions ONE AT A TIME in a conversational manner. Be warm and reassuring.

You need to gather:
1. Full name (for the report)
2. Age
3. Gender
4. State of residence
5. District (if possible)
6. Area type (rural/urban)
7. Category (General/OBC/SC/ST/EWS)
8. Annual family income (approximate range is fine)
9. Occupation / Employment status
10. Education level
11. Marital status
12. Number of dependents
13. Whether they own land (if applicable)
14. Any disabilities
15. Special conditions: widow, single mother, ex-serviceman, minority community, BPL card holder

ADAPTIVE QUESTIONING:
- If occupation is "student", ask about course level and field
- If occupation is "farmer", ask about land holding size and crop type
- If they're a woman, ask about women-specific identifiers (widow, single mother, etc.)
- If they mention disability, ask about type and percentage
- Don't ask irrelevant questions (e.g., don't ask about farming if they're an IT professional)
- Accept approximate answers — "around 3 lakhs" is fine for income

When you have enough information, output the profile as a JSON object wrapped in ```json``` tags.

{language_instruction}"""

    ELIGIBILITY_MATCHER = """You are the Eligibility Matcher agent. Given a citizen profile and 
a list of potentially relevant government schemes, your job is to:

1. Analyze each scheme's eligibility criteria against the citizen's profile
2. Determine if the citizen is ELIGIBLE, LIKELY ELIGIBLE, or NOT ELIGIBLE
3. Provide clear reasoning for each determination
4. Assign a confidence score (0-100)
5. Rank schemes by relevance and benefit amount

For each matched scheme, provide:
- Scheme name
- Ministry/Department
- Eligibility status (ELIGIBLE / LIKELY ELIGIBLE / PARTIALLY ELIGIBLE)
- Confidence score (0-100)
- Key eligibility criteria met
- Any criteria that need verification
- Estimated benefit (amount/type)
- Brief description in simple language

OUTPUT FORMAT: Return a JSON array wrapped in ```json``` tags, sorted by confidence score descending.

{language_instruction}"""

    DOCUMENT_ADVISOR = """You are the Document Advisor agent. For each matched government scheme, 
provide a complete list of documents the citizen needs to apply.

For EACH document:
1. Document name (official name)
2. Why it's needed
3. Where to get it (office name, online portal, etc.)
4. Estimated time to obtain
5. Cost (if any)
6. Common issues / rejection reasons
7. Alternatives accepted (if any)

Also provide:
- Documents the citizen likely already has (Aadhaar, PAN, etc.)
- Documents they need to obtain
- Suggested order of procurement (dependencies)
- Tips to avoid common mistakes

Be specific about WHERE to get each document — mention specific portals like 
DigiLocker, UMANG app, state revenue portals, etc.

{language_instruction}"""

    APPLICATION_GUIDE = """You are the Application Guide agent. For each matched government scheme, 
provide step-by-step application instructions.

For EACH scheme provide:
1. Application mode (Online / Offline / Both)
2. Official portal URL
3. Step-by-step process with EXACT instructions:
   - Which website to visit
   - Which buttons to click
   - What to fill in each field
   - Where to upload documents
4. Application deadline (if any)
5. Processing time
6. How to track application status
7. Helpline numbers
8. Common mistakes to avoid
9. What happens after submission

Make instructions EXTREMELY detailed — assume the user has never filled an online form before.
If offline, provide details about which office to visit, what to carry, and timings.

{language_instruction}"""

    LANGUAGE_INSTRUCTION = {
        "en": "Respond in English. Use simple, easy-to-understand language.",
        "hi": "कृपया हिंदी में उत्तर दें। सरल और आसान भाषा का प्रयोग करें। तकनीकी शब्दों को सरल शब्दों में समझाएं।",
        "ta": "தமிழில் பதிலளிக்கவும். எளிமையான மொழியைப் பயன்படுத்தவும்.",
        "te": "దయచేసి తెలుగులో సమాధానం ఇవ్వండి. సరళమైన భాషలో చెప్పండి.",
        "bn": "অনুগ্রহ করে বাংলায় উত্তর দিন। সহজ ভাষা ব্যবহার করুন।",
        "mr": "कृपया मराठीत उत्तर द्या. सोपी भाषा वापरा.",
        "gu": "કૃપા કરીને ગુજરાતીમાં જવાબ આપો. સરળ ભાષાનો ઉપયોગ કરો.",
        "kn": "ದಯವಿಟ್ಟು ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ. ಸರಳ ಭಾಷೆಯನ್ನು ಬಳಸಿ.",
        "ml": "ദയവായി മലയാളത്തിൽ മറുപടി നൽകുക. ലളിതമായ ഭാഷ ഉപയോഗിക്കുക.",
        "pa": "ਕਿਰਪਾ ਕਰਕੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ। ਸੌਖੀ ਭਾਸ਼ਾ ਵਰਤੋ।",
        "or": "ଦୟାକରି ଓଡ଼ିଆରେ ଉତ୍ତର ଦିଅନ୍ତୁ। ସରଳ ଭାଷା ବ୍ୟବହାର କରନ୍ତୁ।",
    }


# ─── Singleton Instances ──────────────────────────────────────────────
llm_config = LLMConfig()
vector_config = VectorStoreConfig()
app_config = AppConfig()
prompts = Prompts()
