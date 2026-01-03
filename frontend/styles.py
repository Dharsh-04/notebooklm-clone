import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>
    /* App background */
    .stApp {
        background-color: #f9fafb;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Headers */
    h1, h2, h3 {
        color: #111827;
    }

    /* Buttons */
    .stButton > button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #4338CA;
    }

    /* Inputs */
    input, textarea {
        border-radius: 6px !important;
    }

    /* File uploader */
    .stFileUploader {
        border: 2px dashed #c7d2fe;
        border-radius: 12px;
        padding: 20px;
        background: white;
    }

    /* Chat messages */
    .stChatMessage {
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
