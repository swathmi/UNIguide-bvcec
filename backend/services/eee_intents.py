from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
EEE_INTENTS = {

    # ---------- DEPARTMENT ----------
    "department": [
        "eee department details",
        "tell me about eee department",
        "eee branch information",
        "when was eee introduced",
        "eee intake capacity"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "eee hod",
        "who is hod of eee",
        "head of eee department"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "eee faculty",
        "eee faculty members",
        "eee teaching staff",
        "faculty of eee department"
    ],

    # ---------- VISION & MISSION ----------
    "vision_and_mission": [
        "eee vision",
        "eee mission",
        "vision and mission of eee"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "eee syllabus",
        "eee curriculum",
        "eee academic structure"
    ],

    # ---------- YEAR 1 ----------
    "year_1": [
        "eee first year subjects",
        "eee 1-1 subjects",
        "eee 1-2 subjects",
        "eee first year labs"
    ],

    # ---------- YEAR 2 ----------
    "year_2": [
        "eee second year subjects",
        "eee 2-1 subjects",
        "eee 2-2 subjects",
        "eee second year labs"
    ],

    # ---------- YEAR 3 ----------
    "year_3": [
        "eee third year subjects",
        "eee 3-1 subjects",
        "eee 3-2 subjects",
        "eee third year labs"
    ],

    # ---------- YEAR 4 ----------
    "year_4": [
        "eee final year subjects",
        "eee 4-1 subjects",
        "eee 4-2 subjects",
        "eee final year labs"
    ],

    # ---------- SYLLABUS ----------
    "syllabus_links": [
        "eee syllabus pdf",
        "eee regulation syllabus",
        "eee br18 syllabus",
        "eee br20 syllabus",
        "eee br23 syllabus"
    ],

    # ---------- STUDENT PROJECTS ----------
    "student_projects": [
        "eee student projects",
        "projects done by eee students"
    ],

    # ---------- HIGHER STUDIES ----------
    "higher_studies": [
        "higher studies after eee",
        "eee higher education options"
    ],

    # ---------- ENTREPRENEURSHIP ----------
    "entrepreneurship": [
        "entrepreneurship after eee",
        "business options for eee students"
    ]
}

# -------- INTENT DETECTOR --------
def detect_eee_intent(user_query, threshold=0.50):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in EEE_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
