from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
AIML_INTENTS = {

    # ---------- DEPARTMENT BASIC ----------
    "department": [
        "AIML department details",
        "Tell me about AIML department",
        "AIML branch information",
        "AIML intake capacity",
        "When was AIML introduced"
    ],

    # ---------- ABOUT ----------
    "about_department": [
        "About AIML department",
        "Overview of AIML department",
        "About AI and ML department",
        "AIML overview"
    ],

    # ---------- VISION & MISSION ----------
    "vision_and_mission": [
        "vision of AIML",
        "mission of AIML",
        "AIML vision",
        "AIML mission",
        "AIML vision and mission",
        "vision and mission of AIML department"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "Who is HOD of AIML",
        "AIML HOD",
        "AIML HOD name",
        "Head of AIML department"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "list of faculty in AIML department",
        "faculty members of AIML",
        "AIML department faculty list",
        "who are the faculty of AIML",
        "AIML teaching staff"
    ],

    # ---------- PEO PO PSO ----------
    "peo_po_pso": [
        "AIML PEOs",
        "AIML POs",
        "AIML PSOs",
        "PEO PO PSO of AIML"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "AIML syllabus",
        "AIML subjects",
        "AIML curriculum",
        "AIML academic structure"
    ],

    # ---------- YEAR-WISE ----------
    "year_1": [
        "AIML first year subjects",
        "AIML 1-1 subjects",
        "AIML first year labs"
    ],

    "year_2": [
        "AIML second year subjects",
        "AIML 2-1 subjects",
        "AIML second year labs"
    ],

    "year_3": [
        "AIML third year subjects",
        "AIML 3-1 subjects",
        "AIML third year labs"
    ],

    "year_4": [
        "AIML fourth year subjects",
        "AIML 4-1 subjects",
        "AIML 4-2 subjects",
        "Final year labs of AIML"
    ],

    # ---------- COURSE OUTCOMES ----------
    "course_outcomes": [
        "AIML course outcomes",
        "Course outcomes of AIML",
        "What students learn in AIML"
    ],

    # ---------- ACTIVITIES ----------
    "activities": [
        "AIML activities",
        "Department activities of AIML"
    ],

    "industrial_visits": [
        "AIML industrial visits",
        "Industrial visits of AIML"
    ],

    "student_clubs": [
        "AIML student clubs",
        "Clubs in AIML department"
    ],

    "workshops_and_seminars": [
        "AIML workshops",
        "AIML seminars"
    ],

    # ---------- PLACEMENTS ----------
    "placements": [
        "AIML placements",
        "Placement details of AIML",
        "Jobs after AIML"
    ]
}

# -------- INTENT DETECTOR --------
def detect_aiml_intent(user_query, threshold=0.45):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in AIML_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
