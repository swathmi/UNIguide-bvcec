from sentence_transformers import SentenceTransformer, util

# -------- LOAD MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- INTENTS --------
PLACEMENT_INTENTS = {
    "placement_materials": [
        "placement materials",
        "placement preparation materials",
        "placement resources",
        "what materials are available for placement",
        "where to get placement notes",
        "placement study materials"
    ],

    "programming_languages": [
        "c programming",
        "java programming",
        "python programming",
        "sql programming",
        "programming language resources",
        "coding materials",
        "c language",
        "c language notes",
        "python notes",
        "java notes",
        "sql notes",
        "any coding materials",
        "programming resources",
        "language tutorial",
        "code examples"
    ],

    "aptitude_materials": [
        "aptitude materials",
        "quantitative aptitude",
        "logical reasoning",
        "reasoning questions",
        "aptitude resources"
    ],

    "verbal_materials": [
        "english materials",
        "communication skills",
        "verbal ability",
        "english grammar",
        "vocabulary"
    ],

    "company_placements": [
        "company placements",
        "students placed in companies",
        "which company hired students",
        "placement company list",
        "students placed in tcs",
        "students placed in infosys",
        "students placed in wipro",
        "hiring companies",
        "tcs placement",
        "infosys recruitment",
        "wipro campus drive",
        "company recruitment"
    ],

    "attendance_policy": [
        "attendance policy",
        "attendance requirements",
        "minimum attendance",
        "attendance rules",
        "what is attendance percentage required",
        "what is the attendance policy"
    ],

    "faculty_development": [
        "faculty development programs",
        "faculty research schemes",
        "faculty training programs",
        "faculty workshops",
        "any faculty development programs",
        "fdp",
        "faculty development"
    ],

    "circulars": [
        "latest circulars",
        "college circulars",
        "announcements",
        "college news",
        "recent updates",
        "latest updates",
        "what are the latest circulars",
        "latest announcements"
    ]
}

# -------- INTENT DETECTOR --------
def detect_placement_intent(user_query, threshold=0.20):
    """
    Detects placement intent using semantic matching.
    Very low threshold (0.20) for maximum matching.
    """
    query_lower = user_query.lower()
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in PLACEMENT_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, example_embeddings)
        max_score = scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, 0.0
