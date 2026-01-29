# ---------------- IMPORTS ----------------
from sentence_transformers import SentenceTransformer, util

# ---------------- LOAD MODEL ----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================================
# INSTITUTION LEVEL INTENTS
# =========================================================
INSTITUTION_INTENTS = {

    # ================= PLACEMENTS =================
    "PLACEMENT_OVERVIEW": [
        "placement overview",
        "tell me about placements",
        "training and placement cell"
    ],

    "PLACEMENT_HEAD": [
        "placement head",
        "placement officer",
        "who is placement head"
    ],

    "FIRST_PLACEMENT_2026": [
        "first placement 2026",
        "who got first placement",
        "2026 first placement details"
    ],

    "PLACEMENT_DRIVES": [
        "placement drives conducted",
        "placement drive list",
        "companies visited for placements"
    ],

    "ONGOING_PLACEMENT_DRIVES": [
        "ongoing placement drives",
        "current placement drives",
        "present placement drives"
    ],

    "UPCOMING_PLACEMENT_DRIVES": [
        "upcoming placement drives",
        "next placement drive",
        "future placement drives"
    ],

    "TOP_RECRUITERS": [
        "top recruiters",
        "leading recruiters",
        "top placement companies"
    ],

    "PLACEMENT_TRAINING": [
        "placement training programs",
        "soft skills training",
        "aptitude training",
        "interview preparation"
    ],

    "COMPANY_WISE_PLACEMENTS": [
        "Efftronics placement details",
        "Ocean Link drive details",
        "Renault Nissan placements",
        "Soft Suave placement details"
    ],

    # ================= EVENTS =================
    "EVENT_TYPES": [
        "types of events conducted",
        "what events are conducted",
        "college events"
    ],

    "TECHNICAL_EVENTS": [
        "technical events",
        "hackathons conducted",
        "coding competitions"
    ],

    "WORKSHOPS_SEMINARS": [
        "workshops conducted",
        "seminars conducted",
        "faculty workshops"
    ],

    "CULTURAL_EVENTS": [
        "cultural events",
        "college cultural programs",
        "annual day celebrations"
    ],

    "NSS_EVENTS": [
        "nss activities",
        "social responsibility events",
        "nss camps"
    ],

    "RECENT_EVENTS": [
        "recent events",
        "latest events",
        "recently conducted events"
    ],

    # ================= LATEST UPDATES =================
    "LATEST_UPDATES": [
        "latest updates",
        "recent updates",
        "college news"
    ],

    # ================= FACULTY & FDP =================
    "FACULTY_DEVELOPMENT_PROGRAMS": [
        "faculty development programs",
        "fdp programs",
        "cse fdp list"
    ],

    "FACULTY_ACHIEVEMENTS": [
        "faculty achievements",
        "faculty awards",
        "faculty accomplishments"
    ],

    # ================= RESEARCH & PUBLICATIONS =================
    "RESEARCH_PUBLICATIONS": [
        "research publications",
        "faculty publications",
        "published papers"
    ],

    "SCOPUS_PUBLICATIONS": [
        "scopus papers",
        "scopus indexed journals"
    ],

    "FACULTY_WISE_PUBLICATIONS": [
        "Dr A Nageswara Rao publications",
        "B Srilatha research papers",
        "T Priyanka publications"
    ]
}

# =========================================================
# INTENT DETECTION FUNCTION
# =========================================================
def detect_institution_intent(user_query, threshold=0.50):
    """
    Detects the best matching institution-level intent
    using semantic similarity.
    """

    query_embedding = model.encode(user_query, convert_to_tensor=True)

    best_intent = None
    best_score = 0.0

    for intent, examples in INSTITUTION_INTENTS.items():
        example_embeddings = model.encode(examples, convert_to_tensor=True)
        similarity_scores = util.cos_sim(query_embedding, example_embeddings)

        max_score = similarity_scores.max().item()

        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score >= threshold:
        return best_intent

    return None
