from sentence_transformers import SentenceTransformer, util

# ================= LOAD MODEL =================
model = SentenceTransformer("all-MiniLM-L6-v2")

# ================= CAD (CSE-AIDS) INTENTS =================
CAD_INTENTS = {

    # -------- BASIC --------
    "department": [
        "cad department",
        "cse aids department",
        "computer science and data science department",
        "tell me about cad",
        "cad department details",
        "cad intake",
        "cad intake capacity",
        "when was cad introduced",
        "cad department overview"
    ],

    # -------- ABOUT --------
    "about_department": [
        "about cad department",
        "cad department overview",
        "cse aids overview",
        "what is cad department",
        "cad focus areas",
        "data science specialization"
    ],

    # -------- VISION & MISSION --------
    "vision_and_mission": [
        "cad vision",
        "cad mission",
        "cad vision and mission",
        "vision of cad department",
        "mission of cad department",
        "cse aids vision",
        "cse aids mission"
    ],

    # -------- HOD --------
    "head_of_department": [
        "cad hod",
        "who is hod of cad",
        "cad department hod",
        "cad hod name",
        "head of cad department",
        "cse aids hod"
    ],

    # -------- FACULTY --------
    "faculty": [
        "cad faculty",
        "cad department faculty",
        "cad faculty list",
        "cad teaching staff",
        "who are the faculty of cad",
        "cse aids faculty"
    ],

    # -------- PEO / PO / PSO --------
    "peo_po_pso": [
        "cad peos",
        "cad pos",
        "cad psos",
        "cad peo po pso",
        "program outcomes of cad",
        "program specific outcomes of cad"
    ],

    # -------- ACADEMIC STRUCTURE --------
    "academic_structure": [
        "cad syllabus",
        "cad curriculum",
        "cad subjects",
        "cad academic structure",
        "cse aids syllabus"
    ],

    # -------- YEAR-WISE --------
    "year_1": [
        "cad first year subjects",
        "cad 1-1 subjects",
        "cad 1-2 subjects",
        "cad first year labs"
    ],

    "year_2": [
        "cad second year subjects",
        "cad 2-1 subjects",
        "cad 2-2 subjects",
        "cad second year labs"
    ],

    "year_3": [
        "cad third year subjects",
        "cad 3-1 subjects",
        "cad 3-2 subjects",
        "cad third year labs"
    ],

    "year_4": [
        "cad final year subjects",
        "cad 4-1 subjects",
        "cad 4-2 subjects",
        "cad major project",
        "cad internship"
    ],

    # -------- COURSE OUTCOMES --------
    "course_outcomes": [
        "cad course outcomes",
        "what students learn in cad",
        "cad learning outcomes",
        "skills gained in cad"
    ],

    # -------- ACTIVITIES --------
    "activities": [
        "cad activities",
        "cad department activities",
        "cad co curricular activities"
    ],

    # -------- INDUSTRIAL VISITS --------
    "industrial_visits": [
        "cad industrial visits",
        "industrial visits of cad"
    ],

    # -------- STUDENT CLUBS --------
    "student_clubs": [
        "cad clubs",
        "cad student clubs"
    ],

    # -------- WORKSHOPS --------
    "workshops_and_seminars": [
        "cad workshops",
        "cad seminars",
        "workshops conducted by cad"
    ],

    # -------- PLACEMENTS --------
    "placements": [
        "cad placements",
        "jobs after cad",
        "career options after cad",
        "cse aids placements"
    ]
}

# ================= DETECTOR =================
def detect_cad_intent(user_query, threshold=0.45):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in CAD_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
