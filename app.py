import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import io
from PIL import Image
import pdf2image
import base64

import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel("gemini-pro-vision")

    response = model.generate_content([prompt,pdf_content[0],input])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        image = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path="C:/Program Files/poppler/Release-24.02.0-0/poppler-24.02.0/Library/bin")


        first_page = image[0]


        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()

            }

        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file Uploaded")



st.set_page_config(
    page_title = 'ATS RESUME FILTER',
    layout = "centered"
)
input_text = st.text_area(label= "Enter the Job Description",height=30)

uploaded_file = st.file_uploader("Upload your Resume",type=['PDF'])


type_of = st.selectbox(label="Select what do you want",options=['Analyse Your Resume','What skills do i require?','percentage of getting job'],index=None)
if uploaded_file:
    if type_of == "Analyse Your Resume" :
        input_prompt = """
         You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
          Please share your professional evaluation on whether the candidate's profile aligns with the role.
         Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """
        image_generated = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text,image_generated,input_prompt)
        st.success(response)

    if type_of == "What skills do i require?":
        input_prompt = """"
        You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description.
        Please share your professional evaluation on whether the candidate's profile aligns with the role.
        And please tell him what all the skills he should require to crack the job easily
        """
        image_generated = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, image_generated, input_prompt)
        st.success(response)






    if type_of == 'percentage of getting job':
        input_prompt = """
        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
        the job description. First the output should come as percentage and then keywords missing and last final thoughts.
        """
        image_generated = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, image_generated, input_prompt)
        st.success(response)























