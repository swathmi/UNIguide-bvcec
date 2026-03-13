import os
from sentence_transformers import SentenceTransformer, util

DATA_FILE = os.path.join("data", "website_scraped.txt")
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def load_website_text():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = f.read()

    # Clean + chunk
    lines = [l.strip() for l in raw.split("\n") if len(l.strip()) > 40]

    chunks = []
    buffer = ""

    for line in lines:
        buffer += " " + line
        if len(buffer) > 300:
            chunks.append(buffer.strip())
            buffer = ""

    if buffer:
        chunks.append(buffer.strip())

    return chunks


WEBSITE_CHUNKS = load_website_text()
WEBSITE_EMBEDDINGS = (
    model.encode(WEBSITE_CHUNKS, convert_to_tensor=True)
    if WEBSITE_CHUNKS else None
)


def get_rag_answer(user_query, threshold=0.38):
    if not WEBSITE_CHUNKS:
        return "Website data is not available. Please run the website scraper."

    query_embedding = model.encode(user_query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, WEBSITE_EMBEDDINGS)[0]

    top_k = scores.topk(3)
    best_score = top_k.values[0].item()

    if best_score < threshold:
        return (
            "I couldn't find an exact answer to your question on the website.\n"
            "Please try asking more clearly, for example:\n"
            "- syllabus\n"
            "- placements\n"
            "- admissions\n"
            "- departments"
        )

    answers = [WEBSITE_CHUNKS[i] for i in top_k.indices.tolist()]
    return "\n\n".join(answers)


