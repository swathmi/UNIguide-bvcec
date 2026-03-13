from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        print("🔵 Loading model...")
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("✅ Model loaded.")
    return _model
