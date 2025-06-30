import os
import io
import logging
from typing import Optional, Union
import PyPDF2
import pytesseract
from PIL import Image
import streamlit as st

class OCRParser:
    """Handles text extraction from PDF and image files."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                    
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_image(self, file_path: str) -> str:
        """Extract text from image file using OCR."""
        try:
            image = Image.open(file_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            text = pytesseract.image_to_string(image)
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Error extracting text from image {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_uploaded_file(self, uploaded_file) -> str:
        """Extract text from Streamlit uploaded file object."""
        try:
            file_extension = uploaded_file.name.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                # Handle PDF
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
                
            elif file_extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                # Handle images
                image = Image.open(uploaded_file)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                text = pytesseract.image_to_string(image)
                return text.strip()
                
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            self.logger.error(f"Error extracting text from uploaded file: {str(e)}")
            return ""
    
    def process_file(self, file_path: str) -> str:
        """Process a file and extract text based on its type."""
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return ""
        
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
            return self.extract_text_from_image(file_path)
        else:
            self.logger.error(f"Unsupported file type: {file_extension}")
            return ""
    
    def validate_file_type(self, filename: str) -> bool:
        """Validate if file type is supported."""
        supported_extensions = ['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp']
        file_extension = filename.lower().split('.')[-1]
        return file_extension in supported_extensions
