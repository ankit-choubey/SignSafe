import re
import logging
from typing import Dict, List, Tuple

class RiskAnalyzer:
    """Analyzes legal clauses for risk levels and potential issues."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # High-risk keywords and phrases
        self.high_risk_indicators = [
            'unlimited liability', 'personal guarantee', 'liquidated damages',
            'punitive damages', 'attorney fees', 'indemnify', 'hold harmless',
            'waive', 'disclaim', 'exclude', 'limitation of liability',
            'force majeure', 'act of god', 'material breach',
            'immediate termination', 'without notice', 'sole discretion',
            'binding arbitration', 'class action waiver', 'jury trial waiver',
            'automatic renewal', 'perpetual', 'irrevocable',
            'intellectual property assignment', 'work for hire',
            'non-compete', 'restraint of trade', 'liquidation preference'
        ]
        
        # Medium-risk keywords and phrases
        self.medium_risk_indicators = [
            'reasonable efforts', 'best efforts', 'material adverse effect',
            'commercially reasonable', 'industry standard', 'good faith',
            'confidential information', 'proprietary', 'trade secrets',
            'warranty', 'representation', 'covenant', 'undertaking',
            'cure period', 'notice period', 'governing law',
            'jurisdiction', 'venue', 'dispute resolution',
            'modification', 'amendment', 'assignment', 'delegation',
            'severability', 'entire agreement', 'merger clause'
        ]
        
        # Low-risk keywords (generally protective)
        self.low_risk_indicators = [
            'mutual', 'reciprocal', 'both parties', 'either party',
            'reasonable notice', 'written consent', 'prior approval',
            'cure right', 'grace period', 'mitigation',
            'proportionate', 'equitable', 'fair market value'
        ]
        
        # Specific risk patterns
        self.risk_patterns = {
            'unlimited_liability': r'unlimited.*liability|liability.*unlimited',
            'personal_guarantee': r'personal.*guarantee|guarantee.*personal',
            'broad_indemnity': r'indemnify.*from.*all|indemnify.*against.*any',
            'automatic_renewal': r'automatic.*renew|renew.*automatic',
            'broad_termination': r'terminate.*convenience|terminate.*reason',
            'ip_assignment': r'assign.*intellectual.*property|intellectual.*property.*assign',
            'non_compete': r'non.compete|restraint.*trade|compete.*restrict',
            'waiver_rights': r'waive.*right|waive.*claim|waive.*defense',
            'liquidated_damages': r'liquidated.*damage|damage.*liquidated',
            'attorney_fees': r'attorney.*fee|legal.*fee.*prevailing'
        }
    
    def analyze_risk(self, clause_text: str, clause_type: str, importance: str) -> Dict[str, any]:
        """Analyze risk level of a legal clause."""
        result = {
            'risk_level': 'low',
            'risk_score': 0,
            'risk_factors': [],
            'warnings': [],
            'recommendations': [],
            'color': 'green'
        }
        
        try:
            text_lower = clause_text.lower()
            risk_score = 0
            risk_factors = []
            warnings = []
            recommendations = []
            
            # Check for specific risk patterns
            for pattern_name, pattern in self.risk_patterns.items():
                if re.search(pattern, text_lower):
                    risk_score += 30
                    risk_factors.append(pattern_name.replace('_', ' ').title())
                    warnings.append(self._get_pattern_warning(pattern_name))
            
            # Check for high-risk indicators
            for indicator in self.high_risk_indicators:
                if indicator.lower() in text_lower:
                    risk_score += 20
                    risk_factors.append(indicator.title())
                    warnings.append(f"Contains high-risk term: '{indicator}'")
            
            # Check for medium-risk indicators
            for indicator in self.medium_risk_indicators:
                if indicator.lower() in text_lower:
                    risk_score += 10
                    risk_factors.append(indicator.title())
            
            # Check for low-risk (protective) indicators
            protective_count = 0
            for indicator in self.low_risk_indicators:
                if indicator.lower() in text_lower:
                    protective_count += 1
                    risk_score -= 5  # Reduce risk for protective terms
            
            # Adjust risk based on clause type
            risk_score += self._get_type_risk_adjustment(clause_type)
            
            # Adjust risk based on importance
            if importance == 'high':
                risk_score += 15
            elif importance == 'medium':
                risk_score += 5
            
            # Determine final risk level
            if risk_score >= 50:
                result['risk_level'] = 'high'
                result['color'] = 'red'
            elif risk_score >= 25:
                result['risk_level'] = 'medium'
                result['color'] = 'orange'
            else:
                result['risk_level'] = 'low'
                result['color'] = 'green'
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                clause_type, risk_factors, result['risk_level']
            )
            
            result.update({
                'risk_score': max(0, risk_score),
                'risk_factors': list(set(risk_factors)),
                'warnings': warnings,
                'recommendations': recommendations
            })
            
        except Exception as e:
            self.logger.error(f"Error analyzing risk: {str(e)}")
            result['warnings'] = ['Error occurred during risk analysis']
        
        return result
    
    def _get_pattern_warning(self, pattern_name: str) -> str:
        """Get specific warnings for risk patterns."""
        warnings = {
            'unlimited_liability': 'This clause may expose you to unlimited financial liability.',
            'personal_guarantee': 'You may be personally responsible for obligations.',
            'broad_indemnity': 'You may have to pay for legal costs and damages of the other party.',
            'automatic_renewal': 'This agreement may renew automatically without your action.',
            'broad_termination': 'The other party can terminate this agreement easily.',
            'ip_assignment': 'You may be giving up rights to your intellectual property.',
            'non_compete': 'This may restrict your ability to work in your field.',
            'waiver_rights': 'You may be giving up important legal rights.',
            'liquidated_damages': 'You may owe predetermined damages regardless of actual harm.',
            'attorney_fees': 'You may have to pay the other party\'s legal fees if you lose.'
        }
        
        return warnings.get(pattern_name, 'This clause contains potentially risky language.')
    
    def _get_type_risk_adjustment(self, clause_type: str) -> int:
        """Get risk score adjustment based on clause type."""
        type_adjustments = {
            'liability': 20,
            'termination': 15,
            'warranty': 10,
            'intellectual_property': 15,
            'confidentiality': 5,
            'financial': 10,
            'dispute_resolution': 10,
            'general': 0
        }
        
        return type_adjustments.get(clause_type, 0)
    
    def _generate_recommendations(self, clause_type: str, risk_factors: List[str], risk_level: str) -> List[str]:
        """Generate recommendations based on risk analysis."""
        recommendations = []
        
        # General recommendations by risk level
        if risk_level == 'high':
            recommendations.append("Consider consulting with a lawyer before agreeing to this clause.")
            recommendations.append("Try to negotiate more favorable terms.")
        elif risk_level == 'medium':
            recommendations.append("Review this clause carefully and understand its implications.")
            recommendations.append("Consider asking for clarifications or modifications.")
        
        # Specific recommendations by clause type
        type_recommendations = {
            'liability': [
                "Try to limit liability to direct damages only.",
                "Request mutual liability limitations.",
                "Ensure adequate insurance coverage."
            ],
            'termination': [
                "Request reasonable notice periods.",
                "Ensure you have similar termination rights.",
                "Clarify what happens to your data and work product."
            ],
            'warranty': [
                "Ensure warranties are reasonable and achievable.",
                "Request mutual warranty disclaimers.",
                "Limit warranty periods to reasonable timeframes."
            ],
            'intellectual_property': [
                "Clarify ownership of existing vs. new intellectual property.",
                "Retain rights to your pre-existing IP.",
                "Ensure you can use your work for portfolio/reference purposes."
            ],
            'financial': [
                "Ensure payment terms are clearly defined.",
                "Request protection against late payment penalties.",
                "Clarify expense reimbursement procedures."
            ]
        }
        
        if clause_type in type_recommendations:
            recommendations.extend(type_recommendations[clause_type])
        
        # Specific recommendations for risk factors
        if 'Unlimited Liability' in risk_factors:
            recommendations.append("Request a liability cap or limitation.")
        
        if 'Personal Guarantee' in risk_factors:
            recommendations.append("Try to limit personal guarantees to corporate obligations only.")
        
        if 'Non Compete' in risk_factors:
            recommendations.append("Negotiate reasonable geographic and time limitations.")
        
        return list(set(recommendations))  # Remove duplicates
    
    def generate_risk_summary(self, analyzed_clauses: List[Dict]) -> Dict[str, any]:
        """Generate an overall risk summary for the document."""
        total_clauses = len(analyzed_clauses)
        high_risk_count = len([c for c in analyzed_clauses if c.get('risk_level') == 'high'])
        medium_risk_count = len([c for c in analyzed_clauses if c.get('risk_level') == 'medium'])
        low_risk_count = len([c for c in analyzed_clauses if c.get('risk_level') == 'low'])
        
        # Calculate overall risk score
        total_risk_score = sum(c.get('risk_score', 0) for c in analyzed_clauses)
        avg_risk_score = total_risk_score / total_clauses if total_clauses > 0 else 0
        
        # Determine overall risk level
        if high_risk_count > 0 or avg_risk_score >= 50:
            overall_risk = 'high'
            overall_color = 'red'
        elif medium_risk_count > total_clauses * 0.3 or avg_risk_score >= 25:
            overall_risk = 'medium'
            overall_color = 'orange'
        else:
            overall_risk = 'low'
            overall_color = 'green'
        
        # Collect all risk factors and warnings
        all_risk_factors = []
        all_warnings = []
        for clause in analyzed_clauses:
            all_risk_factors.extend(clause.get('risk_factors', []))
            all_warnings.extend(clause.get('warnings', []))
        
        # Get top risk factors
        risk_factor_counts = {}
        for factor in all_risk_factors:
            risk_factor_counts[factor] = risk_factor_counts.get(factor, 0) + 1
        
        top_risk_factors = sorted(risk_factor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'overall_risk': overall_risk,
            'overall_color': overall_color,
            'total_clauses': total_clauses,
            'high_risk_count': high_risk_count,
            'medium_risk_count': medium_risk_count,
            'low_risk_count': low_risk_count,
            'average_risk_score': round(avg_risk_score, 1),
            'top_risk_factors': [factor for factor, count in top_risk_factors],
            'critical_warnings': list(set(all_warnings))[:10],  # Top 10 unique warnings
            'recommendation': self._get_overall_recommendation(overall_risk, high_risk_count, total_clauses)
        }
    
    def _get_overall_recommendation(self, overall_risk: str, high_risk_count: int, total_clauses: int) -> str:
        """Generate overall recommendation for the document."""
        if overall_risk == 'high':
            return f"This document contains {high_risk_count} high-risk clauses out of {total_clauses} total. Ask our AI voice assistant about specific warnings and get detailed explanations before proceeding."
        elif overall_risk == 'medium':
            return f"This document has moderate risk. Use the AI voice assistant to understand complex terms and get personalized guidance."
        else:
            return f"This document appears to have low risk overall. You can ask the AI voice assistant about any specific clauses you want to understand better."
