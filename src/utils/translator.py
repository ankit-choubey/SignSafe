"""
Multi-language translator for legal documents
Supports Hindi and other Indian regional languages
"""

import os
import logging
import time
from typing import Dict, Optional, List
import google.generativeai as genai

class MultiLanguageTranslator:
    """Translates legal documents to Indian regional languages using Gemini AI."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.last_request_time = 0
        self.min_request_interval = 5  # 5 seconds between requests to avoid rate limits
        self.supported_languages = {
            'hindi': 'हिंदी',
            'tamil': 'தமிழ்',
            'telugu': 'తెలుగు',
            'bengali': 'বাংলা',
            'marathi': 'मराठी',
            'gujarati': 'ગુજરાતી',
            'kannada': 'ಕನ್ನಡ',
            'malayalam': 'മലയാളം',
            'punjabi': 'ਪੰਜਾਬੀ',
            'urdu': 'اردو',
            'odia': 'ଓଡ଼ିଆ',
            'assamese': 'অসমীয়া'
        }
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Gemini AI client."""
        try:
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai
                self.logger.info("Translator initialized successfully")
            else:
                self.logger.warning("GEMINI_API_KEY not found")
        except Exception as e:
            self.logger.error(f"Failed to initialize translator: {e}")
    
    def is_available(self) -> bool:
        """Check if translator is available."""
        return self.client is not None
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages."""
        return self.supported_languages.copy()
    
    def _wait_for_rate_limit(self):
        """Wait to avoid rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last_request
            self.logger.info(f"Rate limiting: waiting {wait_time:.1f} seconds")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()

    def translate_text(self, text: str, target_language: str, context: str = "legal") -> Dict[str, any]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'hindi', 'tamil')
            context: Context for translation (legal, general, etc.)
        
        Returns:
            Dictionary with translated text or error message
        """
        if not self.is_available():
            return {"error": "Translator not available. Please check GEMINI_API_KEY."}
        
        if target_language not in self.supported_languages:
            return {"error": f"Language '{target_language}' not supported."}
        
        try:
            # Apply rate limiting
            self._wait_for_rate_limit()
            
            # Create translation prompt
            language_name = self.supported_languages[target_language]
            
            prompt = f"""
            You are a professional legal translator specializing in Indian languages.
            
            Task: Translate the following English legal text to {language_name} ({target_language}).
            
            Requirements:
            1. Maintain legal accuracy and meaning
            2. Use appropriate legal terminology in {language_name}
            3. Keep the translation clear and understandable
            4. Preserve important legal concepts
            5. Make it accessible to common people
            
            Context: This is a {context} document clause.
            
            English Text:
            {text}
            
            Please provide only the translation in {language_name}, without any explanations or additional text.
            """
            
            self.logger.info(f"Translating to {target_language}: {len(text)} characters")
            
            model = self.client.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,  # Low temperature for consistent translations
                    "max_output_tokens": 2048
                }
            )
            
            if response.text:
                translated_text = response.text.strip()
                self.logger.info(f"Translation successful: {len(translated_text)} characters")
                
                return {
                    "translated": translated_text,
                    "source_language": "english",
                    "target_language": target_language,
                    "language_name": language_name,
                    "original_length": len(text),
                    "translated_length": len(translated_text)
                }
            else:
                return {"error": "No translation received from AI"}
                
        except Exception as e:
            error_msg = f"Translation failed: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def translate_clause(self, clause: Dict[str, any], target_language: str) -> Dict[str, any]:
        """
        Translate a complete clause with all its components.
        
        Args:
            clause: Clause dictionary with 'original', 'explanation', etc.
            target_language: Target language code
        
        Returns:
            Dictionary with translated clause components
        """
        if not self.is_available():
            return {"error": "Translator not available"}
        
        translated_clause = clause.copy()
        
        # Translate original text
        if clause.get('original'):
            result = self.translate_text(
                clause['original'], 
                target_language, 
                clause.get('type', 'legal')
            )
            if 'error' in result:
                return result
            translated_clause['original_translated'] = result['translated']
        
        # Translate explanation
        if clause.get('explanation'):
            result = self.translate_text(
                clause['explanation'], 
                target_language, 
                'explanation'
            )
            if 'error' not in result:
                translated_clause['explanation_translated'] = result['translated']
        
        # Translate simplified version if available
        if clause.get('simplified'):
            result = self.translate_text(
                clause['simplified'], 
                target_language, 
                'simplified'
            )
            if 'error' not in result:
                translated_clause['simplified_translated'] = result['translated']
        
        # Translate recommendations
        if clause.get('recommendations'):
            translated_recommendations = []
            for rec in clause['recommendations']:
                result = self.translate_text(rec, target_language, 'recommendation')
                if 'error' not in result:
                    translated_recommendations.append(result['translated'])
                else:
                    translated_recommendations.append(rec)  # Keep original if translation fails
            translated_clause['recommendations_translated'] = translated_recommendations
        
        # Translate warnings
        if clause.get('warnings'):
            translated_warnings = []
            for warning in clause['warnings']:
                result = self.translate_text(warning, target_language, 'warning')
                if 'error' not in result:
                    translated_warnings.append(result['translated'])
                else:
                    translated_warnings.append(warning)  # Keep original if translation fails
            translated_clause['warnings_translated'] = translated_warnings
        
        translated_clause['translation_language'] = target_language
        translated_clause['language_name'] = self.supported_languages[target_language]
        
        return translated_clause
    
    def translate_document_clauses(self, clauses: List[Dict[str, any]], target_language: str) -> List[Dict[str, any]]:
        """
        Translate multiple clauses with improved rate limiting and error handling.
        
        Args:
            clauses: List of clause dictionaries
            target_language: Target language code
        
        Returns:
            List of translated clauses
        """
        if not self.is_available():
            self.logger.warning("Translator not available, returning original clauses")
            return clauses
        
        translated_clauses = []
        total_clauses = len(clauses)
        
        for i, clause in enumerate(clauses):
            try:
                self.logger.info(f"Translating clause {i+1}/{total_clauses}")
                
                # Translate only the most important fields to reduce API calls
                translated_clause = clause.copy()
                
                # Translate original text (most important)
                if clause.get('original'):
                    result = self.translate_text(
                        clause['original'], 
                        target_language, 
                        clause.get('type', 'legal')
                    )
                    if 'error' not in result:
                        translated_clause['original_translated'] = result['translated']
                    else:
                        self.logger.warning(f"Failed to translate clause {i+1} original text: {result.get('error')}")
                
                # Translate simplified version if available (second priority)
                if clause.get('simplified'):
                    result = self.translate_text(
                        clause['simplified'], 
                        target_language, 
                        'simplified'
                    )
                    if 'error' not in result:
                        translated_clause['simplified_translated'] = result['translated']
                    else:
                        self.logger.warning(f"Failed to translate clause {i+1} simplified text")
                
                # Translate explanation if available (third priority)
                if clause.get('explanation'):
                    result = self.translate_text(
                        clause['explanation'], 
                        target_language, 
                        'explanation'
                    )
                    if 'error' not in result:
                        translated_clause['explanation_translated'] = result['translated']
                    else:
                        self.logger.warning(f"Failed to translate clause {i+1} explanation")
                
                translated_clause['translation_language'] = target_language
                translated_clause['language_name'] = self.supported_languages[target_language]
                translated_clauses.append(translated_clause)
                
            except Exception as e:
                self.logger.error(f"Error translating clause {i+1}: {str(e)}")
                # Add original clause if translation fails
                translated_clauses.append(clause)
        
        return translated_clauses
    
    def batch_translate_clauses(self, clauses: List[Dict], target_language: str) -> List[Dict]:
        """
        Translate multiple clauses with rate limiting.
        
        Args:
            clauses: List of clause dictionaries
            target_language: Target language code
        
        Returns:
            List of translated clauses
        """
        translated_clauses = []
        
        for i, clause in enumerate(clauses):
            self.logger.info(f"Translating clause {i+1}/{len(clauses)}")
            
            translated_clause = self.translate_clause(clause, target_language)
            translated_clauses.append(translated_clause)
            
            # Add small delay to avoid rate limiting
            import time
            time.sleep(0.5)
        
        return translated_clauses