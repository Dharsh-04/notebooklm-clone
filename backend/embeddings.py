from sentence_transformers import SentenceTransformer
import numpy as np

# Free embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(texts: list[str]):
    vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return vectors
