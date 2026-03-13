from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
CSE_INTENTS = {

    # ---------- DEPARTMENT ----------
    "department": [
        "CSE department details",
        "Tell me about CSE department",
        "Computer science department details",
        "CSE branch information",
        "CSE intake capacity"
    ],

    # ---------- VISION & MISSION ----------
    "vision_mission": [
        "CSE vision",
        "CSE mission",
        "Vision and mission of CSE",
        "Computer science vision and mission"
    ],

    # ---------- HOD ----------
    "head_of_department": [
        "Who is HOD of CSE",
        "CSE HOD name",
        "Head of CSE department"
    ],

    # ---------- FACULTY ----------
    "faculty": [
        "CSE faculty list",
        "Faculty members of CSE",
        "Teaching staff of CSE department",
        "Who are the faculty in CSE",
        "CSE teachers",
        "CSE professors",
        "CSE faculty members list",
        "Tell me about CSE faculty"
    ],

    # ---------- ACADEMIC STRUCTURE ----------
    "academic_structure": [
        "CSE syllabus",
        "CSE curriculum",
        "CSE academic structure",
        "Subjects in CSE"
    ],

    # ---------- YEAR-WISE ----------
    "year_1": [
        "CSE first year subjects",
        "CSE 1-1 subjects",
        "CSE first year labs"
    ],

    "year_2": [
        "CSE second year subjects",
        "CSE 2-1 subjects",
        "CSE second year labs"
    ],

    "year_3": [
        "CSE third year subjects",
        "CSE 3-1 subjects",
        "CSE third year labs"
    ],

    "year_4": [
        "CSE fourth year subjects",
        "CSE final year subjects",
        "Final year labs of CSE"
    ],

    # ---------- R&D ----------
    "research_and_development": [
        "cse research and development",
        "research activities of cse",
        "cse r and d"
    ],

    # ---------- PROFESSIONAL SOCIETIES ----------
    "professional_societies": [
        "cse professional societies",
        "cse professional activities"
    ],

    # ---------- NEWSLETTERS ----------
    "newsletters": [
        "cse newsletters",
        "computer science newsletters"
    ],

    # ---------- NBA ----------
    "nba_e_sar": [
        "cse nba",
        "nba e sar cse"
    ],

    # ---------- MAGAZINES ----------
    "magazines": [
        "cse magazines",
        "computer science magazines"
    ],

    # ---------- INDUSTRY INTERACTION ----------
    "industry_interaction": [
        "industry institution interaction cse",
        "cse industry interaction"
    ],

    # ---------- INDUSTRIAL VISITS ----------
    "industrial_visits": [
        "CSE industrial visits",
        "Industrial visits of CSE",
        "Companies visited by CSE students"
    ],

    # ---------- GALLERY ----------
    "gallery": [
        "cse gallery",
        "computer science department gallery"
    ],

    # ---------- ENTREPRENEURSHIP ----------
    "entrepreneurship": [
        "cse entrepreneurship",
        "higher studies after cse"
    ],

    # ---------- ALUMNI ----------
    "distinguished_alumni": [
        "cse alumni",
        "computer science distinguished alumni"
    ],

    # ---------- PLACEMENTS ----------
    "placements": [
        "cse placements",
        "computer science placements"
    ],

    # ---------- ACADEMIC AUDIT ----------
    "academic_audit": [
        "cse academic audit",
        "academic audit computer science"
    ],

    # ---------- OLD QUESTION PAPERS ----------
    "old_question_papers": [
        "cse old question papers",
        "computer science previous papers"
    ]
}

# -------- INTENT DETECTOR --------
def detect_cse_intent(user_query, threshold=0.45):
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in CSE_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
