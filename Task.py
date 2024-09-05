import streamlit as st
import pytesseract
import pandas as pd
import cv2
from PIL import Image
import numpy as np
import openai

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

openai.api_key = 'sk-ngYb40b5-jXR9jPeGylGoHUWKJvDfGOLYBgWaQop8qT3BlbkFJzX7EX37zuH_C934JzlHg5LkD0eC_rWuWg9eCa9DlwA'

def extract_table_from_image(image):

    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    custom_config = r'--oem 3 --psm 6'  
    extracted_text = pytesseract.image_to_string(gray, config=custom_config)

    lines = extracted_text.splitlines()
    data = [line.split() for line in lines if line.strip()]

    st.text("Extracted Data:")
    st.write(data)
    
    num_columns = max(len(row) for row in data)
    corrected_data = [row + [''] * (num_columns - len(row)) for row in data]
    column_names = corrected_data[0]
    clean_column_names = []
    seen = set()

    for i, col in enumerate(column_names):
        if not col:
            col = f"Unnamed_{i}"
        if col in seen:
            col = f"{col}_{i}"
        seen.add(col)
        clean_column_names.append(col)

    try:
        df = pd.DataFrame(corrected_data[1:], columns=clean_column_names)
    except ValueError as e:
        st.error(f"Error creating DataFrame: {e}")
        st.write("Corrected Data:")
        st.write(corrected_data)
        return None
    
    return df

def ask_gpt(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo", 
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

st.title("Enter Your Image")

uploaded_image = st.file_uploader("Upload a table image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:

    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    df = extract_table_from_image(image)
    
    if df is not None:
        st.subheader("Extracted Table Data")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='extracted_table.csv',
            mime='text/csv',
        )

st.subheader("ChatGPT 4.0 Mini")

user_prompt = st.text_input("Enter a prompt for ChatGPT:")

if user_prompt:
    with st.spinner('ChatGPT is thinking...'):
        gpt_response = ask_gpt(user_prompt)
    st.text_area("ChatGPT's Response:", gpt_response, )
