"""
YojanaGPT - Government Schemes Database
Contains 50+ real Indian government schemes with complete details.
Each scheme has: eligibility criteria, benefits, required documents, application process.
"""

from copy import deepcopy
from datetime import date, datetime

SCHEMES_DATABASE = [
    # ═══════════════════════════════════════════════════════════════════
    # AGRICULTURE & FARMER WELFARE
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "PM-KISAN",
        "name": "PM-KISAN Samman Nidhi",
        "name_hi": "प्रधानमंत्री किसान सम्मान निधि",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "category": "agriculture",
        "type": "Direct Benefit Transfer",
        "description": "Income support of ₹6,000 per year to all landholding farmer families across the country in three equal installments of ₹2,000 each every four months.",
        "description_hi": "सभी भूमिधारी किसान परिवारों को प्रति वर्ष ₹6,000 की आय सहायता, तीन समान किस्तों में।",
        "benefits": {
            "amount": "₹6,000 per year",
            "frequency": "3 installments of ₹2,000 every 4 months",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["farmer"],
            "land_ownership": True,
            "max_land_holding": None,
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "exclusions": [
                "Institutional landholders",
                "Former and present holders of constitutional posts",
                "Former and present Ministers / State Ministers",
                "Serving or retired officers and employees of Central/State Government Ministries",
                "All persons who paid Income Tax in last assessment year",
                "Professionals like Doctors, Engineers, Lawyers, CAs registered with professional bodies",
                "All superannuated/retired pensioners whose monthly pension is ₹10,000 or more"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre or post office"},
            {"name": "Land ownership records (Khatauni/Khasra/Patta)", "mandatory": True, "where_to_get": "Revenue Department / Tehsil office / Bhulekh portal"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Any bank branch"},
            {"name": "Mobile number linked with Aadhaar", "mandatory": True, "where_to_get": "Aadhaar centre"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://pmkisan.gov.in",
            "offline": "Common Service Centre (CSC) or local agriculture office",
            "steps": [
                "Visit pmkisan.gov.in",
                "Click on 'New Farmer Registration'",
                "Select Rural or Urban farmer",
                "Enter Aadhaar number and captcha",
                "Fill in personal details, bank details, land details",
                "Upload required documents",
                "Submit and note registration number"
            ],
            "helpline": "155261 / 011-24300606",
            "processing_time": "2-3 months for first installment"
        },
        "tags": ["farmer", "agriculture", "income_support", "direct_benefit", "central"]
    },
    {
        "id": "PMFBY",
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "name_hi": "प्रधानमंत्री फसल बीमा योजना",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "category": "agriculture",
        "type": "Insurance",
        "description": "Crop insurance scheme providing financial support to farmers suffering crop loss due to natural calamities, pests, and diseases. Premium is very low — 2% for Kharif, 1.5% for Rabi, 5% for commercial/horticultural crops.",
        "benefits": {
            "amount": "Up to full sum insured based on crop and area",
            "frequency": "Per season per crop",
            "mode": "Direct Bank Transfer on claim"
        },
        "eligibility": {
            "occupation": ["farmer"],
            "land_ownership": None,
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Both loanee and non-loanee farmers", "Sharecroppers and tenant farmers also eligible"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Land records / Lease agreement", "mandatory": True, "where_to_get": "Revenue office"},
            {"name": "Bank account passbook", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Sowing certificate from agriculture officer", "mandatory": True, "where_to_get": "Block agriculture office"},
            {"name": "Crop area details", "mandatory": True, "where_to_get": "Patwari / Revenue office"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://pmfby.gov.in",
            "offline": "Bank branch, CSC, or agriculture office",
            "steps": [
                "Visit pmfby.gov.in or nearest bank branch",
                "Fill crop insurance application form",
                "Provide land and crop details",
                "Pay premium amount (subsidised)",
                "Get insurance policy document"
            ],
            "helpline": "011-23382012",
            "processing_time": "Claims settled within 2 months of harvest"
        },
        "tags": ["farmer", "agriculture", "insurance", "crop", "central"]
    },
    {
        "id": "KCC",
        "name": "Kisan Credit Card",
        "name_hi": "किसान क्रेडिट कार्ड",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "category": "agriculture",
        "type": "Credit",
        "description": "Provides farmers with affordable credit for agricultural needs. Credit limit based on land holding, crop pattern, and scale of finance. Interest rate as low as 4% per annum (with prompt repayment).",
        "benefits": {
            "amount": "Up to ₹3 lakh at 4% interest (with subvention)",
            "frequency": "Annual renewal",
            "mode": "Credit Card / Loan account"
        },
        "eligibility": {
            "occupation": ["farmer"],
            "land_ownership": None,
            "min_age": 18,
            "max_age": 75,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Owner cultivators", "Tenant farmers", "Sharecroppers", "SHG members", "Fishermen and animal husbandry farmers also eligible under revised KCC"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Land ownership proof / Tenancy certificate", "mandatory": True, "where_to_get": "Revenue office"},
            {"name": "Passport size photographs", "mandatory": True, "where_to_get": "Photo studio"},
            {"name": "PAN Card (for limit above ₹50,000)", "mandatory": False, "where_to_get": "NSDL/UTIITSL portal"},
            {"name": "Crop sowing proof", "mandatory": True, "where_to_get": "Agriculture office"}
        ],
        "application_process": {
            "mode": "Offline primarily, Online for some banks",
            "portal": "Respective bank websites",
            "offline": "Nearest bank branch (SBI, PNB, cooperative banks)",
            "steps": [
                "Visit nearest bank branch",
                "Ask for Kisan Credit Card application form",
                "Fill in personal, land, and crop details",
                "Submit documents",
                "Bank will verify land records",
                "Credit limit sanctioned within 15 days",
                "KCC card issued"
            ],
            "helpline": "Bank-specific helplines",
            "processing_time": "15 days to 1 month"
        },
        "tags": ["farmer", "agriculture", "credit", "loan", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # EDUCATION & SCHOLARSHIPS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "NSP-PRE-MATRIC-SC",
        "name": "Pre-Matric Scholarship for SC Students",
        "name_hi": "अनुसूचित जाति के छात्रों के लिए प्री-मैट्रिक छात्रवृत्ति",
        "ministry": "Ministry of Social Justice & Empowerment",
        "category": "education",
        "type": "Scholarship",
        "description": "Scholarships for SC students studying in Class 9 and 10 to reduce dropout rates. Covers maintenance allowance and ad hoc grant for books and stationery.",
        "benefits": {
            "amount": "₹3,500-₹6,250 per annum (day scholars-hostellers)",
            "frequency": "Annual",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["student"],
            "education_level": ["class_9", "class_10"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["sc"],
            "area_type": ["rural", "urban"],
            "max_income": 250000,
            "states": "all"
        },
        "required_documents": [
            {"name": "Caste Certificate (SC)", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "School Enrollment Certificate", "mandatory": True, "where_to_get": "School"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Previous year marksheet", "mandatory": True, "where_to_get": "School"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://scholarships.gov.in",
            "steps": [
                "Visit National Scholarship Portal (scholarships.gov.in)",
                "Register with mobile number and email",
                "Login and select 'Pre-Matric Scholarship for SC'",
                "Fill personal, academic, and bank details",
                "Upload required documents",
                "Submit and note application ID",
                "Institute will verify and forward"
            ],
            "helpline": "0120-6619540",
            "processing_time": "2-4 months"
        },
        "tags": ["student", "education", "scholarship", "sc", "pre_matric", "central"]
    },
    {
        "id": "NSP-POST-MATRIC-SC",
        "name": "Post-Matric Scholarship for SC Students",
        "name_hi": "अनुसूचित जाति के छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "ministry": "Ministry of Social Justice & Empowerment",
        "category": "education",
        "type": "Scholarship",
        "description": "Financial assistance to SC students studying at post-matriculation or post-secondary stage. Covers tuition fees, maintenance allowance, and other expenses.",
        "benefits": {
            "amount": "₹2,300-₹12,000+ per annum based on course and hostel status",
            "frequency": "Annual",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["student"],
            "education_level": ["class_11", "class_12", "undergraduate", "postgraduate", "phd", "diploma", "iti"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["sc"],
            "area_type": ["rural", "urban"],
            "max_income": 250000,
            "states": "all"
        },
        "required_documents": [
            {"name": "Caste Certificate (SC)", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Admission letter / Bonafide certificate", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank passbook", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Fee receipt", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Previous year marksheet", "mandatory": True, "where_to_get": "Board / University"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://scholarships.gov.in",
            "steps": [
                "Visit National Scholarship Portal (scholarships.gov.in)",
                "Register or login with existing credentials",
                "Select 'Post-Matric Scholarship for SC Students'",
                "Fill complete academic and personal details",
                "Upload scanned documents",
                "Submit application",
                "Track status on portal"
            ],
            "helpline": "0120-6619540",
            "processing_time": "3-6 months"
        },
        "tags": ["student", "education", "scholarship", "sc", "post_matric", "central"]
    },
    {
        "id": "NSP-POST-MATRIC-OBC",
        "name": "Post-Matric Scholarship for OBC Students",
        "name_hi": "ओबीसी छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "ministry": "Ministry of Social Justice & Empowerment",
        "category": "education",
        "type": "Scholarship",
        "description": "Scholarship for OBC students studying at post-matric level in recognized institutions.",
        "benefits": {
            "amount": "Tuition fee + ₹750-₹1,000 per month maintenance",
            "frequency": "Annual",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["student"],
            "education_level": ["class_11", "class_12", "undergraduate", "postgraduate", "phd", "diploma", "iti"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["obc"],
            "area_type": ["rural", "urban"],
            "max_income": 100000,
            "states": "all"
        },
        "required_documents": [
            {"name": "OBC Certificate (non-creamy layer)", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Admission proof", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://scholarships.gov.in",
            "steps": [
                "Register on National Scholarship Portal",
                "Select 'Post-Matric Scholarship for OBC'",
                "Fill in all required details",
                "Upload documents",
                "Submit for institute verification"
            ],
            "helpline": "0120-6619540",
            "processing_time": "3-6 months"
        },
        "tags": ["student", "education", "scholarship", "obc", "post_matric", "central"]
    },
    {
        "id": "NSP-MINORITY",
        "name": "Post-Matric Scholarship for Minorities",
        "name_hi": "अल्पसंख्यक छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "ministry": "Ministry of Minority Affairs",
        "category": "education",
        "type": "Scholarship",
        "description": "Scholarship for students belonging to minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) studying at post-matric level.",
        "benefits": {
            "amount": "Up to ₹10,000 per annum + maintenance allowance",
            "frequency": "Annual",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["student"],
            "education_level": ["class_11", "class_12", "undergraduate", "postgraduate", "diploma"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": 200000,
            "states": "all",
            "special_conditions": ["Must belong to notified minority community"]
        },
        "required_documents": [
            {"name": "Minority community self-declaration", "mandatory": True, "where_to_get": "Self-attested"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Admission proof", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Previous marksheet", "mandatory": True, "where_to_get": "Board/University"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://scholarships.gov.in",
            "steps": [
                "Register on National Scholarship Portal",
                "Select 'Post-Matric Scholarship Scheme for Minorities'",
                "Fill application with academic and personal details",
                "Upload documents",
                "Submit application"
            ],
            "helpline": "0120-6619540",
            "processing_time": "3-6 months"
        },
        "tags": ["student", "education", "scholarship", "minority", "central"]
    },
    {
        "id": "PM-VIDYALAXMI",
        "name": "PM Vidyalaxmi - Education Loan",
        "name_hi": "प्रधानमंत्री विद्यालक्ष्मी - शिक्षा ऋण",
        "ministry": "Ministry of Education",
        "category": "education",
        "type": "Loan / Financial Assistance",
        "description": "Education loan portal connecting students with multiple banks. Collateral-free loans up to ₹7.5 lakh for economically weaker sections. Interest subsidy available for loans up to ₹10 lakh.",
        "benefits": {
            "amount": "Loans from ₹4 lakh to ₹1 crore+ based on course",
            "frequency": "One-time disbursement per year",
            "mode": "Directly to institution"
        },
        "eligibility": {
            "occupation": ["student"],
            "education_level": ["undergraduate", "postgraduate", "phd", "diploma"],
            "min_age": 18,
            "max_age": 35,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must have admission in recognized institution"]
        },
        "required_documents": [
            {"name": "Admission letter", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Fee structure letter", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Income proof of co-applicant", "mandatory": True, "where_to_get": "Employer/SDM office"},
            {"name": "Academic records", "mandatory": True, "where_to_get": "Previous institution"},
            {"name": "Collateral documents (for loans > ₹7.5L)", "mandatory": False, "where_to_get": "Revenue office"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://www.vidyalakshmi.co.in",
            "steps": [
                "Register on Vidya Lakshmi Portal",
                "Fill Common Education Loan Application Form (CELAF)",
                "Search and apply to multiple banks in one go",
                "Upload documents",
                "Banks will review and contact you",
                "Select best offer and complete formalities"
            ],
            "helpline": "1800-11-0025",
            "processing_time": "15-30 days"
        },
        "tags": ["student", "education", "loan", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # WOMEN & CHILD WELFARE
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "PMMVY",
        "name": "Pradhan Mantri Matru Vandana Yojana",
        "name_hi": "प्रधानमंत्री मातृ वंदना योजना",
        "ministry": "Ministry of Women & Child Development",
        "category": "women",
        "type": "Direct Benefit Transfer",
        "description": "Cash incentive of ₹5,000 (₹6,000 for second girl child) to pregnant women and lactating mothers for the first living child, to partially compensate for wage loss during pregnancy.",
        "benefits": {
            "amount": "₹5,000 in 3 installments (₹6,000 for 2nd girl child)",
            "frequency": "One-time per pregnancy",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 19,
            "max_age": None,
            "gender": "female",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Pregnant women or lactating mothers", "For first and second living child only", "Government employees not eligible"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank passbook", "mandatory": True, "where_to_get": "Bank"},
            {"name": "MCP Card (Mother & Child Protection Card)", "mandatory": True, "where_to_get": "Anganwadi centre / PHC"},
            {"name": "Pregnancy registration proof", "mandatory": True, "where_to_get": "Hospital / PHC"},
            {"name": "LMP date certificate", "mandatory": True, "where_to_get": "Hospital / PHC"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://pmmvy.wcd.gov.in",
            "offline": "Anganwadi Centre or nearest health facility",
            "steps": [
                "Visit nearest Anganwadi centre or PHC",
                "Register pregnancy and get MCP card",
                "Fill PMMVY application form",
                "Submit Aadhaar and bank details",
                "1st installment after pregnancy registration",
                "2nd installment after at least one ANC checkup",
                "3rd installment after child birth registration and first cycle of vaccination"
            ],
            "helpline": "181 (Women Helpline)",
            "processing_time": "1-2 months per installment"
        },
        "tags": ["women", "pregnancy", "maternity", "health", "direct_benefit", "central"]
    },
    {
        "id": "SUKANYA-SAMRIDDHI",
        "name": "Sukanya Samriddhi Yojana",
        "name_hi": "सुकन्या समृद्धि योजना",
        "ministry": "Ministry of Finance",
        "category": "women",
        "type": "Savings Scheme",
        "description": "Government-backed savings scheme for girl children with one of the highest interest rates (around 8.2%). Tax benefits under Section 80C. Account can be opened from birth till age 10.",
        "benefits": {
            "amount": "~8.2% interest per annum (tax-free returns)",
            "frequency": "Interest compounded annually",
            "mode": "Savings account"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 0,
            "max_age": 10,
            "gender": "female",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Girl child up to 10 years", "Maximum 2 accounts per family", "Parent/guardian opens the account"]
        },
        "required_documents": [
            {"name": "Girl child's birth certificate", "mandatory": True, "where_to_get": "Hospital / Municipal office"},
            {"name": "Parent's Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Parent's PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Address proof", "mandatory": True, "where_to_get": "Various"},
            {"name": "Passport size photos (parent & child)", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": None,
            "offline": "Any post office or authorized bank branch",
            "steps": [
                "Visit nearest post office or bank (SBI, PNB, BOB etc.)",
                "Ask for Sukanya Samriddhi Yojana account opening form",
                "Fill in details of girl child and parent/guardian",
                "Submit documents",
                "Deposit minimum ₹250 (maximum ₹1.5 lakh per year)",
                "Get passbook for the account"
            ],
            "helpline": "1800-266-6868",
            "processing_time": "Same day"
        },
        "tags": ["women", "girl_child", "savings", "investment", "tax_benefit", "central"]
    },
    {
        "id": "UJJWALA",
        "name": "Pradhan Mantri Ujjwala Yojana",
        "name_hi": "प्रधानमंत्री उज्ज्वला योजना",
        "ministry": "Ministry of Petroleum & Natural Gas",
        "category": "women",
        "type": "Subsidy",
        "description": "Free LPG connections to women from BPL households. Includes ₹1,600 financial assistance for the LPG connection and the first refill is free.",
        "benefits": {
            "amount": "Free LPG connection + ₹1,600 assistance + first free refill",
            "frequency": "One-time",
            "mode": "LPG connection + bank transfer"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "female",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must be from BPL household", "No existing LPG connection in household", "Woman member of household"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "BPL ration card / SECC data proof", "mandatory": True, "where_to_get": "Food & Civil Supplies office"},
            {"name": "Bank account passbook", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Passport size photo", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Offline primarily",
            "portal": "https://www.pmujjwalayojana.com",
            "offline": "Nearest LPG distributor (HP, Bharat, Indane)",
            "steps": [
                "Visit nearest LPG distributor",
                "Fill KYC form and Ujjwala application",
                "Submit BPL proof and Aadhaar",
                "Submit bank account details",
                "Connection delivered within 7-15 days"
            ],
            "helpline": "1800-266-6696",
            "processing_time": "7-15 days"
        },
        "tags": ["women", "lpg", "bpl", "cooking", "energy", "central"]
    },
    {
        "id": "FREE-SILAI-MACHINE",
        "name": "Free Silai Machine Yojana",
        "name_hi": "फ्री सिलाई मशीन योजना",
        "ministry": "Ministry of Women & Child Development (State implementations vary)",
        "category": "women",
        "type": "In-Kind Benefit",
        "description": "Free sewing machines to economically weak women so they can start tailoring as a livelihood. Implemented in several states with varying criteria.",
        "benefits": {
            "amount": "Free sewing machine",
            "frequency": "One-time",
            "mode": "Direct delivery"
        },
        "eligibility": {
            "occupation": ["homemaker", "unemployed", "self_employed"],
            "min_age": 20,
            "max_age": 40,
            "gender": "female",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": 120000,
            "states": ["rajasthan", "madhya_pradesh", "maharashtra", "karnataka", "uttar_pradesh", "gujarat", "haryana", "bihar", "chhattisgarh"],
            "special_conditions": ["Economically weak women", "Widows and disabled women given priority"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Age proof", "mandatory": True, "where_to_get": "Birth certificate / School certificate"},
            {"name": "Disability certificate (if applicable)", "mandatory": False, "where_to_get": "Government hospital"},
            {"name": "Widow certificate (if applicable)", "mandatory": False, "where_to_get": "SDM office"},
            {"name": "Passport size photo", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": None,
            "offline": "Nearest Gram Panchayat / Nagar Palika / Women & Child Development office",
            "steps": [
                "Visit nearest government office (Gram Panchayat for rural, Nagar Palika for urban)",
                "Obtain application form",
                "Fill in personal and income details",
                "Submit with documents",
                "Selection based on priority criteria",
                "Sewing machine distributed at camp/event"
            ],
            "helpline": "State Women Helpline 181",
            "processing_time": "1-3 months"
        },
        "tags": ["women", "livelihood", "self_employment", "skill", "state"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # HEALTH & INSURANCE
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "AYUSHMAN-BHARAT",
        "name": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (AB-PMJAY)",
        "name_hi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
        "ministry": "Ministry of Health & Family Welfare",
        "category": "health",
        "type": "Health Insurance",
        "description": "World's largest health insurance scheme providing ₹5 lakh per family per year for secondary and tertiary hospitalization. Covers pre and post hospitalization expenses. Cashless treatment at empanelled hospitals.",
        "benefits": {
            "amount": "₹5,00,000 per family per year",
            "frequency": "Annual (renewable)",
            "mode": "Cashless treatment at empanelled hospitals"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "Family must be listed in SECC 2011 database",
                "Rural: Based on deprivation criteria (kutcha house, no adult member, female-headed, disabled member, landless, manual scavenger, destitute, bonded labour, tribal)",
                "Urban: Based on occupation (rag picker, street vendor, domestic worker, construction worker, sanitation worker, etc.)",
                "All ration card holders with priority households"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Ration Card / SECC listed proof", "mandatory": True, "where_to_get": "Food & Civil Supplies office"},
            {"name": "Family ID / household details", "mandatory": True, "where_to_get": "Aadhaar or local body"},
            {"name": "Mobile number", "mandatory": True, "where_to_get": "—"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://pmjay.gov.in",
            "offline": "Ayushman Mitra at empanelled hospitals or CSC centre",
            "steps": [
                "Check eligibility at mera.pmjay.gov.in by entering mobile/ration card number",
                "If eligible, visit nearest empanelled hospital or CSC",
                "Get Ayushman Card created (free)",
                "Carry Aadhaar and ration card",
                "E-card generated with photo and details",
                "Show card at any empanelled hospital for cashless treatment"
            ],
            "helpline": "14555",
            "processing_time": "Ayushman card created same day; treatment as needed"
        },
        "tags": ["health", "insurance", "hospital", "bpl", "family", "central"]
    },
    {
        "id": "PMSBY",
        "name": "Pradhan Mantri Suraksha Bima Yojana",
        "name_hi": "प्रधानमंत्री सुरक्षा बीमा योजना",
        "ministry": "Ministry of Finance",
        "category": "health",
        "type": "Accident Insurance",
        "description": "Accident insurance cover of ₹2 lakh for accidental death or total disability, ₹1 lakh for partial disability — all for just ₹20 per year, auto-debited from bank account.",
        "benefits": {
            "amount": "₹2 lakh (death/total disability), ₹1 lakh (partial)",
            "frequency": "Annual premium of ₹20",
            "mode": "Claim to bank on incident"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": 70,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must have a savings bank account", "Must have Aadhaar linked to bank account"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account (savings)", "mandatory": True, "where_to_get": "Any bank"},
            {"name": "Consent form for auto-debit", "mandatory": True, "where_to_get": "Bank"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "Through net-banking or bank app",
            "offline": "Bank branch",
            "steps": [
                "Visit bank branch or login to net banking",
                "Ask for PMSBY enrollment form",
                "Fill in nominee details",
                "Give auto-debit consent for ₹20/year",
                "Premium auto-deducted on 1st June every year"
            ],
            "helpline": "1800-180-1111",
            "processing_time": "Instant enrollment"
        },
        "tags": ["insurance", "accident", "affordable", "central"]
    },
    {
        "id": "PMJJBY",
        "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana",
        "name_hi": "प्रधानमंत्री जीवन ज्योति बीमा योजना",
        "ministry": "Ministry of Finance",
        "category": "health",
        "type": "Life Insurance",
        "description": "Life insurance cover of ₹2 lakh for death due to any reason, for a premium of just ₹436 per year. Available through bank accounts.",
        "benefits": {
            "amount": "₹2 lakh death cover",
            "frequency": "Annual premium ₹436",
            "mode": "Claim to nominee on death"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": 50,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must have savings bank account", "Aadhaar linked to account"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account (savings)", "mandatory": True, "where_to_get": "Any bank"},
            {"name": "Nominee details", "mandatory": True, "where_to_get": "Self"},
            {"name": "Self-declaration of good health", "mandatory": True, "where_to_get": "Self"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "Through net-banking or bank app",
            "offline": "Bank branch",
            "steps": [
                "Visit bank branch or login to net banking",
                "Enroll in PMJJBY",
                "Fill nominee details and health declaration",
                "Give auto-debit consent for ₹436/year"
            ],
            "helpline": "1800-180-1111",
            "processing_time": "Instant"
        },
        "tags": ["insurance", "life", "affordable", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # HOUSING
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "PMAY-G",
        "name": "Pradhan Mantri Awas Yojana - Gramin",
        "name_hi": "प्रधानमंत्री आवास योजना - ग्रामीण",
        "ministry": "Ministry of Rural Development",
        "category": "housing",
        "type": "Housing Assistance",
        "description": "Financial assistance for construction of pucca houses for rural poor. Assistance of ₹1.20 lakh in plains and ₹1.30 lakh in hilly/difficult areas, along with MGNREGA convergence for 90-95 days of unskilled labour.",
        "benefits": {
            "amount": "₹1.20 lakh (plains) / ₹1.30 lakh (hilly areas) + toilet + MGNREGA wages",
            "frequency": "One-time (3 installments)",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["sc", "st", "obc", "ews", "general"],
            "area_type": ["rural"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "Must not have a pucca house",
                "Selected from SECC 2011 data based on housing deprivation",
                "Priority: houseless, kutcha house, one room with kutcha wall/roof",
                "Beneficiary list prepared by Gram Sabha"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "SECC data / BPL proof", "mandatory": True, "where_to_get": "Gram Panchayat"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Land ownership proof / NOC for construction", "mandatory": True, "where_to_get": "Revenue office / Gram Panchayat"},
            {"name": "MGNREGA Job Card", "mandatory": False, "where_to_get": "Gram Panchayat"}
        ],
        "application_process": {
            "mode": "Offline primarily",
            "portal": "https://pmayg.nic.in",
            "offline": "Gram Panchayat / Block Development Office",
            "steps": [
                "Check if name is in PMAY-G waiting list at pmayg.nic.in",
                "If listed, Gram Panchayat will notify you",
                "Submit documents to Gram Panchayat",
                "After approval, 1st installment released to start construction",
                "Geo-tagged photos of construction progress required",
                "2nd and 3rd installments based on milestones",
                "House must be completed within 12 months"
            ],
            "helpline": "1800-11-6446",
            "processing_time": "Selection by Gram Sabha, 3-6 months to start"
        },
        "tags": ["housing", "rural", "construction", "bpl", "central"]
    },
    {
        "id": "PMAY-U",
        "name": "Pradhan Mantri Awas Yojana - Urban",
        "name_hi": "प्रधानमंत्री आवास योजना - शहरी",
        "ministry": "Ministry of Housing & Urban Affairs",
        "category": "housing",
        "type": "Housing Subsidy",
        "description": "Interest subsidy on home loans for urban poor and middle class. Subsidy ranges from ₹2.35 lakh to ₹2.67 lakh depending on income category. Also supports in-situ slum rehabilitation and affordable housing projects.",
        "benefits": {
            "amount": "Interest subsidy of ₹2.35 lakh - ₹2.67 lakh on home loan",
            "frequency": "One-time subsidy on loan",
            "mode": "Credited to loan account (reduces EMI)"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["urban"],
            "max_income": 1800000,
            "states": "all",
            "special_conditions": [
                "EWS: Income up to ₹3 lakh — subsidy 6.5% on ₹6 lakh for 20 years",
                "LIG: Income ₹3-6 lakh — subsidy 6.5% on ₹6 lakh for 20 years",
                "MIG-I: Income ₹6-12 lakh — subsidy 4% on ₹9 lakh for 20 years",
                "MIG-II: Income ₹12-18 lakh — subsidy 3% on ₹12 lakh for 20 years",
                "Must not own a pucca house anywhere in India",
                "Priority to women ownership (EWS/LIG)"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Income proof / salary slips", "mandatory": True, "where_to_get": "Employer / CA certificate"},
            {"name": "PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Bank statements (6 months)", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Property documents", "mandatory": True, "where_to_get": "Builder / Registration office"},
            {"name": "Self-declaration of no pucca house", "mandatory": True, "where_to_get": "Self-attested"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://pmaymis.gov.in",
            "offline": "Bank or housing finance company",
            "steps": [
                "Apply for home loan at any bank/HFC",
                "Mention PMAY-CLSS subsidy at time of application",
                "Bank verifies eligibility",
                "Subsidy amount credited to loan account upfront",
                "Monthly EMI reduces accordingly"
            ],
            "helpline": "1800-11-6163",
            "processing_time": "Subsidy credited within 3-4 months of loan disbursement"
        },
        "tags": ["housing", "urban", "loan", "subsidy", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # EMPLOYMENT & SKILL DEVELOPMENT
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "MGNREGA",
        "name": "Mahatma Gandhi National Rural Employment Guarantee Act",
        "name_hi": "महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी अधिनियम",
        "ministry": "Ministry of Rural Development",
        "category": "employment",
        "type": "Employment Guarantee",
        "description": "Guarantees 100 days of wage employment per year to every rural household whose adult members volunteer to do unskilled manual work. Legal right to employment — if not provided within 15 days, unemployment allowance must be paid.",
        "benefits": {
            "amount": "100 days guaranteed employment at state minimum wage (₹200-350/day)",
            "frequency": "Per financial year",
            "mode": "Bank/Post office transfer"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must be resident of rural area", "Willing to do unskilled manual work"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Passport size photo", "mandatory": True, "where_to_get": "Photo studio"},
            {"name": "Bank/Post Office account", "mandatory": True, "where_to_get": "Bank/Post office"},
            {"name": "Address proof / Ration card", "mandatory": True, "where_to_get": "Local body"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://nrega.nic.in",
            "offline": "Gram Panchayat office",
            "steps": [
                "Visit Gram Panchayat office",
                "Apply for Job Card with photo and Aadhaar",
                "Job Card issued within 15 days (free)",
                "Apply for work when needed",
                "Work must be provided within 15 days",
                "Wages paid within 15 days of work completion"
            ],
            "helpline": "1800-345-22244",
            "processing_time": "Job Card: 15 days; Work: within 15 days of demand"
        },
        "tags": ["employment", "rural", "unskilled", "guarantee", "central"]
    },
    {
        "id": "PMKVY",
        "name": "Pradhan Mantri Kaushal Vikas Yojana",
        "name_hi": "प्रधानमंत्री कौशल विकास योजना",
        "ministry": "Ministry of Skill Development & Entrepreneurship",
        "category": "employment",
        "type": "Skill Training",
        "description": "Free skill training and certification in over 300 job roles across sectors like IT, healthcare, construction, automotive, etc. Training duration 150-300 hours. Includes placement assistance.",
        "benefits": {
            "amount": "Free training + ₹8,000 reward on certification + placement support",
            "frequency": "One-time per training course",
            "mode": "Training + certificate + cash reward"
        },
        "eligibility": {
            "occupation": ["unemployed", "student", "dropout"],
            "min_age": 15,
            "max_age": 45,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Class 10 pass preferred but not mandatory for all courses", "Indian citizen with Aadhaar"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Educational certificates (if any)", "mandatory": False, "where_to_get": "School/Board"},
            {"name": "Passport size photos", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://www.pmkvyofficial.org",
            "offline": "Nearest PMKVY Training Centre",
            "steps": [
                "Visit pmkvyofficial.org or Skill India portal",
                "Search for training centres near you",
                "Choose a skill course (IT, healthcare, etc.)",
                "Visit centre and enroll",
                "Complete training (150-300 hours)",
                "Take assessment exam",
                "Get government-certified certificate",
                "Receive ₹8,000 reward and placement support"
            ],
            "helpline": "088000-55555",
            "processing_time": "Training: 2-6 months"
        },
        "tags": ["employment", "skill", "training", "youth", "certification", "central"]
    },
    {
        "id": "MUDRA",
        "name": "Pradhan Mantri MUDRA Yojana",
        "name_hi": "प्रधानमंत्री मुद्रा योजना",
        "ministry": "Ministry of Finance",
        "category": "employment",
        "type": "Business Loan",
        "description": "Collateral-free loans up to ₹10 lakh for small and micro enterprises. Three categories: Shishu (up to ₹50,000), Kishore (₹50,000-₹5 lakh), and Tarun (₹5 lakh-₹10 lakh). No collateral required.",
        "benefits": {
            "amount": "Up to ₹10 lakh (Shishu/Kishore/Tarun)",
            "frequency": "Renewable loan",
            "mode": "Bank loan disbursement"
        },
        "eligibility": {
            "occupation": ["self_employed", "entrepreneur", "small_business"],
            "min_age": 18,
            "max_age": 65,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "Non-corporate, non-farm small/micro enterprises",
                "Manufacturing, trading, service sector",
                "Existing business or new venture",
                "No collateral needed"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Business plan / project report", "mandatory": True, "where_to_get": "Self-prepared"},
            {"name": "Identity & address proof", "mandatory": True, "where_to_get": "Various"},
            {"name": "Business registration (if existing)", "mandatory": False, "where_to_get": "District Industries Centre"},
            {"name": "Bank statements (6 months)", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Quotation of machines/equipment (if applicable)", "mandatory": False, "where_to_get": "Supplier"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://www.mudra.org.in",
            "offline": "Any bank branch, NBFC, or MFI",
            "steps": [
                "Prepare a business plan",
                "Visit nearest bank branch",
                "Ask for MUDRA loan application",
                "Fill in business and personal details",
                "Submit business plan and documents",
                "Bank evaluates and sanctions loan",
                "Loan disbursed to account"
            ],
            "helpline": "1800-180-1111",
            "processing_time": "7-15 days for Shishu, 15-30 days for Kishore/Tarun"
        },
        "tags": ["employment", "business", "loan", "entrepreneur", "msme", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # PENSION & SOCIAL SECURITY
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "PMVVY",
        "name": "Pradhan Mantri Vaya Vandana Yojana",
        "name_hi": "प्रधानमंत्री वय वंदना योजना",
        "ministry": "Ministry of Finance",
        "category": "pension",
        "type": "Pension",
        "description": "Pension scheme for senior citizens providing assured pension based on investment. Operated through LIC. Fixed pension for 10 years on a one-time investment.",
        "benefits": {
            "amount": "~7.4% assured return per annum on investment up to ₹15 lakh",
            "frequency": "Monthly/Quarterly/Annual pension choice",
            "mode": "Pension to bank account"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 60,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Age proof", "mandatory": True, "where_to_get": "Birth certificate / passport"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://www.licindia.in",
            "offline": "LIC branch office",
            "steps": [
                "Visit LIC branch or licindia.in",
                "Fill PMVVY application",
                "Choose pension mode (monthly/quarterly/annual)",
                "Make lump sum investment (up to ₹15 lakh)",
                "Pension starts from next cycle"
            ],
            "helpline": "022-68276827",
            "processing_time": "7-10 days"
        },
        "tags": ["pension", "senior_citizen", "investment", "central"]
    },
    {
        "id": "APY",
        "name": "Atal Pension Yojana",
        "name_hi": "अटल पेंशन योजना",
        "ministry": "Ministry of Finance (PFRDA)",
        "category": "pension",
        "type": "Pension",
        "description": "Guaranteed pension scheme for unorganized sector workers. Monthly pension of ₹1,000 to ₹5,000 after age 60 based on contribution amount and joining age. Government co-contributes 50% for eligible subscribers.",
        "benefits": {
            "amount": "₹1,000 to ₹5,000 monthly pension after age 60",
            "frequency": "Monthly after age 60",
            "mode": "Bank account"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": 40,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "Must have a savings bank account",
                "Not a member of any statutory social security scheme",
                "Not an income tax payer"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account (savings)", "mandatory": True, "where_to_get": "Any bank"},
            {"name": "Mobile number", "mandatory": True, "where_to_get": "—"},
            {"name": "Nominee details", "mandatory": True, "where_to_get": "Self"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://enps.nsdl.com/eNPS/NationalPensionSystem.html",
            "offline": "Any bank branch",
            "steps": [
                "Visit bank branch where you have savings account",
                "Fill APY registration form",
                "Choose pension amount (₹1,000-₹5,000/month)",
                "Give auto-debit consent",
                "Monthly contribution auto-debited from account"
            ],
            "helpline": "1800-110-708",
            "processing_time": "Instant enrollment"
        },
        "tags": ["pension", "unorganized_sector", "retirement", "central"]
    },
    {
        "id": "PM-SYM",
        "name": "Pradhan Mantri Shram Yogi Maan-Dhan",
        "name_hi": "प्रधानमंत्री श्रम योगी मान-धन",
        "ministry": "Ministry of Labour & Employment",
        "category": "pension",
        "type": "Pension",
        "description": "Voluntary and contributory pension scheme for unorganized workers (street vendors, rickshaw pullers, construction workers, domestic workers, etc.). Monthly pension of ₹3,000 after age 60. Government matches the contribution.",
        "benefits": {
            "amount": "₹3,000 monthly pension after age 60 (government matches contribution)",
            "frequency": "Monthly after age 60",
            "mode": "Bank account"
        },
        "eligibility": {
            "occupation": ["unorganized_worker", "street_vendor", "domestic_worker", "construction_worker", "rickshaw_puller"],
            "min_age": 18,
            "max_age": 40,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": 180000,
            "states": "all",
            "special_conditions": [
                "Should not be member of EPFO/ESIC/NPS",
                "Not an income tax payer"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank/Post Office savings account", "mandatory": True, "where_to_get": "Bank/Post office"},
            {"name": "Mobile number", "mandatory": True, "where_to_get": "—"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://maandhan.in",
            "offline": "CSC centre",
            "steps": [
                "Visit nearest CSC centre with Aadhaar and bank details",
                "Self-enrollment also possible at maandhan.in",
                "Choose monthly contribution based on age (₹55-₹200/month)",
                "Government matches your contribution",
                "Monthly auto-debit from bank account"
            ],
            "helpline": "1800-267-6888",
            "processing_time": "Instant"
        },
        "tags": ["pension", "unorganized_worker", "labour", "central"]
    },
    {
        "id": "NSAP-IGNOAPS",
        "name": "Indira Gandhi National Old Age Pension Scheme",
        "name_hi": "इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना",
        "ministry": "Ministry of Rural Development",
        "category": "pension",
        "type": "Pension",
        "description": "Monthly pension for BPL senior citizens. ₹200/month from Centre for age 60-79, ₹500/month for age 80+. States add their own contribution (total pension varies ₹500-₹2,000 by state).",
        "benefits": {
            "amount": "₹200-₹500/month (Central) + State top-up",
            "frequency": "Monthly",
            "mode": "Bank/Post office"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 60,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must be BPL household", "Must be listed in BPL list"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Age proof", "mandatory": True, "where_to_get": "Birth certificate / voter ID / school certificate"},
            {"name": "BPL ration card", "mandatory": True, "where_to_get": "Food & Civil Supplies office"},
            {"name": "Bank/Post Office account", "mandatory": True, "where_to_get": "Bank/Post office"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://nsap.nic.in",
            "offline": "Gram Panchayat / Block office / District Social Welfare office",
            "steps": [
                "Visit Gram Panchayat (rural) or Municipal office (urban)",
                "Fill pension application form",
                "Submit age proof and BPL proof",
                "Gram Panchayat/Municipality verifies and forwards",
                "Block/District office approves",
                "Pension credited monthly"
            ],
            "helpline": "State Social Welfare helpline",
            "processing_time": "1-3 months"
        },
        "tags": ["pension", "senior_citizen", "bpl", "old_age", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # FINANCIAL INCLUSION
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "PMJDY",
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "name_hi": "प्रधानमंत्री जन धन योजना",
        "ministry": "Ministry of Finance",
        "category": "financial_inclusion",
        "type": "Banking",
        "description": "Zero-balance bank accounts for every unbanked Indian with RuPay debit card, ₹2 lakh accident insurance, and ₹30,000 life cover. The foundation for all DBT (Direct Benefit Transfer) schemes.",
        "benefits": {
            "amount": "Zero-balance account + RuPay card + ₹2 lakh accident cover + ₹30,000 life cover",
            "frequency": "Ongoing",
            "mode": "Bank account + Debit card"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 10,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["No existing bank account", "Even without formal ID, small accounts can be opened"]
        },
        "required_documents": [
            {"name": "Aadhaar Card (or any one ID proof)", "mandatory": True, "where_to_get": "UIDAI / various"},
            {"name": "Passport size photo", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": None,
            "offline": "Any bank branch or Banking Correspondent",
            "steps": [
                "Visit nearest bank branch or Banking Correspondent",
                "Fill account opening form (available in Hindi and English)",
                "Submit Aadhaar card (or any ID/address proof)",
                "Submit photo",
                "Account opened same day",
                "RuPay debit card issued"
            ],
            "helpline": "1800-11-0001",
            "processing_time": "Same day"
        },
        "tags": ["banking", "financial_inclusion", "zero_balance", "central"]
    },
    {
        "id": "STAND-UP-INDIA",
        "name": "Stand Up India",
        "name_hi": "स्टैंड अप इंडिया",
        "ministry": "Ministry of Finance",
        "category": "employment",
        "type": "Business Loan",
        "description": "Loans between ₹10 lakh and ₹1 crore for SC/ST and women entrepreneurs for setting up greenfield enterprises in manufacturing, services, or trading sector.",
        "benefits": {
            "amount": "₹10 lakh to ₹1 crore",
            "frequency": "One-time loan, repayment up to 7 years",
            "mode": "Bank loan"
        },
        "eligibility": {
            "occupation": ["entrepreneur", "self_employed"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["sc", "st"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "SC/ST or Women entrepreneur",
                "For greenfield enterprise (new business)",
                "51% shareholding must be with SC/ST or woman",
                "Should not have defaulted on any bank loan"
            ],
            "gender_specific": "Also available to women of all categories"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Caste Certificate (for SC/ST)", "mandatory": True, "where_to_get": "SDM office"},
            {"name": "Business plan / Project report", "mandatory": True, "where_to_get": "Self / DICC help"},
            {"name": "ITR for last 2 years", "mandatory": False, "where_to_get": "CA / IT portal"},
            {"name": "Business registration proof", "mandatory": True, "where_to_get": "ROC / DICC"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://www.standupmitra.in",
            "offline": "Bank branch",
            "steps": [
                "Register on standupmitra.in",
                "Fill in business details and loan requirement",
                "Connect with nearest bank branch through portal",
                "Submit documents and business plan",
                "Bank evaluates and sanctions",
                "SIDBI provides handholding support"
            ],
            "helpline": "1800-180-1111",
            "processing_time": "15-30 days"
        },
        "tags": ["employment", "business", "loan", "sc", "st", "women", "entrepreneur", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # DISABILITY WELFARE
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "ADIP",
        "name": "Assistance to Disabled Persons (ADIP) Scheme",
        "name_hi": "विकलांग व्यक्तियों को सहायता (एडिप) योजना",
        "ministry": "Ministry of Social Justice & Empowerment",
        "category": "disability",
        "type": "Assistive Devices",
        "description": "Free or subsidized assistive devices and aids (artificial limbs, wheelchairs, hearing aids, braille kits, etc.) for persons with disabilities.",
        "benefits": {
            "amount": "Free assistive devices + travel expenses + accommodation during fitting",
            "frequency": "Once every 3 years",
            "mode": "In-kind (devices) + cash for travel"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": 250000,
            "states": "all",
            "special_conditions": ["40% or more disability", "Must have disability certificate"]
        },
        "required_documents": [
            {"name": "Disability Certificate (40%+)", "mandatory": True, "where_to_get": "Government hospital medical board"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Passport size photos", "mandatory": True, "where_to_get": "Photo studio"},
            {"name": "Prescription for specific aid", "mandatory": True, "where_to_get": "Government hospital doctor"}
        ],
        "application_process": {
            "mode": "Offline primarily",
            "portal": None,
            "offline": "District Disability Rehabilitation Centre / ALIMCO / NGOs",
            "steps": [
                "Get disability certificate from government hospital",
                "Contact District Disability Rehabilitation Centre",
                "Apply during ADIP camp (regularly organized)",
                "Get assessed for required aids",
                "Devices fitted and provided free/subsidized"
            ],
            "helpline": "011-23386054",
            "processing_time": "Depends on camp schedule"
        },
        "tags": ["disability", "assistive_devices", "wheelchair", "hearing_aid", "central"]
    },
    {
        "id": "NSAP-IGNDPS",
        "name": "Indira Gandhi National Disability Pension Scheme",
        "name_hi": "इंदिरा गांधी राष्ट्रीय विकलांगता पेंशन योजना",
        "ministry": "Ministry of Rural Development",
        "category": "disability",
        "type": "Pension",
        "description": "Monthly pension for BPL persons with severe or multiple disabilities (80%+). ₹300/month from Centre, states add their contribution.",
        "benefits": {
            "amount": "₹300/month (Central) + State top-up (total ₹500-₹1,500)",
            "frequency": "Monthly",
            "mode": "Bank/Post office"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["80% or more disability", "Must be BPL", "Age 18-79 years"]
        },
        "required_documents": [
            {"name": "Disability Certificate (80%+)", "mandatory": True, "where_to_get": "Government hospital medical board"},
            {"name": "BPL Card / SECC proof", "mandatory": True, "where_to_get": "Food & Civil Supplies office"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://nsap.nic.in",
            "offline": "District Social Welfare office / Gram Panchayat",
            "steps": [
                "Get disability certificate from government hospital",
                "Visit Social Welfare office or Gram Panchayat",
                "Fill pension application form",
                "Submit disability and BPL proof",
                "District office verifies and approves"
            ],
            "helpline": "State Social Welfare helpline",
            "processing_time": "1-3 months"
        },
        "tags": ["disability", "pension", "bpl", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # RURAL DEVELOPMENT & SANITATION
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "SBM",
        "name": "Swachh Bharat Mission (Gramin) - Individual Household Latrine",
        "name_hi": "स्वच्छ भारत मिशन (ग्रामीण) - व्यक्तिगत शौचालय",
        "ministry": "Ministry of Jal Shakti",
        "category": "sanitation",
        "type": "Construction Assistance",
        "description": "Financial incentive of ₹12,000 for construction of individual household latrines for BPL/eligible families in rural areas.",
        "benefits": {
            "amount": "₹12,000 incentive for toilet construction",
            "frequency": "One-time",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must not have a toilet at home", "Must be in rural area", "Priority to BPL, SC/ST, small/marginal farmers, landless labourers, physically handicapped, women-headed households"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "BPL Card / Ration card", "mandatory": True, "where_to_get": "Food & Civil Supplies"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Photo of constructed toilet (for 2nd installment)", "mandatory": True, "where_to_get": "Self"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://swachhbharatmission.gov.in",
            "offline": "Gram Panchayat",
            "steps": [
                "Apply at Gram Panchayat",
                "Gram Panchayat verifies eligibility",
                "1st installment released for construction",
                "Construct toilet",
                "Submit photo proof to Gram Panchayat",
                "2nd installment released after verification"
            ],
            "helpline": "1800-180-4005",
            "processing_time": "1-2 months"
        },
        "tags": ["sanitation", "toilet", "rural", "hygiene", "central"]
    },
    {
        "id": "PMGSY",
        "name": "PM Garib Kalyan Anna Yojana",
        "name_hi": "प्रधानमंत्री गरीब कल्याण अन्न योजना",
        "ministry": "Ministry of Consumer Affairs, Food & Public Distribution",
        "category": "food_security",
        "type": "Food Distribution",
        "description": "Free food grains to eligible households under National Food Security Act. 5 kg per person per month of rice/wheat/coarse grains free of cost to around 81 crore beneficiaries.",
        "benefits": {
            "amount": "5 kg free food grains per person per month",
            "frequency": "Monthly",
            "mode": "Through Fair Price Shops (ration shops)"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must have ration card (Priority Household or Antyodaya)", "Covered under NFSA"]
        },
        "required_documents": [
            {"name": "Ration Card (PHH or AAY)", "mandatory": True, "where_to_get": "Food & Civil Supplies office"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": None,
            "offline": "Nearest Fair Price Shop (Ration Shop)",
            "steps": [
                "If you have a ration card, visit your designated Fair Price Shop",
                "Authenticate with Aadhaar biometric",
                "Collect your monthly quota of free grains",
                "If no ration card, apply at Food & Civil Supplies office"
            ],
            "helpline": "1800-11-6555",
            "processing_time": "Monthly collection"
        },
        "tags": ["food", "ration", "bpl", "nfsa", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # ENERGY & UTILITIES
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "SAUBHAGYA",
        "name": "Saubhagya - PM Sahaj Bijli Har Ghar Yojana",
        "name_hi": "सौभाग्य - प्रधानमंत्री सहज बिजली हर घर योजना",
        "ministry": "Ministry of Power",
        "category": "energy",
        "type": "Electricity Connection",
        "description": "Free electricity connections to all un-electrified households in rural and urban areas. For BPL households, the connection is completely free. For other households, connection charges can be paid in 10 monthly installments.",
        "benefits": {
            "amount": "Free electricity connection for BPL (₹500 for others, payable in installments)",
            "frequency": "One-time",
            "mode": "Electricity connection"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must not have an existing electricity connection"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "BPL card (for free connection)", "mandatory": False, "where_to_get": "Food & Civil Supplies"},
            {"name": "Address proof", "mandatory": True, "where_to_get": "Various"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://saubhagya.gov.in",
            "offline": "Local electricity distribution company office",
            "steps": [
                "Contact local electricity distribution company (DISCOM)",
                "Fill connection application form",
                "Submit Aadhaar and address proof",
                "Connection provided within 7 days (rural) / 15 days (urban)"
            ],
            "helpline": "State DISCOM helpline",
            "processing_time": "7-15 days"
        },
        "tags": ["electricity", "energy", "rural", "bpl", "central"]
    },
    {
        "id": "PM-KUSUM",
        "name": "PM-KUSUM (Solar Energy for Farmers)",
        "name_hi": "पीएम-कुसुम (किसानों के लिए सौर ऊर्जा)",
        "ministry": "Ministry of New & Renewable Energy",
        "category": "energy",
        "type": "Subsidy",
        "description": "Solar pump sets and grid-connected solar power plants for farmers. Component A: Solar power plants on barren land. Component B: Standalone solar pumps (up to 7.5 HP). Component C: Solarization of existing grid-connected pumps. 60% subsidy available.",
        "benefits": {
            "amount": "60% subsidy on solar pumps (30% Central + 30% State)",
            "frequency": "One-time",
            "mode": "Subsidy on installation cost"
        },
        "eligibility": {
            "occupation": ["farmer"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must own agricultural land", "Pump capacity based on water source availability"]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Land ownership documents", "mandatory": True, "where_to_get": "Revenue office"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Existing electricity connection proof (for Component C)", "mandatory": False, "where_to_get": "DISCOM"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://pmkusum.mnre.gov.in",
            "offline": "State MNRE office / Agriculture office",
            "steps": [
                "Visit pmkusum.mnre.gov.in",
                "Register and apply for suitable component",
                "Submit land and personal documents",
                "Pay farmer's share (40% of total cost)",
                "MNRE empanelled vendor installs the system"
            ],
            "helpline": "011-24360404",
            "processing_time": "2-3 months"
        },
        "tags": ["farmer", "solar", "energy", "pump", "subsidy", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # DIGITAL & CONNECTIVITY
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "DIGILOCKER",
        "name": "DigiLocker",
        "name_hi": "डिजिलॉकर",
        "ministry": "Ministry of Electronics & IT",
        "category": "digital",
        "type": "Digital Service",
        "description": "Free cloud-based storage for important documents like Aadhaar, PAN, driving license, vehicle registration, academic certificates. Documents from DigiLocker are legally valid and accepted at all government offices.",
        "benefits": {
            "amount": "Free digital document storage (1 GB)",
            "frequency": "Ongoing",
            "mode": "Mobile app / Web portal"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must have Aadhaar number"]
        },
        "required_documents": [
            {"name": "Aadhaar number", "mandatory": True, "where_to_get": "UIDAI"},
            {"name": "Mobile number linked to Aadhaar", "mandatory": True, "where_to_get": "—"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://www.digilocker.gov.in",
            "steps": [
                "Download DigiLocker app or visit digilocker.gov.in",
                "Sign up with Aadhaar number",
                "Verify OTP on registered mobile",
                "Set username and security PIN",
                "Access and store documents instantly"
            ],
            "helpline": "011-24301349",
            "processing_time": "Instant"
        },
        "tags": ["digital", "documents", "storage", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # WIDOW & SPECIAL CATEGORY
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "NSAP-IGNWPS",
        "name": "Indira Gandhi National Widow Pension Scheme",
        "name_hi": "इंदिरा गांधी राष्ट्रीय विधवा पेंशन योजना",
        "ministry": "Ministry of Rural Development",
        "category": "women",
        "type": "Pension",
        "description": "Monthly pension for BPL widows aged 40-79. ₹300/month from Central Government, states add their own contribution (total varies ₹500-₹2,000).",
        "benefits": {
            "amount": "₹300/month (Central) + State contribution",
            "frequency": "Monthly",
            "mode": "Bank/Post office"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 40,
            "max_age": 79,
            "gender": "female",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must be a widow", "Must be BPL household"]
        },
        "required_documents": [
            {"name": "Husband's death certificate", "mandatory": True, "where_to_get": "Municipal office / Gram Panchayat"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "BPL Card", "mandatory": True, "where_to_get": "Food & Civil Supplies"},
            {"name": "Age proof", "mandatory": True, "where_to_get": "Birth certificate / Voter ID"},
            {"name": "Bank/Post Office account", "mandatory": True, "where_to_get": "Bank/Post office"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://nsap.nic.in",
            "offline": "Gram Panchayat / Municipal office / District Social Welfare office",
            "steps": [
                "Visit Gram Panchayat or Social Welfare office",
                "Fill pension application form",
                "Submit death certificate and BPL proof",
                "Application verified at block/district level",
                "Pension starts after approval"
            ],
            "helpline": "State Social Welfare helpline / 181",
            "processing_time": "1-3 months"
        },
        "tags": ["women", "widow", "pension", "bpl", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # TRIBAL WELFARE
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "VAN-DHAN",
        "name": "Van Dhan Vikas Yojana",
        "name_hi": "वन धन विकास योजना",
        "ministry": "Ministry of Tribal Affairs (TRIFED)",
        "category": "tribal",
        "type": "Livelihood",
        "description": "Groups of tribal gatherers into Van Dhan Vikas Kendras for value addition and marketing of Minor Forest Produce (MFP). Each VDVK gets ₹15 lakh for setting up processing facility. Helps tribal communities earn 3x more from forest produce.",
        "benefits": {
            "amount": "₹15 lakh per VDVK + training + market access",
            "frequency": "One-time setup + ongoing market linkage",
            "mode": "Grant to VDVK"
        },
        "eligibility": {
            "occupation": ["tribal_gatherer", "forest_dweller"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["st"],
            "area_type": ["rural"],
            "max_income": None,
            "states": "all",
            "special_conditions": ["Must be tribal / forest dweller", "Group of 20 tribal gatherers form one SHG", "15 SHGs form one VDVK"]
        },
        "required_documents": [
            {"name": "Tribal certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "SHG registration", "mandatory": True, "where_to_get": "Block office / TRIFED"}
        ],
        "application_process": {
            "mode": "Offline",
            "portal": "https://trifed.tribal.gov.in",
            "offline": "TRIFED / State tribal department / Block office",
            "steps": [
                "Form a group of 20 tribal gatherers",
                "Register as SHG at block office",
                "15 SHGs together form a VDVK",
                "Apply through TRIFED or state tribal department",
                "Training provided on value addition",
                "Processing facility set up",
                "Market linkage through Tribes India network"
            ],
            "helpline": "011-26167021",
            "processing_time": "3-6 months"
        },
        "tags": ["tribal", "st", "forest", "livelihood", "mfp", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # EX-SERVICEMEN
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "ESM-SCHOLARSHIP",
        "name": "PM Scholarship for Wards of Ex-Servicemen",
        "name_hi": "पूर्व सैनिकों के वार्डों के लिए प्रधानमंत्री छात्रवृत्ति",
        "ministry": "Ministry of Defence",
        "category": "education",
        "type": "Scholarship",
        "description": "Scholarships for children and widows of ex-servicemen and ex-Coast Guard personnel for professional degree courses. ₹3,000/month for boys and ₹3,000/month for girls.",
        "benefits": {
            "amount": "₹3,000/month for the duration of the course",
            "frequency": "Monthly during academic year",
            "mode": "Direct Bank Transfer"
        },
        "eligibility": {
            "occupation": ["student"],
            "education_level": ["undergraduate", "postgraduate"],
            "min_age": None,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "Ward (son/daughter) or widow of ex-serviceman / ex-Coast Guard",
                "Must be pursuing professional degree course (BE, MBBS, BBA, BCA, etc.)",
                "Must have scored 60% or above in previous exam"
            ]
        },
        "required_documents": [
            {"name": "Ex-serviceman's discharge certificate", "mandatory": True, "where_to_get": "Military records office"},
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Admission letter", "mandatory": True, "where_to_get": "Institution"},
            {"name": "Previous marksheet (60%+)", "mandatory": True, "where_to_get": "Board/University"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://scholarships.gov.in (Kendriya Sainik Board)",
            "steps": [
                "Visit National Scholarship Portal or KSB portal",
                "Register as ward of ex-serviceman",
                "Select PM Scholarship scheme",
                "Fill academic and family details",
                "Upload documents including discharge certificate",
                "Submit for verification by Zila Sainik Board"
            ],
            "helpline": "011-26192352",
            "processing_time": "2-4 months"
        },
        "tags": ["education", "scholarship", "ex_serviceman", "defence", "central"]
    },

    # ═══════════════════════════════════════════════════════════════════
    # MISCELLANEOUS / UNIVERSAL
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": "PM-SVA-NIDHI",
        "name": "PM SVANidhi - Street Vendor Loan",
        "name_hi": "पीएम स्वनिधि - स्ट्रीट वेंडर ऋण",
        "ministry": "Ministry of Housing & Urban Affairs",
        "category": "employment",
        "type": "Microloan",
        "description": "Working capital loan for street vendors. First loan ₹10,000, second ₹20,000, third ₹50,000 on timely repayment. 7% interest subsidy and cashback incentives for digital transactions.",
        "benefits": {
            "amount": "₹10,000 → ₹20,000 → ₹50,000 (progressive loans)",
            "frequency": "Renewable on repayment",
            "mode": "Bank transfer"
        },
        "eligibility": {
            "occupation": ["street_vendor"],
            "min_age": 18,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["urban"],
            "max_income": None,
            "states": "all",
            "special_conditions": [
                "Must be a street vendor with vending certificate / Letter of Recommendation",
                "Listed in survey conducted by Urban Local Body"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Vending certificate / Letter of Recommendation from ULB", "mandatory": True, "where_to_get": "Municipal Corporation / ULB"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Passport size photo", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://pmsvanidhi.mohua.gov.in",
            "offline": "Bank branch or ULB office",
            "steps": [
                "Check if listed in vendor survey at pmsvanidhi.mohua.gov.in",
                "If listed, apply online or visit bank",
                "Fill simple application form",
                "Loan sanctioned within 30 days",
                "Repay in monthly installments (1 year)",
                "Get interest subsidy (7%) quarterly",
                "Earn cashback on digital transactions"
            ],
            "helpline": "1800-11-6163",
            "processing_time": "15-30 days"
        },
        "tags": ["street_vendor", "loan", "urban", "micro_credit", "central"]
    },
    {
        "id": "NATIONAL-APPRENTICESHIP",
        "name": "National Apprenticeship Promotion Scheme",
        "name_hi": "राष्ट्रीय शिक्षुता संवर्धन योजना",
        "ministry": "Ministry of Skill Development & Entrepreneurship",
        "category": "employment",
        "type": "Apprenticeship",
        "description": "Government shares 25% of stipend (up to ₹1,500/month) with employers for engaging apprentices. Apprentices get on-the-job training with stipend.",
        "benefits": {
            "amount": "Stipend ₹5,000-₹9,000/month during training + government certificate",
            "frequency": "Monthly during apprenticeship (6 months - 3 years)",
            "mode": "Through employer"
        },
        "eligibility": {
            "occupation": ["student", "unemployed", "dropout"],
            "education_level": ["class_10", "class_12", "iti", "diploma", "undergraduate"],
            "min_age": 14,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Educational certificates", "mandatory": True, "where_to_get": "School/Board"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Passport size photos", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://www.apprenticeshipindia.gov.in",
            "steps": [
                "Register on apprenticeshipindia.gov.in",
                "Create profile with education and skill details",
                "Search for apprenticeship opportunities",
                "Apply to suitable openings",
                "Employer selects and registers contract",
                "Start apprenticeship with monthly stipend"
            ],
            "helpline": "1800-2700-164",
            "processing_time": "Varies by employer"
        },
        "tags": ["employment", "apprenticeship", "youth", "skill", "training", "central"]
    },
    {
        "id": "PMAY-SENIOR",
        "name": "Pradhan Mantri Awas Yojana - Senior Citizen (Varishtha Pension Bima)",
        "name_hi": "वरिष्ठ पेंशन बीमा योजना",
        "ministry": "Ministry of Finance / LIC",
        "category": "pension",
        "type": "Pension Insurance",
        "description": "Guaranteed pension for senior citizens through LIC. Provides 8-10% annual returns based on mode of pension (monthly/quarterly/half-yearly/annually) for a period of 10 years.",
        "benefits": {
            "amount": "~8-10% annual returns on investment up to ₹15 lakh",
            "frequency": "Choice of monthly/quarterly/annual pension",
            "mode": "Bank transfer"
        },
        "eligibility": {
            "occupation": ["any"],
            "min_age": 60,
            "max_age": None,
            "gender": "any",
            "category": ["general", "obc", "sc", "st", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": None,
            "states": "all"
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "PAN Card", "mandatory": True, "where_to_get": "NSDL portal"},
            {"name": "Age proof", "mandatory": True, "where_to_get": "Various"},
            {"name": "Bank account", "mandatory": True, "where_to_get": "Bank"},
            {"name": "Passport size photo", "mandatory": True, "where_to_get": "Photo studio"}
        ],
        "application_process": {
            "mode": "Online and Offline",
            "portal": "https://www.licindia.in",
            "offline": "LIC branch",
            "steps": [
                "Visit LIC branch or website",
                "Fill VPBY application form",
                "Make lump sum investment",
                "Choose pension frequency",
                "Pension starts from next period"
            ],
            "helpline": "022-68276827",
            "processing_time": "7-10 days"
        },
        "tags": ["pension", "senior_citizen", "lic", "investment", "central"]
    },
    {
        "id": "PM-DAKSH",
        "name": "PM-DAKSH (Pradhan Mantri Dakshta Aur Kushalta Sampann Hitgrahi)",
        "name_hi": "पीएम-दक्ष (प्रधानमंत्री दक्षता और कुशलता सम्पन्न हितग्राही)",
        "ministry": "Ministry of Social Justice & Empowerment",
        "category": "employment",
        "type": "Skill Training",
        "description": "Free skill development training for SC, OBC, EBC, DNT, and sanitation workers. Short-term (32-200 hrs) and long-term (6 months+) courses. Includes monthly stipend during training.",
        "benefits": {
            "amount": "Free training + stipend ₹1,000-₹3,000/month + placement assistance",
            "frequency": "During training period",
            "mode": "Bank transfer"
        },
        "eligibility": {
            "occupation": ["unemployed", "student", "low_income_worker"],
            "min_age": 18,
            "max_age": 45,
            "gender": "any",
            "category": ["sc", "obc", "ews"],
            "area_type": ["rural", "urban"],
            "max_income": 300000,
            "states": "all",
            "special_conditions": [
                "SC/OBC/EBC/DNT/Safai Karamchari",
                "For OBC: annual family income up to ₹3 lakh",
                "For EBC: annual family income up to ₹1 lakh"
            ]
        },
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True, "where_to_get": "UIDAI centre"},
            {"name": "Caste Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Income Certificate", "mandatory": True, "where_to_get": "SDM / Tehsildar office"},
            {"name": "Educational certificates", "mandatory": True, "where_to_get": "School/Board"},
            {"name": "Bank account details", "mandatory": True, "where_to_get": "Bank"}
        ],
        "application_process": {
            "mode": "Online",
            "portal": "https://pmdaksh.dosje.gov.in",
            "steps": [
                "Register on pmdaksh.dosje.gov.in",
                "Select training program and nearest centre",
                "Upload documents",
                "Attend training centre",
                "Complete training and assessment",
                "Receive certificate and placement support"
            ],
            "helpline": "1800-11-0031",
            "processing_time": "Training: 1-6 months"
        },
        "tags": ["employment", "skill", "training", "sc", "obc", "central"]
    },
]


DEFAULT_REVIEW_WINDOW_DAYS = 45

# Only schemes in this registry are treated as actively verified.
VERIFIED_SCHEME_METADATA = {
    "PM-KISAN": {
        "official_source_url": "https://pmkisan.gov.in/",
        "source_name": "PM-KISAN Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMFBY": {
        "official_source_url": "https://pmfby.gov.in/",
        "source_name": "PMFBY Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSP-PRE-MATRIC-SC": {
        "official_source_url": "https://scholarships.gov.in/",
        "source_name": "National Scholarship Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSP-POST-MATRIC-SC": {
        "official_source_url": "https://scholarships.gov.in/",
        "source_name": "National Scholarship Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSP-POST-MATRIC-OBC": {
        "official_source_url": "https://scholarships.gov.in/",
        "source_name": "National Scholarship Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSP-MINORITY": {
        "official_source_url": "https://scholarships.gov.in/",
        "source_name": "National Scholarship Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "AYUSHMAN-BHARAT": {
        "official_source_url": "https://nha.gov.in/PM-JAY.php",
        "source_name": "National Health Authority",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMMVY": {
        "official_source_url": "https://pmmvy.wcd.gov.in/",
        "source_name": "PMMVY Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "SUKANYA-SAMRIDDHI": {
        "official_source_url": "https://www.indiapost.gov.in/Financial/pages/content/sukanya-samriddhi-accounts.aspx",
        "source_name": "India Post",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMSBY": {
        "official_source_url": "https://www.indiapost.gov.in/insurance-services/pmsby",
        "source_name": "India Post",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMJJBY": {
        "official_source_url": "https://www.indiapost.gov.in/insurance-services/pmjjby",
        "source_name": "India Post",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMAY-U": {
        "official_source_url": "https://pmaymis.gov.in/pmaymis2_2024/PMAY-urban-2.html",
        "source_name": "PMAY Urban Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMAY-G": {
        "official_source_url": "https://pmayg.dord.gov.in/",
        "source_name": "PMAY Gramin Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "APY": {
        "official_source_url": "https://www.pfrda.org.in/index1.cshtml?lsid=234",
        "source_name": "PFRDA",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PM-SYM": {
        "official_source_url": "https://labour.gov.in/en/pm-sym",
        "source_name": "Ministry of Labour and Employment",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMJDY": {
        "official_source_url": "https://www.pmjdy.gov.in/scheme",
        "source_name": "Department of Financial Services",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "MUDRA": {
        "official_source_url": "https://www.pmmymudra.com/",
        "source_name": "PMMY / MUDRA Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "STAND-UP-INDIA": {
        "official_source_url": "https://www.standupmitra.in/Home/SUISchemes",
        "source_name": "Stand-Up India Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "MGNREGA": {
        "official_source_url": "https://nregarep1.nic.in/",
        "source_name": "MGNREGA MIS Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "UJJWALA": {
        "official_source_url": "https://www.pmuy.gov.in/",
        "source_name": "PMUY Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "ADIP": {
        "official_source_url": "https://adip.depwd.gov.in/",
        "source_name": "Department of Empowerment of Persons with Disabilities",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "DIGILOCKER": {
        "official_source_url": "https://www.digilocker.gov.in/",
        "source_name": "DigiLocker Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSAP-IGNOAPS": {
        "official_source_url": "https://nsap.nic.in/",
        "source_name": "NSAP Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSAP-IGNDPS": {
        "official_source_url": "https://nsap.nic.in/",
        "source_name": "NSAP Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NSAP-IGNWPS": {
        "official_source_url": "https://nsap.nic.in/",
        "source_name": "NSAP Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PM-SVA-NIDHI": {
        "official_source_url": "https://pmsvanidhi.mohua.gov.in/",
        "source_name": "PM SVANidhi Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "NATIONAL-APPRENTICESHIP": {
        "official_source_url": "https://www.apprenticeshipindia.gov.in/",
        "source_name": "Apprenticeship India",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PM-KUSUM": {
        "official_source_url": "https://pmkusum.mnre.gov.in/",
        "source_name": "MNRE PM-KUSUM Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PM-VIDYALAXMI": {
        "official_source_url": "https://www.vidyalakshmi.co.in/Students/",
        "source_name": "Vidya Lakshmi Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PM-DAKSH": {
        "official_source_url": "https://pmdaksh.dosje.gov.in/",
        "source_name": "PM-DAKSH Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "PMGSY": {
        "official_source_url": "https://www.pmgsy.nic.in/",
        "source_name": "PMGSY Official Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "SBM": {
        "official_source_url": "https://swachhbharatmission.ddws.gov.in/index.php/",
        "source_name": "Swachh Bharat Mission Gramin Portal",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
    "ESM-SCHOLARSHIP": {
        "official_source_url": "https://www.ksb.gov.in/",
        "source_name": "Kendriya Sainik Board",
        "last_verified_on": "2026-03-18",
        "verification_status": "verified",
    },
}


def _derive_review_due_on(last_verified_on: str) -> str:
    verified_date = datetime.strptime(last_verified_on, "%Y-%m-%d").date()
    return date.fromordinal(verified_date.toordinal() + DEFAULT_REVIEW_WINDOW_DAYS).isoformat()


def _with_verification_metadata(scheme: dict) -> dict:
    enriched = deepcopy(scheme)
    metadata = VERIFIED_SCHEME_METADATA.get(enriched["id"], {})

    if metadata:
        enriched.update(metadata)
        enriched["review_due_on"] = metadata.get(
            "review_due_on",
            _derive_review_due_on(metadata["last_verified_on"]),
        )
    else:
        enriched.setdefault("official_source_url", enriched.get("application_process", {}).get("portal"))
        enriched.setdefault("source_name", "Needs official verification")
        enriched["last_verified_on"] = None
        enriched["review_due_on"] = None
        enriched["verification_status"] = "needs_review"

    return enriched


def is_scheme_verified(scheme: dict) -> bool:
    """Return True when a scheme is currently safe to recommend."""
    return scheme.get("verification_status") == "verified"


def get_verified_schemes():
    """Return only actively verified schemes."""
    return [scheme for scheme in get_all_schemes() if is_scheme_verified(scheme)]


def get_all_schemes():
    """Return all schemes."""
    return [_with_verification_metadata(scheme) for scheme in SCHEMES_DATABASE]


def get_scheme_by_id(scheme_id: str):
    """Get a specific scheme by ID."""
    for scheme in SCHEMES_DATABASE:
        if scheme["id"] == scheme_id:
            return _with_verification_metadata(scheme)
    return None


def get_schemes_by_category(category: str):
    """Get schemes filtered by category."""
    return [s for s in SCHEMES_DATABASE if s["category"] == category]


def get_schemes_by_tag(tag: str):
    """Get schemes that have a specific tag."""
    return [s for s in SCHEMES_DATABASE if tag in s.get("tags", [])]


def get_scheme_count():
    """Return total number of schemes in database."""
    return len(SCHEMES_DATABASE)


def get_verified_scheme_count():
    """Return total number of actively verified schemes."""
    return len(VERIFIED_SCHEME_METADATA)
