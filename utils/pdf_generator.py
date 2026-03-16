"""
YojanaGPT - PDF Report Generator
Generates a professional PDF report of matched schemes for citizens.
"""

import os
import json
from datetime import datetime
from fpdf import FPDF
from config.settings import ASSETS_DIR, app_config
from data.schemes_database import get_scheme_by_id


class YojanaGPTReport(FPDF):
    """Custom PDF report for YojanaGPT results."""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        # Use built-in font that supports basic characters
        self.add_page()
    
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(25, 65, 120)
        self.cell(0, 10, "YojanaGPT - Government Scheme Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(8)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"YojanaGPT | Page {self.page_no()}/{{nb}} | Verify at official portals before applying", align="C")
    
    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(25, 65, 120)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
    
    def sub_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    
    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        # Handle encoding - replace non-latin characters with ASCII equivalents
        safe_text = text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 5, safe_text)
        self.ln(2)
    
    def key_value(self, key: str, value: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.cell(55, 6, f"{key}:")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        safe_value = str(value).encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 6, safe_value, new_x="LMARGIN", new_y="NEXT")
    
    def badge(self, text: str, color: tuple = (46, 125, 50)):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        w = self.get_string_width(text) + 8
        self.cell(w, 7, text, fill=True, align="C")
        self.set_text_color(0, 0, 0)
    
    def separator(self):
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)


