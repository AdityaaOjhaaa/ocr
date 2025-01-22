import streamlit as st
import easyocr
from PIL import Image
import io

# Page config
st.set_page_config(page_title="Smart OCR Scanner", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# Header
st.title("Smart OCR Scanner")
st.markdown("Extract text from images instantly")

# File upload
uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Extract text
    if st.button('Extract Text'):
        with st.spinner('Processing...'):
            text = reader.readtext(uploaded_file, detail=0)
            extracted_text = " ".join(text)
            
            # Display results
            st.subheader("Extracted Text:")
            st.text_area("", extracted_text, height=200)
            
            # Copy button
            st.download_button(
                "Copy text",
                extracted_text,
                "extracted_text.txt",
                "text/plain"
            )
