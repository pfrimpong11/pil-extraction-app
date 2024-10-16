from flask import Flask, request, jsonify
import pytesseract
import PIL.Image
import PyPDF2
import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

    FIll empty keys and arrays with N/A

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
        print(f"An error occurred: Please try again!", e)
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

    FIll empty keys and arrays with N/A

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
        print(f"An error occurred: Please try again!", e)
        return ""



# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() for page in pdf_reader.pages])


@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    file_type = file.content_type
    
    if file_type == "application/pdf":
        pdf_text = extract_text_from_pdf(file)
        # print(pdf_text)
        response = generate_PIL_information_pdf(pdf_text)

        # Clean up the response
        response = re.sub(r'```json|```', '', response).strip()
        response = response.replace('\n', '')

        # print(response)
        return jsonify(response)

    else:
        try:
            img = PIL.Image.open(file)
            extracted_text = pytesseract.image_to_string(img)
            if extracted_text.strip():
                # print(extracted_text)
                response = generate_PIL_information(img, extracted_text)

                # Clean up the response
                response = re.sub(r'```json|```', '', response).strip()
                response = response.replace('\n', '')

                # print(response)
                return jsonify(response)
            else:
                return jsonify({"error": "Could not extract text from the image"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
