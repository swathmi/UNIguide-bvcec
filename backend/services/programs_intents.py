# ---------------- IMPORTS ----------------
from sentence_transformers import SentenceTransformer, util

# ---------------- LOAD MODEL (SAME MODEL USED EVERYWHERE) ----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- COURSES & PROGRAMS INTENTS ----------------
COURSES_PROGRAMS_INTENTS = {

    # ========= ACADEMIC LEVEL =========
    "UG_PROGRAMS": [
        "ug courses",
        "ug programs",
        "undergraduate programs",
        "btech courses",
        "ug programs offered",
        "btech branches"
    ],

    "PG_PROGRAMS": [
        "pg courses",
        "pg programs",
        "postgraduate programs",
        "mtech courses",
        "pg programs offered"
    ],

    # ========= PROGRAM / BRANCH =========
    "CSE_PROGRAM": [
        "computer science engineering",
        "cse",
        "cse course",
        "cse program"
    ],

    "CSE_AI_ML_PROGRAM": [
        "cse ai ml",
        "csm",
        "cse-ai ml course",
        "cse-artificial intelligence and machine learning"
    ],

    "CSE_AI_DS_PROGRAM": [
        "cse ai ds",
        "cad",
        "ai ds course",
        "artificial intelligence and data science"
    ],

    "IT_PROGRAM": [
        "information technology",
        "it",
        "it course",
        "it branch"
    ],

    "ECE_PROGRAM": [
        "ece course",
        "ece",
        "electronics and communication engineering"
    ],

    "EEE_PROGRAM": [
        "eee course",
        "eee",
        "electrical and electronics engineering"
    ],

    "MECH_PROGRAM": [
        "mechanical engineering",
        "mech",
        "mechanical course"
    ],

    "CIVIL_PROGRAM": [
        "civil engineering",
        "civil",
        "civil course"
    ],

    # ========= COURSE CODES =========
    "UG_COURSE_CODES": [
        "ug course codes",
        "btech course codes"
    ],

    "PG_COURSE_CODES": [
        "pg course codes",
        "mtech course codes"
    ],

    # ========= ELIGIBILITY =========
    "UG_ELIGIBILITY": [
        "ug eligibility",
        "btech eligibility",
        "eligibility for btech",
        "eligibility for ug courses"
    ],

    "PG_ELIGIBILITY": [
        "pg eligibility",
        "mtech eligibility",
        "eligibility for pg courses",
        "eligibility for pg courses"
    ],

    "LATERAL_ENTRY_ELIGIBILITY": [
        "lateral entry eligibility",
        "lateral eligibility",
        "ecet eligibility"
    ],

    # ========= FEES =========
    "UG_FEES": [
        "ug fees",
        "btech fee structure"
    ],

    "PG_FEES": [
        "pg fees",
        "mtech fee structure"
    ],

    "HOSTEL_FEES": [
        "hostel fees",
        "hostel fee structure"
    ],

    "SCHOLARSHIP_DETAILS": [
        "scholarships",
        "fee reimbursement"
    ],

    # ========= INTAKE =========
    "INTAKE_DETAILS": [
        "intake capacity",
        "branch wise intake",
        "number of seats"
    ],

   

    # ========= TEACHING =========
    "TEACHING_METHODS": [
        "teaching methodology",
        "learning methods"
    ],

    # ========= SYLLABUS =========
    "SYLLABUS_STRUCTURE": [
        "syllabus",
        "course curriculum"
    ],

    "REGULATIONS": [
        "regulations",
        "r20",
        "r23"
    ],

    # ========= PLACEMENTS =========
    "PLACEMENT_PERCENTAGE": [
        "placement percentage",
        "placement record"
    ],

    "TOP_RECRUITERS": [
        "top recruiters",
        "recruiting companies"
    ],

    "PACKAGE_DETAILS": [
        "average package",
        "highest package"
    ],

    "INTERNSHIP_DETAILS": [
        "internships",
        "summer internships"
    ],

    # ========= VALUE ADDED =========
    "TECHNICAL_COURSES": [
        "technical courses",
        "value added courses"
    ],

    "SOFT_SKILLS": [
        "soft skills",
        "aptitude training"
    ],

    # ========= RESEARCH & INDUSTRY =========
    "RESEARCH_ACTIVITIES": [
        "research activities",
        "student research"
    ],

    "INDUSTRY_EXPOSURE": [
        "industrial visits",
        "industry exposure",
        "mous"
    ]
}

# ---------------- INTENT DETECTION FUNCTION ----------------
def detect_courses_programs_intent(user_query, threshold=0.50):
    """
    Detects the best matching Courses & Programs intent
    using semantic similarity.
    """

    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in COURSES_PROGRAMS_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        similarity_scores = util.cos_sim(query_embedding, example_embeddings)

        max_score = similarity_scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent

    return None
