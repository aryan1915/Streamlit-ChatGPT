import streamlit as st
from PIL import Image
import openai

openai.api_key = "sk-7WKeMzOt9vPM5nMb4jWJMTmcs58gxvJi7lVZx9OaCDT3BlbkFJXtKOt7JpMcKsikgn_DRKLSMvridabyqb76_tNhF9YA"

st.title("Enter Your Image")
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

static_prompt = "You are an AI assistant tasked with analyzing a table image and extracting its contents into a CSV format. The table is filled with information about people. Your goal is to understand the table structure, extract column names and their corresponding values, and output the data in CSV format. Pay close attention to preserving the table hierarchy and detecting handwritten English text. Do not give pretext, explaination or any other text than csv. I want all fields even if blank. Only one row should be there. Here is the table image you need to analyze: <table_image>ATTACHED </table_image> "

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
if st.button("Submit"):
    if uploaded_image:
        response = openai.Completion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "user", "content": static_prompt}
            ],
            max_tokens=150
        )
        
        st.subheader("Model's Response:")
        st.write(response.choices[0].text.strip())
    else:
        st.warning("Please upload an image.")
