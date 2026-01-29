from sentence_transformers import SentenceTransformer, util

# ==================================================
# Load Model ONCE
# ==================================================
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==================================================
# COLLEGE OVERVIEW INTENTS (100% JSON COVERAGE)
# ==================================================
COLLEGE_OVERVIEW_INTENTS = {

    # ================= BASIC IDENTITY =================
    "COLLEGE_NAME": [
        "college name",
        "what is the name of our college",
        "full name of college"
    ],

    "COLLEGE_SHORT_NAME": [
        "short name of college",
        "college short name",
        
    ],

    "COLLEGE_CODE": [
        "college code",
        "college code number"
    ],

    "COLLEGE_TYPE": [
        "college type",
        "is it private or government",
        "college affiliation"
    ],

    "TRUST_NAME": [
        "trust name",
        "management trust",
        "educational society"
    ],

    "ESTABLISHMENT_YEAR": [
        "established year",
        "year of establishment",
        "when was college established"
    ],

    # ================= VISION & MISSION =================
    "COLLEGE_VISION": [
        "college vision",
        "vision of the college"
    ],

    "COLLEGE_MISSION": [
        "college mission",
        "mission of the college"
    ],

    # ================= MANAGEMENT =================
    "CHAIRMAN_DETAILS": [
        "chairman",
        "who is chairman",
        "college chairman"
    ],

    "FORMER_CHAIRMAN_DETAILS": [
        "former chairman",
        "previous chairman"
    ],

    "FOUNDER_DETAILS": [
        "founder",
        "who founded the college"
    ],

    "PRINCIPAL_DETAILS": [
        "principal",
        "who is principal",
        "college principal"
    ],

    "VICE_PRINCIPAL_DETAILS": [
        "vice principal",
        "who is vice principal"
    ],

    "SECRETARY_DETAILS": [
        "secretary",
        "college secretary"
    ],

    # ================= LOCATION & CONTACT =================
    "COLLEGE_LOCATION": [
        "college location",
        "where is the college located",
        "college address",
        "google maps location"
    ],

    "COLLEGE_CONTACT": [
        "contact details",
        "college phone number",
        "email address of college"
    ],

    # ================= ACCREDITATION =================
    "COLLEGE_ACCREDITATION": [
        "accreditation",
        "naac",
        "nba",
        "aicte approval",
        "ugc recognition"
    ],

    # ================= RANKINGS =================
    "RANKINGS_RECOGNITIONS": [
        "rankings",
        "recognitions",
        "college achievements"
    ],

    # ================= CAMPUS & INFRASTRUCTURE =================
    "CAMPUS_AREA": [
        "campus area",
        "college campus size"
    ],

    "INFRASTRUCTURE": [
        "infrastructure",
        "campus facilities",
        "college facilities"
    ],

    # ================= TIMINGS =================
    "COLLEGE_TIMINGS": [
        "college timings",
        "working hours",
        "office hours"
    ],

    # ================= ONLINE PRESENCE =================
    "ONLINE_PRESENCE": [
        "official website",
        "college social media",
        "facebook instagram linkedin"
    ],

    # ================= ACADEMIC ENVIRONMENT =================
    "TEACHING_METHODOLOGY": [
        "teaching methodology",
        "teaching approach",
        "how teaching is done"
    ],

    "DIGITAL_LEARNING": [
        "digital learning",
        "smart classrooms",
        "online learning facilities"
    ],

    # ================= STUDENT & FACULTY =================
    "STUDENT_STRENGTH": [
        "number of students",
        "student strength"
    ],
    "campus_size": [
    "campus size",
    "college area",
    "campus area",
    "how big is the campus"
    ],


    "FACULTY_STRENGTH": [
        "faculty details",
        "teaching staff",
        "faculty strength"
    ],

    "STUDENT_FACULTY_RATIO": [
        "student faculty ratio"
    ],

    # ================= CULTURE & VALUES =================
    "COLLEGE_CULTURE": [
        "college culture",
        "discipline",
        "college values"
    ],

    # ================= SAFETY & FACILITIES =================
    "SAFETY_FACILITIES": [
        "safety facilities",
        "security",
        "medical facilities",
        "transport facilities"
    ],

    # ================= WHY CHOOSE COLLEGE =================
    "WHY_CHOOSE_COLLEGE": [
        "why choose bvcec",
        "why our college",
        "advantages of bvcec"
    ]
}

# ==================================================
# INTENT DETECTION FUNCTION
# ==================================================
def detect_college_overview_intent(user_query, threshold=0.55):
    """
    Detects best matching college overview intent
    using semantic similarity.
    """

    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in COLLEGE_OVERVIEW_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        similarity_scores = util.cos_sim(query_embedding, example_embeddings)

        max_score = similarity_scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent

    return None
