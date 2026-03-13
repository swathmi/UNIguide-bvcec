from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL (global, reused) --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
CSE_AIML_INTENTS = {

    # ---------- DEPARTMENT BASIC ----------
    "department": [
        "CSM department details",
        "Tell me about CSM department",
        "CSM branch information",
        "CSM intake capacity",
        "When was CSM introduced"
    ],

    # ---------- ABOUT ----------
    "about_department": [
        "About CSM department",
        "Overview of CSM department",
        "About CSE AIML department",
        "CSE AIML overview"
    ],

    # ---------- VISION & MISSION ----------
    "vision_and_mission": [
        "vision of csm",
        "mission of csm",
        "csm vision",
        "csm mission",
        "csm vision and mission",
        "vision and mission of csm department",
        "CSE AIML vision",
        "CSE AIML mission"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "Who is HOD of CSM",
        "CSM HOD",
        "CSM HOD name",
        "Head of CSM department",
        "CSE AIML HOD"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "list of faculty in csm department",
        "faculty members of csm",
        "csm department faculty list",
        "who are the faculty of csm",
        "csm teaching staff",
        "faculty of csm department",
        "cse aiml faculty members",
        "csm faculty",
        "csm staff",
        "csm teachers",
        "csm professors",
        "tell me about csm staff",
        "tell me about csm faculty members",
        "csm faculty members",
        "details of csm faculty members",
        "faculty members details",
        "staff members of csm"
    ],

    # ---------- PEO PO PSO ----------
    "peo_po_pso": [
        "CSM PEOs",
        "CSM POs",
        "CSM PSOs",
        "PEO PO PSO of CSM"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "CSM syllabus",
        "CSM subjects",
        "CSM curriculum",
        "CSM academic structure"
    ],

    # ---------- YEAR-WISE ----------
    "year_1": [
        "CSM first year subjects",
        "CSM 1-1 subjects",
        "CSM first year labs"
    ],

    "year_2": [
        "CSM second year subjects",
        "CSM 2-1 subjects",
        "CSM second year labs"
    ],

    "year_3": [
        "CSM third year subjects",
        "CSM 3-1 subjects",
        "CSM third year labs"
    ],

    "year_4": [
        "CSM fourth year subjects",
        "CSM 4-1 subjects",
        "CSM 4-2 subjects",
        "CSM 4-1 labs",
        "CSM 4-2 labs",
        "Final year labs of CSM"
    ],

    # ---------- COURSE OUTCOMES ----------
    "course_outcomes": [
        "CSM course outcomes",
        "Course outcomes of CSM",
        "What students learn in CSM"
    ],

    # ---------- ACTIVITIES ----------
    "activities": [
        "CSM activities",
        "Department activities of CSM"
    ],

    # ---------- INDUSTRIAL VISITS ----------
    "industrial_visits": [
        "CSM industrial visits",
        "Industrial visits of CSM",
        "CSM industry visit details"
    ],

    # ---------- STUDENT CLUBS ----------
    "student_clubs": [
        "CSM student clubs",
        "Clubs in CSM department"
    ],

    # ---------- WORKSHOPS ----------
    "workshops_and_seminars": [
        "CSM workshops",
        "CSM seminars",
        "Workshops conducted by CSM"
    ],

    # ---------- PLACEMENTS ----------
    "placements": [
        "CSM placements",
        "Placement details of CSM",
        "Jobs after CSM"
    ],

    # ==================================================
    # 🔥🔥🔥 NEW: WEBSITE SECTIONS (ONLY ADDITION) 🔥🔥🔥
    # ==================================================

    "research_and_development": [
        "CSM research and development",
        "CSM research activities",
        "research work in csm department",
        "csm r and d"
    ],

    "department_placements": [
        "CSM department placements",
        "placement statistics of csm",
        "csm placement records"
    ],

    "gallery": [
        "CSM gallery",
        "CSM department gallery",
        "photos of csm department"
    ]
}

# -------- INTENT DETECTOR (UNCHANGED) --------
def detect_cse_aiml_intent(user_query, threshold=0.45):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in CSE_AIML_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
