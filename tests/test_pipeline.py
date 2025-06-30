"""
Unit tests for SignSafe document processing pipeline
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.ocr_parser import OCRParser
from pipeline.clause_splitter import ClauseSplitter
from pipeline.risk_analyzer import RiskAnalyzer


class TestOCRParser(unittest.TestCase):
    """Test cases for OCR Parser functionality"""
    
    def setUp(self):
        self.parser = OCRParser()
    
    def test_validate_file_type_pdf(self):
        """Test PDF file type validation"""
        self.assertTrue(self.parser.validate_file_type("test.pdf"))
        self.assertTrue(self.parser.validate_file_type("document.PDF"))
    
    def test_validate_file_type_image(self):
        """Test image file type validation"""
        self.assertTrue(self.parser.validate_file_type("scan.png"))
        self.assertTrue(self.parser.validate_file_type("doc.jpg"))
        self.assertTrue(self.parser.validate_file_type("file.jpeg"))
    
    def test_validate_file_type_invalid(self):
        """Test invalid file type rejection"""
        self.assertFalse(self.parser.validate_file_type("document.txt"))
        self.assertFalse(self.parser.validate_file_type("file.docx"))


class TestClauseSplitter(unittest.TestCase):
    """Test cases for Clause Splitter functionality"""
    
    def setUp(self):
        self.splitter = ClauseSplitter()
    
    def test_split_simple_text(self):
        """Test splitting simple legal text"""
        text = "1. First clause about liability. 2. Second clause about termination."
        clauses = self.splitter.split_into_clauses(text)
        
        self.assertEqual(len(clauses), 2)
        self.assertIn("liability", clauses[0]['text'].lower())
        self.assertIn("termination", clauses[1]['text'].lower())
    
    def test_determine_clause_type_liability(self):
        """Test liability clause type detection"""
        text = "The party shall be liable for all damages and losses"
        clause_type = self.splitter._determine_clause_type(text)
        self.assertEqual(clause_type, "liability")
    
    def test_determine_clause_type_termination(self):
        """Test termination clause type detection"""
        text = "This agreement may be terminated by either party"
        clause_type = self.splitter._determine_clause_type(text)
        self.assertEqual(clause_type, "termination")
    
    def test_determine_importance_high(self):
        """Test high importance detection"""
        text = "unlimited liability and personal guarantee required"
        importance = self.splitter._determine_importance(text)
        self.assertEqual(importance, "high")
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "  Multiple   spaces\n\nand   newlines  "
        clean_text = self.splitter._clean_text(dirty_text)
        self.assertEqual(clean_text, "Multiple spaces and newlines")


class TestRiskAnalyzer(unittest.TestCase):
    """Test cases for Risk Analyzer functionality"""
    
    def setUp(self):
        self.analyzer = RiskAnalyzer()
    
    def test_analyze_high_risk_clause(self):
        """Test high risk clause detection"""
        clause_text = "unlimited liability and personal guarantee"
        result = self.analyzer.analyze_risk(clause_text, "liability", "high")
        
        self.assertEqual(result['risk_level'], "high")
        self.assertGreater(len(result['risk_factors']), 0)
        self.assertIn("unlimited_liability", [rf['pattern'] for rf in result['risk_factors']])
    
    def test_analyze_medium_risk_clause(self):
        """Test medium risk clause detection"""
        clause_text = "automatic renewal every year unless terminated"
        result = self.analyzer.analyze_risk(clause_text, "general", "medium")
        
        self.assertIn(result['risk_level'], ["medium", "high"])
        self.assertGreater(len(result['risk_factors']), 0)
    
    def test_analyze_low_risk_clause(self):
        """Test low risk clause detection"""
        clause_text = "standard business day definitions apply"
        result = self.analyzer.analyze_risk(clause_text, "general", "low")
        
        self.assertEqual(result['risk_level'], "low")
    
    def test_risk_summary_generation(self):
        """Test risk summary generation"""
        analyzed_clauses = [
            {'risk_level': 'high', 'risk_factors': [{'pattern': 'test'}]},
            {'risk_level': 'medium', 'risk_factors': []},
            {'risk_level': 'low', 'risk_factors': []}
        ]
        
        summary = self.analyzer.generate_risk_summary(analyzed_clauses)
        
        self.assertEqual(summary['high_risk_count'], 1)
        self.assertEqual(summary['medium_risk_count'], 1)
        self.assertEqual(summary['low_risk_count'], 1)
        self.assertEqual(summary['total_clauses'], 3)
        self.assertEqual(summary['overall_risk'], 'high')


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline"""
    
    def setUp(self):
        self.parser = OCRParser()
        self.splitter = ClauseSplitter()
        self.analyzer = RiskAnalyzer()
    
    def test_complete_pipeline(self):
        """Test the complete document processing pipeline"""
        # Sample legal text
        sample_text = """
        1. LIABILITY: The Contractor shall be liable for unlimited damages.
        2. TERMINATION: This agreement may be terminated with 30 days notice.
        3. WARRANTY: Standard warranties apply as per industry practice.
        """
        
        # Split into clauses
        clauses = self.splitter.split_into_clauses(sample_text)
        self.assertGreater(len(clauses), 0)
        
        # Analyze each clause for risk
        analyzed_clauses = []
        for clause in clauses:
            risk_analysis = self.analyzer.analyze_risk(
                clause['text'], 
                clause['type'], 
                clause['importance']
            )
            clause.update(risk_analysis)
            analyzed_clauses.append(clause)
        
        # Generate overall risk summary
        risk_summary = self.analyzer.generate_risk_summary(analyzed_clauses)
        
        # Verify results
        self.assertIn('overall_risk', risk_summary)
        self.assertIn('high_risk_count', risk_summary)
        self.assertGreater(risk_summary['total_clauses'], 0)
        
        # Check that high-risk clause was detected (unlimited liability)
        high_risk_clauses = [c for c in analyzed_clauses if c['risk_level'] == 'high']
        self.assertGreater(len(high_risk_clauses), 0)


if __name__ == '__main__':
    unittest.main()