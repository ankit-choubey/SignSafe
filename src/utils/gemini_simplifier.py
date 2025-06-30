import os
import logging
from typing import Dict, Optional, Union, Any
import google.generativeai as genai

class GeminiSimplifier:
    """Uses Gemini AI to simplify legal clauses in the shortest, simplest language."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Try both GOOGLE_API_KEY and GEMINI_API_KEY
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.logger.info("Gemini client initialized successfully")
            except Exception as e:
                self.model = None
                self.logger.error(f"Failed to initialize Gemini client: {str(e)}")
        else:
            self.model = None
            self.logger.warning("No API key found (GEMINI_API_KEY or GOOGLE_API_KEY)")
    
    def simplify_clause(self, clause_text: str, clause_type: str = "general") -> Dict[str, Any]:
        """Simplify a legal clause using Gemini AI."""
        if not self.model:
            error_msg = 'Gemini API not available. Please check your GOOGLE_API_KEY.'
            self.logger.error(error_msg)
            return {
                'simplified': clause_text,
                'error': error_msg
            }
        
        try:
            # Create a specific prompt for legal clause simplification
            prompt = f"""
You are a legal expert who explains complex legal language in the simplest terms possible.

Task: Simplify this {clause_type} legal clause into the shortest, simplest language that anyone can understand.

Legal Clause:
{clause_text}

Requirements:
1. Use only simple, everyday words
2. Make it as short as possible while keeping the meaning
3. Explain what the person must do or what happens to them
4. Use "you" instead of "the party" or "the customer"
5. No legal jargon at all

Provide only the simplified version, nothing else.
            """
            
            self.logger.info(f"Sending request to Gemini for clause type: {clause_type}")
            
            response = self.model.generate_content(prompt)
            
            self.logger.info(f"Received response from Gemini: {bool(response.text)}")
            
            if response.text:
                simplified = response.text.strip()
                
                # Clean up the response
                simplified = simplified.replace('"', '')
                simplified = simplified.replace('Simplified version:', '')
                simplified = simplified.replace('Simplified:', '')
                simplified = simplified.strip()
                
                self.logger.info(f"Successfully simplified clause: {len(simplified)} characters")
                
                return {
                    'simplified': simplified,
                    'success': True
                }
            else:
                error_msg = 'No response from Gemini API'
                self.logger.warning(error_msg)
                return {
                    'simplified': clause_text,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f'Gemini API error: {str(e)}'
            self.logger.error(error_msg)
            return {
                'simplified': clause_text,
                'error': error_msg
            }
    
    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        return self.model is not None and self.api_key is not None