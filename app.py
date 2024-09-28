import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
import os
import streamlit as st
import pytesseract
import re
import json
import PyPDF2

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Function to generate PIL information using the image and description
def generate_PIL_information(img, description):
    prompt = f"""
    Hey! Act as a PIL (Patient Information Leaflet) expert with diverse experiences in pharmacy and drugs.
    I will provide you with an image of a PIL and an extracted text from the same PIL.
    Your task is to provide this information about the PIL:

    Drug name: Name of the drug.
    Intended use: The specific conditions or diseases the drug is meant to treat.
    Dosage: The recommended amount and frequency of use.
    Side effects: Potential side effects that may occur.
    Precautions: Warnings or precautions to be aware of.
    Interactions: Possible interactions with other drugs or substances.
    Storage: How to store the medication properly.
    Expiration date: The date by which the medication should be used.

    Respond with a JSON string structured as follows:
    {{
        "DrugName": "",
        "IntendedUse": [],
        "Dosage": "",
        "SideEffects": [],
        "Precautions": [],
        "Interactions": [],
        "Storage": "",
        "ExpirationDate": ""
    }}
    """
    
    # Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    try:
        response = model.generate_content([prompt, img, description])

        # Access response candidates 
        if hasattr(response, "candidates") and len(response.candidates) > 0:
            candidate = response.candidates[0]

            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                parts = candidate.content.parts
                if len(parts) > 0 and hasattr(parts[0], "text"):
                    # Joining text from all parts
                    extracted_text = " ".join(part.text for part in parts)
                    return extracted_text
                else:
                    return ""
            else:
                return ""
        else:
            return response.text
    except Exception as e:
        st.error(f"An error occurred: Please try again!")
        return ""



# Function to generate PIL information using pdf
def generate_PIL_information_pdf(pdf_text):
    prompt = f"""
    Hey! Act as a PIL (Patient Information Leaflet) expert with diverse experiences in pharmacy and drugs.
    I will provide you with text extracted from a PIL pdf file.
    Your task is to provide this information about the PIL:

    Drug name: Name of the drug.
    Intended use: The specific conditions or diseases the drug is meant to treat.
    Dosage: The recommended amount and frequency of use.
    Side effects: Potential side effects that may occur.
    Precautions: Warnings or precautions to be aware of.
    Interactions: Possible interactions with other drugs or substances.
    Storage: How to store the medication properly.
    Expiration date: The date by which the medication should be used.

    Respond with a JSON string structured as follows:
    {{
        "DrugName": "",
        "IntendedUse": [],
        "Dosage": "",
        "SideEffects": [],
        "Precautions": [],
        "Interactions": [],
        "Storage": "",
        "ExpirationDate": ""
    }}
    """
    
    # Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    try:
        response = model.generate_content([prompt, pdf_text])

        # Access response candidates 
        if hasattr(response, "candidates") and len(response.candidates) > 0:
            candidate = response.candidates[0]

            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                parts = candidate.content.parts
                if len(parts) > 0 and hasattr(parts[0], "text"):
                    # Joining text from all parts
                    extracted_text = " ".join(part.text for part in parts)
                    return extracted_text
                else:
                    return ""
            else:
                return ""
        else:
            return response.text
    except Exception as e:
        st.error(f"An error occurred: Please try again!")
        return ""




def display_response(response):
    st.subheader("PIL Information")

    # Clean up the response
    response = re.sub(r'```json|```', '', response).strip()

    try:
        drug_information = json.loads(response)

        # Drug name
        st.subheader("Drug Name:")
        drugName = drug_information.get("DrugName","")
        if drugName:
            st.write(drugName)
        else:
            st.write("No Drug name section found on the uploaded PIL image.")

        # Intended Use
        st.subheader("Intended Use:")
        intendedUse = drug_information.get("IntendedUse", [])
        if intendedUse:
            for use in intendedUse:
                st.write("- ", use)
        else:
            st.write("No Intended use section found on the uploaded PIL image.")

        # Dosage
        st.subheader("Dosage:")
        dosage = drug_information.get("Dosage","")
        if dosage:
            st.write(dosage)
        else:
            st.write("No Dosage section found on the uploaded PIL image.")

        # Side effects
        st.subheader("Side Effects:")
        sideEffect = drug_information.get("SideEffects", [])
        if sideEffect:
            for effect in sideEffect:
                st.write("- ", effect)
        else:
            st.write("No side effects section found on the uploaded PIL image")

        # Precautions
        st.subheader("Precautions:")
        precautions = drug_information.get("Precautions", [])
        if precautions:
            for precaution in precautions:
                st.write("- ", precaution)
        else:
            st.write("No Precautions section found on the uploaded PIL image")

        # Interactions
        st.subheader("Interactions:")
        interactions = drug_information.get("Interactions", [])
        if interactions:
            for interaction in interactions:
                st.write("- ", interaction)
        else:
            st.write("No Interactions section found on the uploaded PIL image")

        # Storage
        st.subheader("Storage:")
        storage = drug_information.get("Storage","")
        if storage:
            st.write(storage)
        else:
            st.write("No Storage section found on the uploaded PIL image.")

        # Expiration date
        st.subheader("Expiration Date:")
        expirationDate = drug_information.get("ExpirationDate","")
        if expirationDate:
            st.write(expirationDate)
        else:
            st.write("No expiration date section found on the uploaded PIL image.")

    except json.JSONDecodeError as e:
        st.error("An error occurred. Please try again!")



# web app
def main():
    st.title("PIL Extractor App")
    st.subheader("Welcome to the PIL Extractor App!")
    st.write("""
        With this app, you can easily extract important drug information from Patient Information Leaflets (PILs). 
        Simply upload an image or PDF of a PIL, and and let the app handle the rest!
        """)

    # File uploader for the image
    upload_file = st.file_uploader('Upload PIL Image', type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if upload_file is not None:
        
        if upload_file.type =="application/pdf":
            pdf_reader = PyPDF2.PdfReader(upload_file)
            pdf_text = "".join([page.extract_text() for page in pdf_reader.pages])

            response = generate_PIL_information_pdf(pdf_text)
            # display response/ results
            display_response(response)

        else:
            img = PIL.Image.open(upload_file)
            
            # Display the uploaded image
            st.image(img, caption="Uploaded PIL Image", use_column_width=True)

            # Extract text from the image using pytesseract
            extracted_text = pytesseract.image_to_string(img)

            if extracted_text.strip():  # Ensure that some text has been extracted
                response = generate_PIL_information(img, extracted_text)
                # Display results/response
                display_response(response)
            else:
                st.write("Could not extract text from the image.")

if __name__ == "__main__":
    main()
