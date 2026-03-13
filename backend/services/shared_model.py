from sentence_transformers import SentenceTransformer

# Load the model once to be shared across all intent modules
# This prevents excessive memory usage and slow startup times
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Shared SentenceTransformer model loaded successfully.")
