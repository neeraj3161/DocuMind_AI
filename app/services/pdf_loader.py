from typing import Any

import pdfplumber
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    length_per_page = 0
    for page in reader.pages:
        try:
            page_text = page.get_object().extract_text()
            if page_text:
                text += page_text + "\n"
                if length_per_page == 0:
                    length_per_page += len(page_text)
        except Exception as e:
            print("Skipping problematic page:", e)
            continue
    print('Extracted text length:', len(text))
    if len(text) == 0:
        extract_text_from_pdf_with_pdfplumber(file_path)
    return text

def extract_text_from_pdf_with_pdfplumber(file_path: str):
    try:
        # created a fallback if something fails
        print('Extracting text from PDF plumber')
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages])
    except Exception as e:
        print("Skipping problematic page:", e)