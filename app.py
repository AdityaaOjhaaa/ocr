import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import base64

# Page configuration
st.set_page_config(page_title="Smart OCR Scanner", layout="wide")

# Custom CSS for UI styling
st.markdown("""
    <style>
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
        text-align: center;
    }
    .result-container {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize EasyOCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# App header
st.title("Smart OCR Scanner")
st.subheader("Extract text from images instantly")

# Initialize session state
if 'processed_text' not in st.session_state:
    st.session_state['processed_text'] = None

# Helper: Reset session state
def reset_state():
    st.session_state['processed_text'] = None

# Helper: Copy to clipboard using JavaScript
def copy_to_clipboard(text):
    b64_text = base64.b64encode(text.encode()).decode()
    st.markdown(f"""
        <script>
        navigator.clipboard.writeText(atob("{b64_text}")).then(() => {{
            alert('Text copied to clipboard!');
        }}).catch(err => {{
            console.error('Could not copy text: ', err);
        }});
        </script>
    """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])

# OCR processing
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)
    
    if st.button("Extract Text"):
        with st.spinner("Processing..."):
            try:
                image_array = np.array(image)
                result = reader.readtext(image_array, detail=0)
                extracted_text = "\n".join(result)
                st.session_state['processed_text'] = extracted_text
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")

# Display extracted text and options
if st.session_state['processed_text']:
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    st.text_area("Extracted Text", st.session_state['processed_text'], height=200)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Copy Text"):
            copy_to_clipboard(st.session_state['processed_text'])
    with col2:
        if st.button("Try Another Image"):
            reset_state()  # Clear processed text
            st.experimental_rerun()  # Reload app components

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.write("Upload an image containing text, and the OCR scanner will extract it for you!")
