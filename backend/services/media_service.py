import os
import json

PDF_FILE = os.path.join("data", "website_pdfs.json")
IMAGE_FILE = os.path.join("data", "website_images.json")

# -------- BRANCH KEYWORDS --------
BRANCH_KEYWORDS = {
    "cse": ["cse"],
    "csm": ["cse-aiml"],
    "aiml": ["aiml", "ai", "ml"],
    "mech": ["mech", "mechanical"],
    "civil": ["civil"],
    "ece": ["ece"],
    "eee": ["eee"]
}


# -------- LOAD JSON --------
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

PDFS = load_json(PDF_FILE)
IMAGES = load_json(IMAGE_FILE)

# -------- HELPER --------
def detect_branch(query):
    q = query.lower()
    for branch, keys in BRANCH_KEYWORDS.items():
        if any(k in q for k in keys):
            return branch
    return None


# ================= MAIN MEDIA HANDLER =================
def get_media_response(user_query):
    q = user_query.lower()

    # ================= PDF HANDLING =================
    if "pdf" in q or "syllabus" in q or "download" in q:
        if not PDFS:
            return "No PDF documents are available at the moment."

        branch = detect_branch(q)
        matched = []

        for pdf in PDFS:
            url = pdf.get("url", "").lower()
            name = pdf.get("name", "Document")

            if branch:
                if branch in url:
                    matched.append((name, pdf["url"]))
            else:
                matched.append((name, pdf["url"]))

        if not matched:
            return "No matching PDF found for your request."

        response = "📄 **Available PDF Downloads:**\n\n"
        for name, link in matched[:6]:
            response += f"- 🔗 [{name}]({link})\n"

        return response

    # ================= IMAGE HANDLING =================
    if "image" in q or "photo" in q or "gallery" in q:
        if not IMAGES:
            return "No images are available at the moment."

        response = "🖼️ **Campus Images:**\n\n"
        for img in IMAGES[:8]:
            response += f"- 🔗 {img['url']}\n"

        return response

    return None
