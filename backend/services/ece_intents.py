from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
ECE_INTENTS = {

    # ---------- DEPARTMENT BASIC ----------
    "department": [
        "ece department details",
        "tell me about ece department",
        "ece branch information",
        "ece intake capacity",
        "when was ece introduced"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "ece hod",
        "who is hod of ece",
        "head of ece department"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "ece faculty",
        "ece faculty members",
        "ece teaching staff",
        "faculty of ece department"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "ece syllabus",
        "ece curriculum",
        "ece academic structure",
        "subjects in ece"
    ],

    # ---------- YEAR 1 ----------
    "year_1": [
        "ece first year subjects",
        "ece 1-1 subjects",
        "ece 1-2 subjects",
        "ece first year labs"
    ],

    # ---------- YEAR 2 ----------
    "year_2": [
        "ece second year subjects",
        "ece 2-1 subjects",
        "ece 2-2 subjects",
        "ece second year labs"
    ],

    # ---------- YEAR 3 ----------
    "year_3": [
        "ece third year subjects",
        "ece 3-1 subjects",
        "ece 3-2 subjects",
        "ece third year labs"
    ],

    # ---------- YEAR 4 ----------
    "year_4": [
        "ece fourth year subjects",
        "ece 4-1 subjects",
        "ece 4-2 subjects",
        "ece final year subjects",
        "ece final year labs"
    ],

    # ---------- STUDENT PROJECTS ----------
    "student_projects": [
        "ece student projects",
        "ece projects",
        "projects done by ece students"
    ],

    # ---------- INFRASTRUCTURE ----------
    "infrastructure": [
        "ece labs",
        "ece infrastructure",
        "ece facilities"
    ]
}

# -------- INTENT DETECTOR --------
def detect_ece_intent(user_query, threshold=0.45):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in ECE_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
