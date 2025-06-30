import os
import requests
import logging
import time
from typing import Dict, Optional

class LegalSimplifier:
    """Uses Omnidimension API to simplify complex legal language."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv("OMNIDIMENSION_API_KEY", "")
        self.base_url = "https://api.omnidimension.ai/v1"
        
        # Simple word replacements for easier reading
        self.simplification_patterns = {
            'heretofore': 'until now',
            'hereinafter': 'from now on',
            'whereas': 'since',
            'pursuant to': 'following',
            'notwithstanding': 'even though',
            'aforementioned': 'mentioned above',
            'subsequent to': 'after',
            'prior to': 'before',
            'in the event that': 'if',
            'for the purpose of': 'to',
            'with respect to': 'about',
            'in accordance with': 'following',
            'terminate': 'end',
            'commence': 'start',
            'constitute': 'make',
            'obtain': 'get',
            'provide': 'give',
            'utilize': 'use',
            'endeavor': 'try',
            'sufficient': 'enough',
            'additional': 'extra',
            'modification': 'change',
            'notification': 'notice',
            'compensation': 'payment',
            'obligations': 'things you must do',
            'representations': 'claims',
            'warranties': 'promises',
            'indemnification': 'paying for someone else\'s problems',
            'force majeure': 'things no one can control',
            'liability': 'responsibility for problems',
            'breach': 'breaking the rules',
            'covenant': 'promise',
            'consideration': 'payment',
            'execute': 'sign',
            'party': 'person or company',
            'shall': 'must',
            'may': 'can',
        }
    
    def simplify_clause(self, clause_text: str, clause_type: str = "general") -> Dict[str, any]:
        """Simplify a legal clause using AI or fallback methods."""
        result = {
            'original': clause_text,
            'simplified': '',
            'explanation': '',
            'confidence': 0.0,
            'method': 'fallback'
        }
        
        try:
            # Try AI simplification first
            if self.api_key:
                ai_result = self._simplify_with_ai(clause_text, clause_type)
                if ai_result:
                    result.update(ai_result)
                    result['method'] = 'ai'
                    return result
            
            # Fallback to pattern-based simplification
            simplified = self._simplify_with_patterns(clause_text)
            result['simplified'] = simplified
            result['explanation'] = self._generate_explanation(clause_text, clause_type)
            result['recommendation'] = self._generate_simple_recommendation(clause_type)
            result['confidence'] = 0.7 if simplified != clause_text else 0.3
            
        except Exception as e:
            self.logger.error(f"Error simplifying clause: {str(e)}")
            result['simplified'] = clause_text
            result['explanation'] = "Could not simplify this clause."
            result['recommendation'] = "Ask someone to help explain this."
            result['confidence'] = 0.0
        
        return result
    
    def _simplify_with_ai(self, clause_text: str, clause_type: str) -> Optional[Dict[str, any]]:
        """Use Omnidimension API to simplify legal text."""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""
            Simplify this legal clause for someone with no legal knowledge. Use very simple words and short sentences.
            
            Original: {clause_text}
            
            Please provide:
            1. EXPLANATION: What does this mean in everyday language? (1-2 sentences max)
            2. SIMPLIFIED: Rewrite using simple words only (2-3 sentences max)
            3. RECOMMENDATION: What should the person do about this? (1 simple sentence)
            
            Use words a 12-year-old would understand. No legal terms.
            """
            
            payload = {
                'model': 'gpt-4',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are helping everyday people understand legal documents. Use only simple, common words. Write like you are talking to a friend who knows nothing about law.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 300,
                'temperature': 0.2
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data['choices'][0]['message']['content']
                
                # Parse AI response sections
                lines = ai_response.strip().split('\n')
                simplified = ""
                explanation = ""
                recommendation = ""
                
                current_section = ""
                for line in lines:
                    line = line.strip()
                    if line.upper().startswith('EXPLANATION'):
                        current_section = "explanation"
                        continue
                    elif line.upper().startswith('SIMPLIFIED'):
                        current_section = "simplified"
                        continue
                    elif line.upper().startswith('RECOMMENDATION'):
                        current_section = "recommendation"
                        continue
                    elif line and not line.startswith(('1.', '2.', '3.', '-', '*')):
                        if current_section == "explanation":
                            explanation += line + " "
                        elif current_section == "simplified":
                            simplified += line + " "
                        elif current_section == "recommendation":
                            recommendation += line + " "
                
                # If parsing failed, use fallback
                if not simplified:
                    simplified = ai_response[:200] + "..."
                if not explanation:
                    explanation = "This clause contains important legal terms."
                if not recommendation:
                    recommendation = "Review this carefully before agreeing."
                
                return {
                    'simplified': simplified.strip(),
                    'explanation': explanation.strip(),
                    'recommendation': recommendation.strip(),
                    'confidence': 0.9
                }
            
            else:
                self.logger.warning(f"AI API request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error calling AI API: {str(e)}")
            return None
    
    def _simplify_with_patterns(self, text: str) -> str:
        """Simplify text using pattern replacement."""
        simplified = text
        
        # Apply pattern replacements
        for complex_term, simple_term in self.simplification_patterns.items():
            simplified = simplified.replace(complex_term, simple_term)
        
        # Additional simplification rules
        simplified = self._apply_simplification_rules(simplified)
        
        return simplified
    
    def _apply_simplification_rules(self, text: str) -> str:
        """Apply general simplification rules."""
        # Break up long sentences
        sentences = text.split('. ')
        simplified_sentences = []
        
        for sentence in sentences:
            # Replace complex sentence structures
            sentence = sentence.replace(' which ', ' that ')
            sentence = sentence.replace(' wherein ', ' where ')
            sentence = sentence.replace(' whereby ', ' by which ')
            
            # Simplify passive voice where possible
            sentence = sentence.replace(' shall be ', ' will be ')
            sentence = sentence.replace(' may be ', ' can be ')
            
            simplified_sentences.append(sentence)
        
        return '. '.join(simplified_sentences)
    
    def _generate_explanation(self, clause_text: str, clause_type: str) -> str:
        """Generate a basic explanation for a clause type."""
        explanations = {
            'liability': 'This clause determines who is responsible for damages or losses if something goes wrong.\nIt affects your financial risk and legal protection in the agreement.',
            'warranty': 'This is a promise or guarantee about the quality, performance, or condition of something.\nIf the warranty is broken, you may have the right to compensation or repair.',
            'termination': 'This clause explains the conditions and procedures for ending the agreement.\nIt covers when, how, and what happens after the contract is terminated.',
            'financial': 'This section deals with money matters including payments, fees, costs, and financial obligations.\nIt determines how much you pay, when you pay, and what happens if you miss payments.',
            'confidentiality': 'This requires you to keep certain information private and not share it with others.\nBreaking confidentiality could result in legal consequences or financial penalties.',
            'intellectual_property': 'This determines who owns ideas, inventions, creative works, or other intellectual property.\nIt affects your rights to use, modify, or profit from intellectual property.',
            'dispute_resolution': 'This explains how disagreements or conflicts will be handled if they arise.\nIt may require mediation, arbitration, or specify which courts can hear disputes.',
            'general': 'This clause contains basic rules and conditions that apply to the overall agreement.\nIt helps define the framework and general obligations for both parties.'
        }
        
        base_explanation = explanations.get(clause_type, explanations['general'])
        
        # Add specific risk warnings based on clause content
        if 'unlimited' in clause_text.lower() or 'without limit' in clause_text.lower():
            base_explanation += '\n⚠️ Warning: This clause may expose you to unlimited financial risk.'
        elif 'automatic' in clause_text.lower() and clause_type == 'termination':
            base_explanation += '\n⚠️ Note: This agreement may renew automatically unless you take action.'
        elif 'shall' in clause_text.lower() or 'must' in clause_text.lower():
            base_explanation += '\n⚠️ Important: This creates mandatory obligations you must fulfill.'
        
        return base_explanation
    
    def _generate_simple_recommendation(self, clause_type: str) -> str:
        """Generate simple recommendations for clause types."""
        recommendations = {
            'liability': 'Ask a lawyer if you might have to pay money if something goes wrong.',
            'warranty': 'Make sure you can do what you promise.',
            'termination': 'Understand how to end this agreement.',
            'financial': 'Check all payment amounts and dates.',
            'confidentiality': 'Be careful about sharing information.',
            'intellectual_property': 'Know who owns what you create.',
            'dispute_resolution': 'Understand how problems will be solved.',
            'general': 'Read this carefully and ask questions if confused.'
        }
        
        return recommendations.get(clause_type, recommendations['general'])
    
    def batch_simplify(self, clauses: list) -> list:
        """Simplify multiple clauses with rate limiting."""
        simplified_clauses = []
        
        for i, clause in enumerate(clauses):
            self.logger.info(f"Simplifying clause {i+1}/{len(clauses)}")
            
            simplified = self.simplify_clause(clause['text'], clause['type'])
            
            # Add original clause data
            simplified.update({
                'id': clause['id'],
                'type': clause['type'],
                'importance': clause['importance']
            })
            
            simplified_clauses.append(simplified)
            
            # Rate limiting for API calls
            if self.api_key and i < len(clauses) - 1:
                time.sleep(1)  # Wait 1 second between API calls
        
        return simplified_clauses
