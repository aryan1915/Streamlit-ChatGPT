import streamlit as st
from PIL import Image
import openai

openai.api_key = "sk-7WKeMzOt9vPM5nMb4jWJMTmcs58gxvJi7lVZx9OaCDT3BlbkFJXtKOt7JpMcKsikgn_DRKLSMvridabyqb76_tNhF9YA"

st.title("Enter Your Image and Prompt to GPT-4o_Mini Model")
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
user_prompt = st.text_input("Enter your prompt for the model:")

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if st.button("Submit"):
    if uploaded_image and user_prompt:
        response = openai.Completion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=150
        )
        
        st.subheader("Model's Response:")
        st.write(response.choices[0].text.strip())
    else:
        st.warning("Please upload an image and enter a prompt.")



