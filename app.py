import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import pyperclip

# Page configuration
st.set_page_config(page_title="Smart OCR Scanner", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    .stApp {
        background-color: #f8fafc;
    }
    div[data-testid="stFileUploader"] {
        border: 2px dashed #e5e7eb;
        border-radius: 0.75rem;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #2563eb;
        background-color: #f8fafc;
    }
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        padding: 0.75rem;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1e40af;
    }
    h1 {
        color: #111827;
        text-align: center;
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .result-container {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-top: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
        text-align: center;
    }
    .feature {
        padding: 1rem;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTextArea textarea {
        font-family: 'Inter', sans-serif;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize EasyOCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# App header
st.markdown("<h1>Smart OCR Scanner</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Extract text from images instantly</p>", unsafe_allow_html=True)

# Features section
st.markdown("""
    <div class='features-grid'>
        <div class='feature'>
            <h3>📸 Fast Processing</h3>
            <p>Quick and efficient text extraction</p>
        </div>
        <div class='feature'>
            <h3>🌍 Multiple Languages</h3>
            <p>Support for various languages</p>
        </div>
        <div class='feature'>
            <h3>✨ High Accuracy</h3>
            <p>Precise text recognition</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_text' not in st.session_state:
    st.session_state['processed_text'] = None

# Process image function
def process_image(uploaded_file):
    if uploaded_file:
        image = Image.open(uploaded_file)
        image_array = np.array(image)
        st.image(image, width=400, caption="Uploaded Image")

        if st.button("Extract Text"):
            with st.spinner("Processing..."):
                try:
                    result = reader.readtext(image_array, detail=0)
                    extracted_text = "\n".join(result)
                    st.session_state['processed_text'] = extracted_text
                except Exception as e:
                    st.error(f"Error processing image: {e}")

# File uploader
uploaded_file = st.file_uploader("Drop your image here or click to browse", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    process_image(uploaded_file)

if st.session_state['processed_text']:
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    st.text_area("Extracted Text", st.session_state['processed_text'], height=200)

    if st.button("Copy Text"):
        try:
            pyperclip.copy(st.session_state['processed_text'])
            st.success("Text copied to clipboard!")
        except Exception as e:
            st.error("Unable to copy to clipboard. Please copy manually.")

    if st.button("Try Another Image"):
        st.session_state.clear()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; color: #6b7280;'>
        <p>Upload any image containing text to extract its contents</p>
    </div>
""", unsafe_allow_html=True)
