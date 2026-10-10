
import streamlit as st
from PIL import Image
from google import genai

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="Gemini Vision Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------
# 2. CUSTOM CSS - BEAUTIFUL UI
# --------------------------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f0ff 0%,
        #edf4ff 50%,
        #fff0f7 100%
    );
}

/* Main content spacing */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main heading */
.hero-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #5632a8;
    margin-bottom: 8px;
}

/* Subtitle */
.hero-subtitle {
    text-align: center;
    font-size: 17px;
    color: #625d78;
    margin-bottom: 30px;
}

/* Feature cards */
.feature-card {
    background: rgba(255, 255, 255, 0.88);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e7ddff;
    box-shadow: 0 5px 20px rgba(79, 48, 130, 0.07);
    margin-bottom: 20px;
}

/* Upload section */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
    border: 1px dashed #9b7bea;
}

/* Text input */
.stTextInput input {
    border-radius: 12px;
    border: 1px solid #cbb9f7;
    padding: 12px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #7041d9, #a34fe8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    transition: all 0.2s ease;
    width: 100%;
}

/* Button hover */
.stButton > button:hover {
    background: linear-gradient(90deg, #5727bd, #8734d0);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(112, 65, 217, 0.25);
}

/* Image preview */
[data-testid="stImage"] img {
    border-radius: 16px;
}

/* Analysis response */
.response-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border-left: 5px solid #8052df;
    box-shadow: 0 5px 20px rgba(79, 48, 130, 0.08);
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #77718c;
    padding-top: 35px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# 3. GEMINI CONNECTION
# --------------------------------
try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API"]
    )
except Exception:
    st.error(
        "Gemini API configuration could not be loaded. "
        "Please check your Streamlit Secrets."
    )
    st.stop()

# --------------------------------
# 4. HEADER
# --------------------------------
st.markdown(
    '<div class="hero-title">✨ Gemini Vision Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Upload an image, ask a question, and discover more with AI.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="feature-card">
    <h3 style="color:#5632a8; margin-top:0;">
        🪄 Your AI Image Assistant
    </h3>
    <p style="color:#625d78; margin-bottom:0;">
        Analyze photographs, identify objects, understand scenes,
        and ask questions about your images.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# 5. IMAGE UPLOAD
# --------------------------------
st.subheader("📤 Upload Your Image")

image_file = st.file_uploader(
    "Choose a PNG, JPG, or JPEG image",
    type=["png", "jpg", "jpeg"],
    help="Select an image from your computer."
)

# --------------------------------
# 6. IMAGE PREVIEW AND PROMPT
# --------------------------------
if image_file is not None:

    try:
        image = Image.open(image_file)
        image.load()

        # Keep two columns for a professional layout
        image_col, prompt_col = st.columns(
            [1, 1],
            gap="large"
        )

        with image_col:
            st.markdown("### 🖼️ Image Preview")

            st.image(
                image,
                caption="Your uploaded image",
                use_container_width=True
            )

        with prompt_col:
            st.markdown("### 💬 Ask Gemini")

            prompt = st.text_input(
                "Your question",
                placeholder="Describe this image...",
                key="image_prompt"
            )

            st.markdown("""
            <p style="color:#625d78;">
                💡 Try asking:
                <br>• What is happening in this image?
                <br>• Describe the objects you see.
                <br>• What colors are present?
                <br>• Explain this image in detail.
            </p>
            """, unsafe_allow_html=True)

            analyze_button = st.button(
                "✨ Analyze My Image",
                use_container_width=True
            )

        # --------------------------------
        # 7. GEMINI IMAGE ANALYSIS
        # --------------------------------
        if analyze_button:

            if prompt.strip():

                try:
                    with st.spinner(
                        "🔮 Gemini is analyzing your image..."
                    ):
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[prompt.strip(), image]
                        )

                    if response.text:
                        st.markdown("---")
                        st.markdown("## ✨ AI Analysis")

                        st.markdown(
                            '<div class="response-card">'
                            '<h3 style="color:#5632a8;">'
                            '🤖 Gemini Response'
                            '</h3>'
                            '</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(response.text)

                        st.success(
                            "Your image analysis is complete!"
                        )
                    else:
                        st.warning(
                            "Gemini returned no text. "
                            "Please try another question."
                        )

                except Exception:
                    st.error(
                        "Gemini could not analyze the image. "
                        "Please check your API quota and connection, "
                        "then try again."
                    )

            else:
                st.warning(
                    "Please enter a question before analyzing."
                )

    except Exception:
        st.error(
            "This image could not be opened. "
            "Please upload a valid PNG, JPG, or JPEG image."
        )

else:
    st.info(
        "👆 Start by uploading an image to unlock the AI analyzer."
    )

# --------------------------------
# 8. FOOTER
# --------------------------------
st.markdown("""
<div class="footer">
    Built with 💜 Streamlit and Google Gemini AI
    <br>
    Your imagination, powered by AI ✨
</div>
""", unsafe_allow_html=True)
