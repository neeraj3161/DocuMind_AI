from typing import Any

from pypdf import PdfReader

def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""
    length_per_page = 0
    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                if length_per_page == 0:
                    length_per_page += len(page_text)
        except Exception as e:
            print("Skipping problematic page:", e)
            continue
    print('Extracted text length:', len(text))
    return text