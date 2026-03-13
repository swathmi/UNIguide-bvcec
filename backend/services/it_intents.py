from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
IT_INTENTS = {

    # ---------- DEPARTMENT ----------
    "department": [
        "it department details",
        "tell me about it department",
        "information technology department",
        "it branch information",
        "when was it introduced",
        "it intake capacity"
    ],

    # ---------- VISION & MISSION ----------
    "vision_and_mission": [
        "it vision",
        "it mission",
        "vision and mission of it",
        "it department vision mission"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "it hod",
        "who is hod of it",
        "head of it department"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "it faculty",
        "it faculty members",
        "it teaching staff",
        "faculty of it department"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "it syllabus",
        "it curriculum",
        "it academic structure"
    ],

    # ---------- YEAR-WISE ----------
    "year_1": [
        "it first year subjects",
        "it 1-1 subjects",
        "it 1-2 subjects",
        "it first year labs"
    ],

    "year_2": [
        "it second year subjects",
        "it 2-1 subjects",
        "it 2-2 subjects",
        "it second year labs"
    ],

    "year_3": [
        "it third year subjects",
        "it 3-1 subjects",
        "it 3-2 subjects",
        "it third year labs"
    ],

    "year_4": [
        "it final year subjects",
        "it 4-1 subjects",
        "it 4-2 subjects",
        "it final year labs"
    ],

    # ---------- INDUSTRIAL VISITS ----------
    "industrial_visits": [
        "it industrial visits",
        "industrial visits of it department"
    ]
}

# -------- INTENT DETECTOR --------
def detect_it_intent(user_query, threshold=0.45):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in IT_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
