from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from llm import extract_text_from_document, embed_and_store, generate_answer,generate_flashcards
from typing import List

import os
import io
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_files(files: List[UploadFile]):
    for f in files:
        file_bytes = await f.read()
        filename = f.filename

        # Extract text
        text = extract_text_from_document(file_bytes, filename)

        # Store embeddings
        embed_and_store(text)

    return {"status": "success"}



@app.post("/ask")
async def ask_question(data: dict):
    query = data.get("query", "")
    if not query.strip():
        return {"error": "Query is empty."}

    answer = generate_answer(query)
    return {"answer": answer}

@app.post("/flashcards")
async def flashcards():
    cards = generate_flashcards()
    return {"flashcards": cards}
