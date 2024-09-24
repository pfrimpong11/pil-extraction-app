
# PIL Information Extraction Web App

This project is a web-based application built with `Streamlit` for generating information from Patient Information Leaflets (PILs). The application allows users to upload images or PDF files of PILs, from which it extracts text and uses a Generative AI model to identify relevant drug information. 

The generated information includes:
- **Drug Name**
- **Intended Use**
- **Dosage**
- **Side Effects**
- **Precautions**
- **Interactions**
- **Storage Instructions**
- **Expiration Date**

## Features
- Upload PIL as an image (`PNG`, `JPG`, or `JPEG`) or PDF.
- Extract text from the PIL using OCR (`pytesseract`).
- For PDFs, extract text using `PyPDF2`.
- Use Google Generative AI to extract relevant drug information from the PIL text.
- Display extracted information in an easy-to-read format.
  
## Requirements

Before you start, ensure you have `Python` installed on your system.

### Python Libraries
To run this project, you will need to install the following Python libraries:

```bash
pip install streamlit google-generativeai pytesseract python-dotenv pillow PyPDF2
```

### Additional Requirements

#### Tesseract OCR:
For text extraction from images, Tesseract OCR must be installed separately. You can install it as follows:

1. **Windows:**
   Download and install the [Tesseract Windows installer](https://github.com/UB-Mannheim/tesseract/wiki).

2. **Linux:**
   Install using the package manager:
   ```bash
   sudo apt install tesseract-ocr
   ```

3. **MacOS:**
   Install using `brew`:
   ```bash
   brew install tesseract
   ```

#### Google Generative AI:
To access Google Generative AI, you need to configure an API key in a `.env` file. Create a `.env` file in the project root directory with the following content:

```
API_KEY=your_google_generative_ai_api_key
```

Replace `your_google_generative_ai_api_key` with the actual API key.

## Running the Project

1. Clone this repository:
   ```bash
   git clone https://github.com/pfrimpong11/pil-extraction-app.git
   cd pil-extraction-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open the provided link in your browser to interact with the app.

## Usage

1. Upload a PIL image (PNG, JPG, JPEG) or PDF.
2. The app will extract the text and generate the relevant drug information.
3. Review the extracted data such as drug name, dosage, and side effects.

## Example

![App Screenshot](app_screenshot.png)


---

**Enjoy using the PIL Information Extraction Web App!**