def generate_report(profile: dict, matched_schemes: list, 
                    document_advice: list, output_path: str = None) -> str:
    """
    Generate a comprehensive PDF report.
    
    Args:
        profile: Citizen profile dict
        matched_schemes: List of matched scheme results
        document_advice: List of document advisory results
        output_path: Custom output path (optional)
    
    Returns:
        Path to generated PDF file
    """
    pdf = YojanaGPTReport()
    pdf.alias_nb_pages()
    
    # ── Profile Summary ───────────────────────────────────────────
    pdf.section_title("Your Profile Summary")
    
    profile_display = {
        "Name": profile.get("name", "N/A"),
        "Age": profile.get("age", "N/A"),
        "Gender": profile.get("gender", "N/A").title(),
        "State": profile.get("state", "N/A").replace("_", " ").title(),
        "Area": profile.get("area_type", "N/A").title(),
        "Category": profile.get("category", "N/A").upper(),
        "Annual Income": f"Rs. {profile.get('income', 'N/A'):,}" if isinstance(profile.get('income'), (int, float)) else "N/A",
        "Occupation": profile.get("occupation", "N/A").replace("_", " ").title(),
        "Education": profile.get("education_level", "N/A").replace("_", " ").title(),
    }
    
    for key, value in profile_display.items():
        pdf.key_value(key, str(value))
    
    # Special conditions
    special = []
    if profile.get("is_bpl"): special.append("BPL Card Holder")
    if profile.get("is_widow"): special.append("Widow")
    if profile.get("is_pregnant"): special.append("Pregnant")
    if profile.get("has_disability"): special.append("Person with Disability")
    if profile.get("is_minority"): special.append("Minority Community")
    if profile.get("is_ex_serviceman"): special.append("Ex-Serviceman")
    if profile.get("land_ownership"): special.append("Land Owner")
    
    if special:
        pdf.key_value("Special Conditions", ", ".join(special))
    
    pdf.ln(5)
    pdf.separator()
    
    # ── Matched Schemes ───────────────────────────────────────────
    pdf.section_title(f"Matched Schemes ({len(matched_schemes)} found)")
    
    if not matched_schemes:
        pdf.body_text("No schemes matched your profile. Please verify your details and try again.")
    
    for i, match in enumerate(matched_schemes, 1):
        scheme = match.get("full_scheme") or get_scheme_by_id(match.get("id", ""))
        if not scheme:
            continue
        
        # Scheme header with confidence badge
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(25, 65, 120)
        pdf.cell(0, 8, f"{i}. {scheme['name']}", new_x="LMARGIN", new_y="NEXT")
        
        confidence = match.get("confidence", 0)
        status = match.get("status", "LIKELY_ELIGIBLE")
        
        if confidence >= 80:
            pdf.badge(f"  {status} ({confidence}%)  ", (46, 125, 50))
        elif confidence >= 60:
            pdf.badge(f"  {status} ({confidence}%)  ", (255, 152, 0))
        else:
            pdf.badge(f"  {status} ({confidence}%)  ", (158, 158, 158))
        
        priority = match.get("priority", "MEDIUM")
        pdf.cell(5)
        pdf.badge(f" {priority} PRIORITY ", (63, 81, 181) if priority == "HIGH" else (158, 158, 158))
        pdf.ln(8)
        
        # Scheme details
        pdf.key_value("Ministry", scheme.get("ministry", "N/A"))
        pdf.key_value("Type", scheme.get("type", "N/A"))
        
        benefits = scheme.get("benefits", {})
        pdf.key_value("Benefit Amount", benefits.get("amount", "N/A"))
        pdf.key_value("Frequency", benefits.get("frequency", "N/A"))
        
        # Why eligible
        reasons = match.get("reasons_eligible", [])
        if reasons:
            pdf.sub_title("Why you qualify:")
            for reason in reasons:
                safe_reason = str(reason).encode('latin-1', 'replace').decode('latin-1')
                pdf.body_text(f"  * {safe_reason}")
        
        # What to verify
        uncertain = match.get("reasons_uncertain", [])
        if uncertain:
            pdf.sub_title("To verify:")
            for item in uncertain:
                safe_item = str(item).encode('latin-1', 'replace').decode('latin-1')
                pdf.body_text(f"  ? {safe_item}")
        
        # Application info
        app = scheme.get("application_process", {})
        if app:
            pdf.key_value("Apply", app.get("mode", "N/A"))
            if app.get("portal"):
                pdf.key_value("Portal", app["portal"])
            if app.get("helpline"):
                pdf.key_value("Helpline", app["helpline"])
            if app.get("processing_time"):
                pdf.key_value("Processing Time", app["processing_time"])
        
        pdf.ln(3)
        pdf.separator()
    
    # ── Document Checklist ────────────────────────────────────────
    if document_advice:
        pdf.add_page()
        pdf.section_title("Document Checklist")
        pdf.body_text("Below is a consolidated list of documents you need. Many documents are common across schemes.")
        
        # Consolidated unique documents
        all_docs = {}
        for advice in document_advice:
            for doc in advice.get("documents", {}).get("all_documents", []):
                doc_name = doc["name"]
                if doc_name not in all_docs:
                    all_docs[doc_name] = {
                        "mandatory": doc["mandatory"],
                        "where_to_get": doc["where_to_get"],
                        "schemes": []
                    }
                all_docs[doc_name]["schemes"].append(advice["scheme_name"])
        
        for doc_name, doc_info in all_docs.items():
            status = "REQUIRED" if doc_info["mandatory"] else "OPTIONAL"
            safe_name = doc_name.encode('latin-1', 'replace').decode('latin-1')
            safe_where = doc_info["where_to_get"].encode('latin-1', 'replace').decode('latin-1')
            
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 6, f"[ ] {safe_name} ({status})", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"    Get from: {safe_where}", new_x="LMARGIN", new_y="NEXT")
            
            scheme_names = ", ".join(doc_info["schemes"][:3])
            safe_schemes = scheme_names.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 5, f"    Needed for: {safe_schemes}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
    
    # ── Disclaimer ────────────────────────────────────────────────
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4, (
        "DISCLAIMER: This report is generated by YojanaGPT for informational purposes only. "
        "Eligibility assessments are based on the information you provided and may not be 100% accurate. "
        "Please verify all details at the official government portals or nearest government office before applying. "
        "Scheme details, benefits, and eligibility criteria are subject to change by the government. "
        "YojanaGPT is not affiliated with any government body."
    ))
    
    # Save PDF
    if not output_path:
        name = profile.get("name", "citizen").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"YojanaGPT_Report_{name}_{timestamp}.pdf"
    
    pdf.output(output_path)
    return output_path
