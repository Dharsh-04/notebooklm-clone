import os
import json
import csv
import numpy as np
from io import BytesIO, StringIO
from dotenv import load_dotenv
load_dotenv()
import PyPDF2
from docx import Document
import markdown2

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq

# Load LLM client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Vector store
vector_store = []

def extract_text_from_document(file_bytes, filename):
    ext = filename.split(".")[-1].lower()

    if ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")

    if ext == "pdf":
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext == "docx":
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == "md":
        return markdown2.markdown(
            file_bytes.decode("utf-8", errors="ignore")
        )

    if ext == "json":
        data = json.loads(file_bytes.decode("utf-8", errors="ignore"))
        return json.dumps(data, indent=2)

    if ext == "csv":
        text = file_bytes.decode("utf-8", errors="ignore")
        reader = csv.reader(StringIO(text))
        return "\n".join(" ".join(row) for row in reader)

    return ""

def embed_and_store(text: str):
    global vector_store
    vector_store = [] 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)
    embeddings = embedder.encode(chunks)

    for chunk, emb in zip(chunks, embeddings):
        vector_store.append((chunk, emb))

def generate_flashcards(num_cards=10):
    global vector_store

    # Take broad context
    all_chunks = " ".join([chunk for chunk, _ in vector_store[:20]])

    prompt = f"""
    You are a study assistant.

    Create {num_cards} flashcards from the notes below.
    Each flashcard should have:
    - Question
    - Answer

    Notes:
    {all_chunks}

    Format:
    Q1: ...
    A1: ...

    Q2: ...
    A2: ...
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def generate_answer(query: str) -> str:
    if not vector_store:
        return "No documents uploaded yet."

    query_emb = embedder.encode([query])[0]

    similarities = []
    for chunk, emb in vector_store:
        score = np.dot(query_emb, emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(emb)
        )
        similarities.append((score, chunk))

    similarities.sort(reverse=True)
    top_chunks = " ".join(c for _, c in similarities[:10])

    prompt = f"""
You are an assistant that has read the following document.

Write a concise, structured summary using the information below.
Do NOT say "not found".
Synthesize the ideas in your own words.
Context:
{top_chunks}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content.strip()

    return answer


