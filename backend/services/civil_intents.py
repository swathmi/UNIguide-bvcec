from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
CIVIL_INTENTS = {

    # ---------- DEPARTMENT BASIC ----------
    "department": [
        "Civil engineering department details",
        "Tell me about civil department",
        "Civil branch information",
        "CE department details",
        "Civil engineering details"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "Who is HOD of civil",
        "Civil HOD name",
        "Head of civil department",
        "CE HOD"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "Civil department faculty",
        "Faculty members of civil",
        "Civil engineering faculty list",
        "Teaching staff of civil department"
    ],

    # ---------- VISION & MISSION ----------
    "vision_and_mission": [
        "Vision of civil department",
        "Mission of civil department",
        "Civil department vision and mission",
        "CE vision and mission"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "Civil syllabus",
        "Civil curriculum",
        "Civil academic structure",
        "Subjects in civil engineering"
    ],

    # ---------- YEAR-WISE ----------
    "year_1": [
        "Civil first year subjects",
        "Civil 1-1 subjects",
        "Civil first year labs"
    ],

    "year_2": [
        "Civil second year subjects",
        "Civil 2-1 subjects",
        "Civil second year labs"
    ],

    "year_3": [
        "Civil third year subjects",
        "Civil 3-1 subjects",
        "Civil third year labs"
    ],

    "year_4": [
        "Civil fourth year subjects",
        "Civil final year subjects",
        "Final year labs of civil"
    ],

    # ---------- SYLLABUS ----------
    "syllabus": [
        "Civil syllabus pdf",
        "Civil regulation syllabus",
        "Civil syllabus link"
    ],

    # ---------- ACTIVITIES ----------
    "department_activities": [
        "Civil department activities",
        "Activities in civil department",
        "Civil engineering activities"
    ]
}

# -------- INTENT DETECTOR --------
def detect_civil_intent(user_query, threshold=0.50):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in CIVIL_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
