import streamlit as st
import requests
from styles import apply_global_style

apply_global_style()
API_URL = "http://localhost:8000"

st.title("🧠 NotebookLM Clone")
st.caption("Upload files → Ask questions → Get contextual answers")

# Accept txt, pdf, docx
uploaded_files = st.file_uploader(
    "Upload files", 
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write("Uploading files...")

    files = []
    for f in uploaded_files:
        # Determine MIME type based on file extension
        ext = f.name.split(".")[-1].lower()
        if ext == "txt":
            mime = "text/plain"
        elif ext == "pdf":
            mime = "application/pdf"
        elif ext == "docx":
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            mime = "application/octet-stream"
        
        files.append(
            ("files", (f.name, f.getvalue(), mime))
        )

    res = requests.post(f"{API_URL}/upload", files=files)

    if res.status_code == 200:
        st.success("Files uploaded & indexed!")
    else:
        st.error(f"Upload failed: {res.text}")

query = st.text_input("Ask a question based on your uploaded documents")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Thinking..."):
            response = requests.post(f"{API_URL}/ask", json={"query": query})

            if response.status_code == 200:
                st.write("### Answer:")
                st.write(response.json()["answer"])
            else:
                st.error("Error generating answer")

if st.button("🃏 Generate Flashcards"):
    with st.spinner("Creating flashcards..."):
        res = requests.post(f"{API_URL}/flashcards")

        if res.status_code == 200:
            st.subheader("Flashcards")
            st.text(res.json()["flashcards"])
        else:
            st.error("Failed to generate flashcards")

