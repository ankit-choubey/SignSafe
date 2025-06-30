# SignSafe - Legal Document Analyzer

## Overview

SignSafe is a professional, GitHub-ready legal document analyzer built with Streamlit. The application features a comprehensive repository structure with proper documentation, testing, and contribution guidelines. It uses AI-powered analysis to make complex legal language accessible through risk assessment, clause simplification, and multi-language translation. The project follows industry best practices for open-source development with modular architecture and extensive documentation.

## System Architecture

### Project Structure
- **Clean Organization**: All source code organized under `src/` directory
- **Modular Design**: Separate directories for pipeline, ui, utils, and config components
- **Single Entry Point**: `app.py` serves as the main application entry point
- **Environment Configuration**: `.env` file for API keys and configuration

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **UI Pattern**: Single-page application with sidebar navigation and expandable layout
- **State Management**: Streamlit session state for maintaining user data across interactions
- **File Handling**: Built-in Streamlit file upload components with local storage in uploads directory
- **Interactive Elements**: Risk dashboard, voice chat interface, and multi-language translation controls

### Backend Architecture
- **Architecture Pattern**: Modular pipeline with loosely coupled components organized in `src/` directory
- **Processing Pipeline**: Sequential document processing through specialized modules (OCR → Clause Splitting → Simplification → Risk Analysis → Translation)
- **API Integration**: Multiple AI service integrations (Omnidimension API and Google Gemini) with regex-based fallback mechanisms
- **File Monitoring**: Real-time folder monitoring using watchdog library for automatic document processing
- **Error Handling**: Comprehensive logging and graceful degradation when external services are unavailable
- **Rate Limiting**: Built-in 5-second delays between API requests to avoid service limits

## Key Components

### Document Processing Pipeline
- **OCR Parser** (`pipeline/ocr_parser.py`): Handles PDF text extraction using PyPDF2 and image OCR using pytesseract for various image formats (PNG, JPG, JPEG, TIFF, BMP)
- **Clause Splitter** (`pipeline/clause_splitter.py`): Segments legal documents using pattern recognition for numbered clauses, sections, and legal terminology with categorization by clause type (liability, termination, warranty, financial, confidentiality)
- **Legal Simplifier** (`pipeline/simplifier.py`): AI-powered language simplification using Omnidimension API with extensive regex-based fallbacks for common legal terms
- **Gemini Simplifier** (`utils/gemini_simplifier.py`): Alternative AI simplification using Google Gemini API for shortest, simplest language conversion with specific legal context prompts
- **Risk Analyzer** (`pipeline/risk_analyzer.py`): Risk assessment using keyword matching and pattern recognition to identify high, medium, and low-risk clauses with specific risk patterns for unlimited liability, personal guarantees, and broad indemnity

### User Interface Components
- **Streamlit UI** (`ui/streamlit_ui.py`): Main application interface with file upload, processing status, results display, document management, and interactive risk dashboard
- **Voice Chat** (`utils/voice_chat.py`): Conversational query interface for document analysis with pattern-based question routing for common legal topics

### Utility Components
- **Pathway Monitor** (`utils/pathway_monitor.py`): File system monitoring for automatic document processing using watchdog with support for multiple file formats and real-time event handling
- **Multi-Language Translator** (`utils/translator.py`): AI-powered translation system supporting Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, and Assamese with batch translation capabilities
- **Main Entry Points** (`main.py`, `app.py`): Application bootstrap and Streamlit configuration with environment variable loading

## Data Flow

1. **Document Input**: Users upload files through Streamlit interface or files are detected via folder monitoring
2. **Text Extraction**: OCR Parser extracts text from PDF/image files using appropriate libraries (PyPDF2 for PDFs, pytesseract for images)
3. **Clause Segmentation**: Text is broken into individual clauses using regex patterns and categorized by type (liability, termination, warranty, etc.)
4. **Language Simplification**: Complex legal language is simplified using AI APIs (Omnidimension or Gemini) or fallback patterns for common legal terms
5. **Risk Assessment**: Clauses are analyzed for risk levels using keyword matching and pattern recognition with specific indicators for high, medium, and low-risk content
6. **Translation**: Simplified clauses can be translated to Indian regional languages using Gemini API with rate limiting
7. **Results Presentation**: Processed information is displayed in the Streamlit interface with interactive elements, risk summaries, and expandable clause details
8. **Voice Interaction**: Users can ask questions about documents through the voice chat interface with pattern-based routing

## External Dependencies

### Third-Party Libraries
- **Streamlit**: Web application framework for the user interface
- **PyPDF2**: PDF text extraction and parsing
- **pytesseract**: OCR functionality for image-based text extraction
- **Pillow (PIL)**: Image processing and format conversion
- **watchdog**: File system monitoring for real-time document detection
- **requests**: HTTP client for external API communications
- **google-generativeai**: Google Gemini AI integration for advanced text processing
- **python-dotenv**: Environment variable management

### External APIs
- **Omnidimension API**: Primary AI service for legal text simplification with fallback to regex patterns
- **Google Gemini API**: Alternative AI service for text simplification and multi-language translation
- **Tesseract OCR**: System-level OCR engine for image text extraction

## Deployment Strategy

### Local Development
- **Entry Point**: Single entry point (`app.py`) for streamlined deployment
- **Dependency Installer**: Simple `install_dependencies.py` script for one-command setup
- **Environment Configuration**: `.env` file for API key management with `.env.template` example
- **Direct Installation**: No virtual environment complexity - direct Python package installation

### Configuration Management
- **API Keys**: Environment-based configuration for Omnidimension and Google Gemini APIs
- **Fallback Mechanisms**: Graceful degradation when external services are unavailable
- **File Storage**: Local uploads directory with automatic creation
- **Logging**: Comprehensive logging configuration for debugging and monitoring

### System Requirements
- **Python**: Version 3.11 or higher
- **Optional OCR**: Tesseract OCR engine for enhanced image text extraction
- **Storage**: Local file system for document uploads and processing
- **Network**: Internet connection required for AI API services (optional with fallbacks)

## Changelog

- June 30, 2025: Optimized repository structure for professional GitHub deployment
  - Created comprehensive GitHub repository structure with proper documentation
  - Added professional README with badges, detailed usage instructions, and roadmap
  - Implemented standard open-source files: LICENSE (MIT), .gitignore, CONTRIBUTING.md
  - Created extensive documentation suite: USER_GUIDE.md, ARCHITECTURE.md, API reference
  - Added professional test suite with unit tests for core pipeline functionality
  - Structured project with proper docs/ and tests/ directories
  - Enhanced .env.template with detailed configuration instructions
  - Streamlined installation process with single dependency installer script
- June 29, 2025: Major cleanup and reorganization
  - Completely restructured project with clean src/ directory organization
  - Removed all duplicate files and unused components
  - Consolidated multiple nested directories into single clean structure
  - Updated all import paths for new organization
  - Created comprehensive README.md with project overview
  - Simplified deployment with single app.py entry point
- June 29, 2025: Fixed runtime errors and deployment issues
  - Resolved "resource temporarily unavailable" runtime errors
  - Fixed Google Generative AI module import issues
  - Configured proper Streamlit deployment settings
  - Added API key configuration in .env files
  - Successfully integrated Omnidimension and Gemini APIs
  - App now running successfully with full AI features enabled
- June 29, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.