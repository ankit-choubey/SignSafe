import os
import logging
import requests
from typing import Dict, List, Any, Optional

class VoiceChatHandler:
    """Handles voice chat functionality for document queries."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv("OMNIDIMENSION_API_KEY", "")
        self.base_url = "https://api.omnidimension.ai/v1"
        
        # Common legal question patterns and responses
        self.question_patterns = {
            'termination': [
                'termination', 'terminate', 'end', 'cancel', 'cancellation',
                'exit', 'break', 'dissolution'
            ],
            'liability': [
                'liability', 'liable', 'responsible', 'blame', 'fault',
                'damages', 'compensation', 'indemnity'
            ],
            'payment': [
                'payment', 'pay', 'money', 'cost', 'fee', 'price',
                'billing', 'invoice', 'financial'
            ],
            'warranty': [
                'warranty', 'guarantee', 'promise', 'assurance',
                'coverage', 'protection'
            ],
            'obligations': [
                'obligations', 'duties', 'responsibilities', 'requirements',
                'must', 'shall', 'need to', 'have to'
            ],
            'breach': [
                'breach', 'violation', 'default', 'non-compliance',
                'break', 'violate', 'fail to'
            ],
            'renewal': [
                'renewal', 'renew', 'extend', 'extension', 'continue',
                'automatic', 'rollover'
            ],
            'intellectual_property': [
                'intellectual property', 'ip', 'copyright', 'patent',
                'trademark', 'trade secret', 'proprietary'
            ]
        }
    
    def process_question(self, question: str, document_data: Dict[str, Any]) -> str:
        """Process a user question about the document."""
        try:
            # First try AI-powered response
            if self.api_key:
                ai_response = self._get_ai_response(question, document_data)
                if ai_response:
                    return ai_response
            
            # Fallback to pattern-based response
            return self._get_pattern_based_response(question, document_data)
            
        except Exception as e:
            self.logger.error(f"Error processing question: {str(e)}")
            return "I'm sorry, I encountered an error while processing your question. Please try again."
    
    def _get_ai_response(self, question: str, document_data: Dict[str, Any]) -> Optional[str]:
        """Get AI-powered response using Omnidimension API."""
        try:
            clauses = document_data.get('clauses', [])
            risk_summary = document_data.get('risk_summary', {})
            
            # Prepare context from document
            context = self._prepare_document_context(clauses, risk_summary)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""
            You are a legal assistant helping users understand their legal documents. 
            Please answer the user's question based on the document analysis provided.
            
            Document Context:
            {context}
            
            User Question: {question}
            
            Please provide a clear, helpful answer that:
            1. Directly addresses the user's question
            2. References specific clauses when relevant
            3. Highlights any important risks or implications
            4. Uses simple, non-legal language
            5. Suggests next steps if appropriate
            
            If the question cannot be answered from the document, say so clearly.
            """
            
            payload = {
                'model': 'gpt-4',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a helpful legal assistant that explains legal documents in simple terms.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 400,
                'temperature': 0.3
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                self.logger.warning(f"AI API request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting AI response: {str(e)}")
            return None
    
    def _prepare_document_context(self, clauses: List[Dict], risk_summary: Dict) -> str:
        """Prepare document context for AI processing."""
        context_parts = []
        
        # Add risk summary
        overall_risk = risk_summary.get('overall_risk', 'unknown')
        context_parts.append(f"Overall Risk Level: {overall_risk}")
        
        high_risk_count = risk_summary.get('high_risk_count', 0)
        medium_risk_count = risk_summary.get('medium_risk_count', 0)
        
        context_parts.append(f"High Risk Clauses: {high_risk_count}")
        context_parts.append(f"Medium Risk Clauses: {medium_risk_count}")
        
        # Add top risk factors
        top_risks = risk_summary.get('top_risk_factors', [])
        if top_risks:
            context_parts.append(f"Main Risk Factors: {', '.join(top_risks[:3])}")
        
        # Add key clauses by type
        clause_types = {}
        for clause in clauses:
            clause_type = clause.get('type', 'general')
            if clause_type not in clause_types:
                clause_types[clause_type] = []
            clause_types[clause_type].append(clause)
        
        # Include important clause types
        important_types = ['liability', 'termination', 'warranty', 'financial', 'intellectual_property']
        
        for clause_type in important_types:
            if clause_type in clause_types:
                context_parts.append(f"\n{clause_type.title()} Clauses:")
                for clause in clause_types[clause_type][:2]:  # Max 2 clauses per type
                    simplified = clause.get('simplified', clause.get('original', ''))
                    risk_level = clause.get('risk_level', 'unknown')
                    context_parts.append(f"- ({risk_level} risk) {simplified[:200]}...")
        
        return "\n".join(context_parts)
    
    def _get_pattern_based_response(self, question: str, document_data: Dict[str, Any]) -> str:
        """Generate response based on question patterns and document analysis."""
        question_lower = question.lower()
        clauses = document_data.get('clauses', [])
        risk_summary = document_data.get('risk_summary', {})
        
        # Identify question type
        question_type = self._identify_question_type(question_lower)
        
        if question_type:
            return self._generate_typed_response(question_type, clauses, risk_summary)
        else:
            return self._generate_general_response(question, clauses, risk_summary)
    
    def _identify_question_type(self, question: str) -> Optional[str]:
        """Identify the type of question based on keywords."""
        for question_type, keywords in self.question_patterns.items():
            if any(keyword in question for keyword in keywords):
                return question_type
        return None
    
    def _generate_typed_response(self, question_type: str, clauses: List[Dict], risk_summary: Dict) -> str:
        """Generate a response for a specific question type."""
        # Find relevant clauses
        relevant_clauses = [
            clause for clause in clauses 
            if clause.get('type') == question_type or 
               any(keyword in clause.get('original', '').lower() 
                   for keyword in self.question_patterns.get(question_type, []))
        ]
        
        if not relevant_clauses:
            return f"I couldn't find any specific {question_type} clauses in this document. This might mean that {question_type} is not addressed, or it might be covered under general terms."
        
        response_parts = []
        
        # Response based on question type
        if question_type == 'termination':
            response_parts.append("Here's what I found about termination:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                risk_level = clause.get('risk_level', 'unknown')
                response_parts.append(f"• ({risk_level} risk) {simplified[:150]}...")
            
            if any(clause.get('risk_level') == 'high' for clause in relevant_clauses):
                response_parts.append("\n⚠️ Warning: Some termination clauses have high risk. Consider legal review.")
        
        elif question_type == 'liability':
            response_parts.append("Here's what I found about liability:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                risk_level = clause.get('risk_level', 'unknown')
                response_parts.append(f"• ({risk_level} risk) {simplified[:150]}...")
            
            if any(clause.get('risk_level') == 'high' for clause in relevant_clauses):
                response_parts.append("\n⚠️ Warning: High-risk liability terms detected. You may have significant financial exposure.")
        
        elif question_type == 'payment':
            response_parts.append("Here's what I found about payments and costs:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                response_parts.append(f"• {simplified[:150]}...")
        
        elif question_type == 'warranty':
            response_parts.append("Here's what I found about warranties and guarantees:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                risk_level = clause.get('risk_level', 'unknown')
                response_parts.append(f"• ({risk_level} risk) {simplified[:150]}...")
        
        elif question_type == 'obligations':
            response_parts.append("Here are your main obligations under this agreement:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                response_parts.append(f"• {simplified[:150]}...")
        
        elif question_type == 'renewal':
            response_parts.append("Here's what I found about renewal terms:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                risk_level = clause.get('risk_level', 'unknown')
                response_parts.append(f"• ({risk_level} risk) {simplified[:150]}...")
            
            if any('automatic' in clause.get('original', '').lower() for clause in relevant_clauses):
                response_parts.append("\n⚠️ Note: This agreement may renew automatically. Make sure you understand the renewal terms.")
        
        else:
            response_parts.append(f"Here's what I found about {question_type}:")
            for clause in relevant_clauses[:3]:
                simplified = clause.get('simplified', clause.get('original', ''))
                response_parts.append(f"• {simplified[:150]}...")
        
        return "\n".join(response_parts)
    
    def _generate_general_response(self, question: str, clauses: List[Dict], risk_summary: Dict) -> str:
        """Generate a general response when question type is not identified."""
        overall_risk = risk_summary.get('overall_risk', 'unknown')
        high_risk_count = risk_summary.get('high_risk_count', 0)
        total_clauses = risk_summary.get('total_clauses', 0)
        
        response_parts = [
            f"Based on your question, here's a general overview of this document:",
            f"",
            f"📊 Document Summary:",
            f"• Total clauses analyzed: {total_clauses}",
            f"• Overall risk level: {overall_risk}",
            f"• High-risk clauses: {high_risk_count}",
            f"",
            f"To get more specific information, try asking about:",
            f"• Termination conditions",
            f"• Liability and damages",
            f"• Payment terms",
            f"• Your obligations",
            f"• Warranty provisions",
            f"",
            f"For detailed analysis, review the Document Review tab."
        ]
        
        return "\n".join(response_parts)
    
    def get_suggested_questions(self, document_data: Dict[str, Any]) -> List[str]:
        """Generate suggested questions based on document content."""
        clauses = document_data.get('clauses', [])
        risk_summary = document_data.get('risk_summary', {})
        
        suggestions = []
        
        # Check what clause types are present
        clause_types = set(clause.get('type', 'general') for clause in clauses)
        
        if 'liability' in clause_types:
            suggestions.append("What are my liability risks in this agreement?")
        
        if 'termination' in clause_types:
            suggestions.append("How can this agreement be terminated?")
        
        if 'financial' in clause_types:
            suggestions.append("What are the payment terms?")
        
        if 'warranty' in clause_types:
            suggestions.append("What warranties am I providing?")
        
        # Add risk-based questions
        high_risk_count = risk_summary.get('high_risk_count', 0)
        if high_risk_count > 0:
            suggestions.append("What are the highest-risk parts of this document?")
        
        # Default questions
        suggestions.extend([
            "What are my main obligations under this contract?",
            "Are there any automatic renewal terms?",
            "What happens if I breach this agreement?"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions
