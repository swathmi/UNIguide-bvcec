from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
MECH_INTENTS = {

    # ---------- BASIC ----------
    "department": [
        "mech department details",
        "mechanical engineering department",
        "tell me about mech department",
        "mech branch information"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "mech hod",
        "who is hod of mech",
        "head of mechanical department"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "mech faculty",
        "mechanical faculty members",
        "mech teaching staff",
        "faculty of mechanical department"
    ],

    # ---------- ADMIN ----------
    "principal": [
        "principal of mech department",
        "mechanical principal"
    ],

    # ---------- SECTIONS ----------
    "research_and_development": [
        "mech research and development",
        "research activities of mech"
    ],

    "professional_societies": [
        "mech professional societies",
        "mechanical activities"
    ],

    "newsletters": [
        "mech newsletters",
        "mechanical newsletters"
    ],

    "nba_e_sar": [
        "mech nba",
        "nba e sar mech"
    ],

    "magazines": [
        "mech magazines",
        "mechanical magazines"
    ],

    "industry_interaction": [
        "industry institution interaction mech",
        "mech industry interaction"
    ],

    "gallery": [
        "mech gallery",
        "mechanical department gallery"
    ],

    "entrepreneurship": [
        "mech entrepreneurship",
        "higher studies after mechanical"
    ],

    "distinguished_alumni": [
        "mech alumni",
        "mechanical distinguished alumni"
    ],

    "placements": [
        "mech placements",
        "mechanical placements"
    ],

    "academic_audit": [
        "mech academic audit",
        "academic audit mechanical"
    ],

    "old_question_papers": [
        "mech old question papers",
        "mechanical previous papers"
    ]
}

# -------- INTENT DETECTOR --------
def detect_mech_intent(user_query, threshold=0.50):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in MECH_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
