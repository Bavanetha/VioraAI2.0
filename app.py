import requests
import streamlit as st
import io
from PIL import Image

API_URL_img = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_URL_cap = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

st.title("VioraAI 2.0")

# Navigation options
nav_option = st.sidebar.radio("Choose a task", ("Image Generator", "Image Caption Generator"))

if nav_option == "Image Generator":
    def img_query(payload):
        response = requests.post(API_URL_img, headers=headers, json=payload)
        return response.content
    
    image_bytes = img_query({
        "inputs": st.text_input("Enter the prompt"),
    })
    # You can access the image with PIL.Image for example

    if(st.button("Generate")):
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image)
        # Convert image to bytes for saving
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)


            # Add a save/download button
        st.download_button(
                label="Save Image",
                data=img_buffer,
                file_name="generated_image.png",
                mime="image/png"
        )
        image = Image.open(io.BytesIO(image_bytes))


elif nav_option == "Image Caption Generator":

    def query(filename):
        
        image_data = filename.read()
        response = requests.post(API_URL_cap, headers=headers, data=image_data)
        return response.json()


    img = st.file_uploader("Upload a image" , type = "jpg")

    if(img):
        output = query(img)
        st.image(img,width=400)
        st.write(output[0]['generated_text'])

