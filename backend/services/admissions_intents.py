from sentence_transformers import SentenceTransformer, util

# Load model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")

# ================= ADMISSIONS INTENTS =================

ADMISSIONS_INTENTS = {

    # ---------- DEGREE LEVEL ----------
    "DEGREES_OFFERED": [
        "what degrees are offered",
        "degrees available in bvcec",
        "mee college lo eh degrees vunnayi",
        "btech mtech vunnaya",
        "what programs level are offered",
        "does bvcec offer btech and mtech"
    ],

    # ---------- ADMISSION OVERVIEW ----------
    "ADMISSION_OVERVIEW": [
        "admission overview",
        "tell me about admissions",
        "how admissions are done",
        "bvcec admission details",
        "college admission process overview"
    ],

    "ADMISSION_MODES": [
        "admission modes",
        "types of admissions",
        "how can i get admission",
        "government quota management quota",
        "eamcet ecet management quota"
    ],

    # ---------- BTECH ----------
    "BTECH_ADMISSION_PROCESS": [
        "btech admission process",
        "how to join btech",
        "btech admission procedure",
        "btech seat allotment process"
    ],

    "BTECH_ELIGIBILITY": [
        "btech eligibility",
        "eligibility for btech",
        "engineering eligibility",
        "can i join btech",
        "btech admission eligibility"
    ],

    "BTECH_ENTRANCE_EXAM": [
        "btech entrance exam",
        "eamcet for btech",
        "which exam for btech",
        "ap eamcet details"
    ],

    "BTECH_COUNSELING": [
        "btech counseling",
        "eamcet counseling",
        "how counseling works for btech"
    ],

    # ---------- LATERAL ENTRY ----------
    "LATERAL_ENTRY_OVERVIEW": [
        "lateral entry admission",
        "second year admission",
        "direct second year btech"
    ],

    "LATERAL_ENTRY_ELIGIBILITY": [
        "lateral entry eligibility",
        "ecet eligibility",
        "diploma lateral entry"
    ],

    "LATERAL_ENTRY_ENTRANCE_EXAM": [
        "ecet exam",
        "lateral entry entrance exam",
        "ap ecet details"
    ],

    # ---------- MANAGEMENT QUOTA ----------
    "MANAGEMENT_QUOTA_OVERVIEW": [
        "management quota",
        "management quota admission",
        "direct admission",
        "without eamcet admission"
    ],

    "MANAGEMENT_QUOTA_ELIGIBILITY": [
        "management quota eligibility",
        "who can apply for management quota"
    ],

    "MANAGEMENT_QUOTA_PROCESS": [
        "management quota process",
        "how to apply for management quota"
    ],

    # ---------- DATES ----------
    "IMPORTANT_ADMISSION_DATES": [
        "important admission dates",
        "admission dates",
        "when admissions start",
        "eamcet admission dates"
    ],

    # ---------- DOCUMENTS ----------
    "DOCUMENTS_REQUIRED_MANDATORY": [
        "documents required for admission",
        "mandatory documents",
        "certificates required for admission"
    ],

    "DOCUMENTS_REQUIRED_CATEGORY": [
        "caste certificate required",
        "ews certificate",
        "income certificate required"
    ],

    # ---------- COUNSELING ----------
    "COUNSELING_AUTHORITY": [
        "who conducts counseling",
        "counseling authority",
        "apsche counseling"
    ],

    "COUNSELING_STEPS": [
        "counseling steps",
        "counseling procedure",
        "how counseling is done"
    ],

    "SEAT_ALLOTMENT_RULES": [
        "seat allotment rules",
        "how seats are allotted",
        "seat allotment process"
    ],

    # ---------- RESERVATION ----------
    "RESERVATION_POLICY_OVERVIEW": [
        "reservation policy",
        "reservation rules",
        "does reservation apply"
    ],

    "RESERVATION_SC": [
        "sc reservation",
        "scheduled caste reservation"
    ],

    "RESERVATION_ST": [
        "st reservation",
        "scheduled tribe reservation"
    ],

    "RESERVATION_BC": [
        "bc reservation",
        "backward class reservation"
    ],

    "RESERVATION_EWS": [
        "ews reservation",
        "economically weaker section"
    ],

    "RESERVATION_PWD": [
        "pwd reservation",
        "physically challenged reservation"
    ],

    "MANAGEMENT_QUOTA_RESERVATION": [
        "reservation in management quota",
        "does management quota have reservation"
    ],

    # ---------- HELP DESK ----------
    "ADMISSION_OFFICER_DETAILS": [
        "admission officer",
        "administrative officer",
        "who is admission incharge"
    ],

    "ADMISSION_CONTACT_NUMBERS": [
        "admission contact number",
        "phone number for admission",
        "admission helpline"
    ],

    "ADMISSION_EMAIL_CONTACTS": [
        "admission email",
        "email for admission enquiry"
    ],

    # ---------- INTERNATIONAL / NEPAL ----------
    "INTERNATIONAL_STUDENTS_OVERVIEW": [
        "international students",
        "foreign students in bvcec",
        "students from other countries"
    ],

    "NEPAL_STUDENTS_AVAILABILITY": [
        "nepal students",
        "are nepal students studying",
        "does bvcec have nepal students"
    ],

    "NEPAL_REGISTERED_OFFICE_DETAILS": [
        "nepal office details",
        "nepal registered office",
        "nepal admission contact"
    ],

    "INTERNATIONAL_ADMISSIONS_INCHARGE": [
        "international admissions incharge",
        "who handles foreign admissions"
    ],

    "INTERNATIONAL_ADMISSIONS_CONTACT": [
        "international admission contact",
        "foreign student contact number"
    ],

    "INTERNATIONAL_ADMISSIONS_ADDRESS": [
        "international admissions address",
        "foreign admissions office address"
    ],

    # ---------- GENERAL RULES ----------
    "GENERAL_ADMISSION_RULES": [
        "general admission rules",
        "admission rules",
        "college admission policies"
    ]
}

# ================= INTENT DETECTOR =================

def detect_admission_intent(user_query, threshold=0.55):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in ADMISSIONS_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        similarity_scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = similarity_scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent

    return None
