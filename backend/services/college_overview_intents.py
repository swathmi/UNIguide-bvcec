from sentence_transformers import util
from services.shared_model import model

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
        "who founded the college",
        "who is the founder",
        "founder of bvcec",
        "who is the founder of bvcec",
        "who is the founder of the college",
        "who established bvcec",
        "who established the college"
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
    ],

    # ================= DEPARTMENTS =================
    "DEPARTMENT_COUNT": [
        "how many departments are there",
        "number of departments",
        "total departments",
        "departments count",
        "how many departments in our college"
    ],

    "DEPARTMENT_LIST": [
        "list of departments",
        "all departments",
        "what are the departments",
        "departments offered",
        "available departments",
        "departments in college"
    ]
}

# ==================================================
# INTENT DETECTION FUNCTION
# ==================================================
def detect_college_overview_intent(user_query, threshold=0.55):
    """
    Detects best matching college overview intent
    using semantic similarity.
    EXCLUDES queries that mention specific departments.
    """
    
    query_lower = user_query.lower()
    
    # Department keywords to exclude college overview matching
    DEPARTMENT_KEYWORDS = [
        "csm", "cse aiml", "aiml", "cad", "aids", "civil", "ce", "cse", 
        "computer science", "ece", "electronics", "eee", "electrical", 
        "it", "information technology", "mech", "mechanical"
    ]
    
    # If query mentions a specific department, don't match college overview
    if any(dept in query_lower for dept in DEPARTMENT_KEYWORDS):
        return None

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
