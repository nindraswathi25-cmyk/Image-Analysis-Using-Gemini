
import streamlit as st
from PIL import Image
from google import genai

# Read the API key securely from Streamlit Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API"])

st.title("Gemini Image Analyzer")
st.write("Upload an image and ask Gemini a question about it.")

image_file = st.file_uploader(
    "Choose an image",
    type=["png", "jpg", "jpeg"]
)

if image_file is not None:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    prompt = st.text_input("Enter your prompt")

    if st.button("Response"):
        if prompt.strip():
            try:
                with st.spinner("Gemini is analyzing your image..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[prompt, image]
                    )

                st.success("Gemini's Response")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")

