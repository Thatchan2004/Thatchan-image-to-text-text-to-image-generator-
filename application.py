import requests
import streamlit as st
from PIL import Image
import io

# Define API URLs and headers
STABLE_DIFFUSION_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
BLIP_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

def query_stable_diffusion(payload):
    response = requests.post(STABLE_DIFFUSION_API_URL, headers=headers, json=payload)
    return response.content

def query_blip(image_data):
    response = requests.post(BLIP_API_URL, headers=headers, data=image_data)
    return response.json()

# App title
st.title("Thatchan AI-Powered Image Processing")

# Sidebar for selecting options
option = st.sidebar.selectbox("Choose an option", ["Generate Image", "Caption Image"])

# Option 1: Generate Image using Stable Diffusion
if option == "Generate Image":
    st.header("Generate Image with Text")
    prompt = st.text_input("Enter prompt")
    
    if st.button('Generate'):
        if prompt:
            image_bytes = query_stable_diffusion({"inputs": prompt})
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.warning("Please enter a prompt to generate an image.")

# Option 2: Caption Image using BLIP
elif option == "Caption Image":
    st.header("Image Captioning")
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Read the image data
        image_data = uploaded_file.read()
        
        # Query the BLIP API
        caption = query_blip(image_data)
        
        # Display the caption
        st.write("Caption:", caption[0]['generated_text'])
