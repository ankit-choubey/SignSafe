# pipeline/ocr_parser.py

import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

def extract_text(file_path: str) -> str:
    text_output = ""

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text_output += page.get_text()
    elif ext in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file_path)
        text_output = pytesseract.image_to_string(image)
    else:
        raise ValueError("Unsupported file type: " + ext)

    return text_output.strip()
