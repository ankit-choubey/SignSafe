import re
import logging
from typing import List, Dict, Tuple

class ClauseSplitter:
    """Splits legal documents into individual clauses and categorizes them."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Common section headers that indicate clause boundaries
        self.section_patterns = [
            r'\b(?:SECTION|Section|SEC\.|Sec\.)\s+\d+',
            r'\b(?:ARTICLE|Article|ART\.|Art\.)\s+\d+',
            r'\b(?:CLAUSE|Clause)\s+\d+',
            r'^\d+\.\s+',
            r'^\(\d+\)\s+',
            r'^[A-Z]\.\s+',
            r'^\([a-z]\)\s+',
            r'WHEREAS,',
            r'NOW THEREFORE,',
            r'IN WITNESS WHEREOF',
            r'TERMINATION',
            r'LIABILITY',
            r'WARRANTY',
            r'CONFIDENTIALITY',
            r'INTELLECTUAL PROPERTY',
            r'PAYMENT',
            r'DISPUTE RESOLUTION'
        ]
        
        # Clause type keywords
        self.clause_types = {
            'liability': [
                'liability', 'liable', 'damages', 'indemnify', 'indemnification',
                'hold harmless', 'limitation of liability', 'exclude liability'
            ],
            'termination': [
                'termination', 'terminate', 'end', 'expire', 'dissolution',
                'breach', 'default', 'cancel', 'cancellation'
            ],
            'warranty': [
                'warranty', 'warrant', 'guarantee', 'representation',
                'covenant', 'assurance', 'promise'
            ],
            'financial': [
                'payment', 'fee', 'cost', 'price', 'compensation',
                'billing', 'invoice', 'salary', 'wage', 'money'
            ],
            'confidentiality': [
                'confidential', 'confidentiality', 'non-disclosure', 'nda',
                'proprietary', 'trade secret', 'secret information'
            ],
            'intellectual_property': [
                'intellectual property', 'copyright', 'patent', 'trademark',
                'trade mark', 'proprietary rights', 'work for hire'
            ],
            'dispute_resolution': [
                'dispute', 'arbitration', 'mediation', 'court', 'jurisdiction',
                'governing law', 'venue', 'litigation'
            ]
        }
        
        # Importance indicators
        self.importance_keywords = {
            'high': [
                'shall', 'must', 'required', 'mandatory', 'obligation',
                'liable', 'responsible', 'penalty', 'breach', 'default'
            ],
            'medium': [
                'should', 'may', 'can', 'will', 'agree', 'covenant',
                'undertake', 'consent', 'approve'
            ]
        }
    
    def split_into_clauses(self, text: str) -> List[Dict[str, str]]:
        """Split document text into individual clauses."""
        try:
            # Clean and normalize text
            cleaned_text = self._clean_text(text)
            
            # Split into potential clauses
            raw_clauses = self._split_by_patterns(cleaned_text)
            
            # Process and categorize each clause
            processed_clauses = []
            
            for i, clause_text in enumerate(raw_clauses):
                if len(clause_text.strip()) > 50:  # Filter out very short clauses
                    clause = self._process_clause(clause_text, i)
                    processed_clauses.append(clause)
            
            return processed_clauses
            
        except Exception as e:
            self.logger.error(f"Error splitting clauses: {str(e)}")
            # Return entire text as single clause if splitting fails
            return [{
                'id': 1,
                'text': text,
                'type': 'general',
                'importance': 'medium',
                'original': text
            }]
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Normalize punctuation
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\2', text)
        
        return text.strip()
    
    def _split_by_patterns(self, text: str) -> List[str]:
        """Split text using section patterns."""
        # Create a combined pattern for all section indicators
        combined_pattern = '|'.join(self.section_patterns)
        
        # Split the text
        parts = re.split(f'({combined_pattern})', text, flags=re.IGNORECASE | re.MULTILINE)
        
        # Combine headers with their content
        clauses = []
        current_clause = ""
        
        for part in parts:
            part = part.strip()
            if part:
                if re.match(combined_pattern, part, re.IGNORECASE):
                    # This is a header - start new clause
                    if current_clause:
                        clauses.append(current_clause)
                    current_clause = part + " "
                else:
                    # This is content - add to current clause
                    current_clause += part + " "
        
        # Add the last clause
        if current_clause:
            clauses.append(current_clause)
        
        # If no patterns found, split by sentences/paragraphs
        if len(clauses) <= 1:
            clauses = self._split_by_sentences(text)
        
        return clauses
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Fallback method to split by sentences if no patterns found."""
        # Split by double newlines (paragraphs) first
        paragraphs = re.split(r'\n\s*\n', text)
        
        clauses = []
        for paragraph in paragraphs:
            # If paragraph is too long, split by sentences
            if len(paragraph) > 500:
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                
                # Group sentences into reasonable clause sizes
                current_clause = ""
                for sentence in sentences:
                    if len(current_clause + sentence) > 300 and current_clause:
                        clauses.append(current_clause.strip())
                        current_clause = sentence + " "
                    else:
                        current_clause += sentence + " "
                
                if current_clause:
                    clauses.append(current_clause.strip())
            else:
                clauses.append(paragraph.strip())
        
        return [c for c in clauses if len(c.strip()) > 50]
    
    def _process_clause(self, clause_text: str, clause_id: int) -> Dict[str, str]:
        """Process and categorize a single clause."""
        clause_type = self._determine_clause_type(clause_text)
        importance = self._determine_importance(clause_text)
        
        return {
            'id': clause_id + 1,
            'text': clause_text.strip(),
            'type': clause_type,
            'importance': importance,
            'original': clause_text.strip()
        }
    
    def _determine_clause_type(self, text: str) -> str:
        """Determine the type of clause based on keywords."""
        text_lower = text.lower()
        
        # Count matches for each type
        type_scores = {}
        
        for clause_type, keywords in self.clause_types.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            type_scores[clause_type] = score
        
        # Return the type with highest score
        if type_scores and max(type_scores.values()) > 0:
            return max(type_scores, key=type_scores.get)
        
        return 'general'
    
    def _determine_importance(self, text: str) -> str:
        """Determine the importance level of a clause."""
        text_lower = text.lower()
        
        high_score = sum(1 for keyword in self.importance_keywords['high'] if keyword in text_lower)
        medium_score = sum(1 for keyword in self.importance_keywords['medium'] if keyword in text_lower)
        
        if high_score > 0:
            return 'high'
        elif medium_score > 0:
            return 'medium'
        else:
            return 'low'
    
    def get_clause_summary(self, clauses: List[Dict[str, str]]) -> Dict[str, any]:
        """Generate a summary of clauses by type and importance."""
        summary = {
            'total_clauses': len(clauses),
            'by_type': {},
            'by_importance': {},
            'type_distribution': {}
        }
        
        # Count by type
        for clause in clauses:
            clause_type = clause.get('type', 'general')
            importance = clause.get('importance', 'low')
            
            # Count by type
            summary['by_type'][clause_type] = summary['by_type'].get(clause_type, 0) + 1
            
            # Count by importance
            summary['by_importance'][importance] = summary['by_importance'].get(importance, 0) + 1
        
        # Calculate type distribution percentages
        total = len(clauses)
        for clause_type, count in summary['by_type'].items():
            summary['type_distribution'][clause_type] = round((count / total) * 100, 1)
        
        return summary
