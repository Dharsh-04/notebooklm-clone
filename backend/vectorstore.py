import faiss
import os
import numpy as np
import pickle

VECTOR_DIR = "data/vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)

INDEX_FILE = f"{VECTOR_DIR}/index.faiss"
META_FILE = f"{VECTOR_DIR}/meta.pkl"

def load_store():
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(META_FILE, "rb") as f:
            meta = pickle.load(f)
    else:
        index = faiss.IndexFlatIP(384)  # MiniLM dim = 384
        meta = []
    return index, meta

def save_store(index, meta):
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(meta, f)

def save_embeddings(texts, vectors):
    index, meta = load_store()
    index.add(vectors)
    meta.extend(texts)
    save_store(index, meta)

def search(query_vec, k=5):
    index, meta = load_store()
    scores, ids = index.search(np.array([query_vec]), k)
    results = [meta[i] for i in ids[0]]
    return results
