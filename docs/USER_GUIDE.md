# SignSafe User Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Uploading Documents](#uploading-documents)
- [Understanding Results](#understanding-results)
- [Using Voice Chat](#using-voice-chat)
- [Language Translation](#language-translation)
- [Risk Assessment](#risk-assessment)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Installation
1. Install dependencies: `python install_dependencies.py`
2. (Optional) Configure API keys by copying `.env.template` to `.env`
3. Run the application: `streamlit run app.py`
4. Open your browser to the displayed URL

### First Time Setup
- The application creates an `uploads/` folder for document storage
- API keys are optional - the app works with pattern-based analysis without them
- For enhanced AI features, add your Google Gemini API key to the `.env` file

## Uploading Documents

### Supported File Types
- **PDF files**: `.pdf`
- **Image files**: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`

### Upload Methods
1. **Web Interface**: Drag and drop files or click to browse
2. **Folder Monitoring**: Place files directly in the `uploads/` folder

### File Requirements
- Maximum file size: 200MB
- Images should have clear, readable text
- PDFs can be text-based or scanned documents

## Understanding Results

### Clause Analysis
Each document is broken down into individual clauses with:
- **Original Text**: The exact legal language from the document
- **Simplified Version**: Plain English explanation
- **Clause Type**: Category (liability, termination, warranty, etc.)
- **Importance Level**: High, Medium, or Low priority

### Clause Types
- **Liability**: Terms about who is responsible for damages
- **Termination**: Conditions for ending the agreement
- **Warranty**: Guarantees and promises made by parties
- **Financial**: Payment terms, fees, and financial obligations
- **Confidentiality**: Non-disclosure and privacy requirements
- **General**: Other contractual terms

## Risk Assessment

### Risk Levels
- **🔴 High Risk**: Requires immediate attention
- **🟡 Medium Risk**: Should be reviewed carefully
- **🟢 Low Risk**: Standard contractual language

### Risk Indicators
- Unlimited liability clauses
- Personal guarantees
- Broad indemnification terms
- Automatic renewal clauses
- Harsh termination penalties

### Risk Summary Dashboard
- Overall document risk level
- Count of high, medium, and low-risk clauses
- Specific recommendations for each risk area
- Suggested actions to mitigate risks

## Using Voice Chat

### Asking Questions
The voice chat feature allows you to ask natural language questions about your documents:

**Example Questions:**
- "What are my main obligations under this contract?"
- "What happens if I breach this agreement?"
- "How can this contract be terminated?"
- "What are the payment terms?"
- "What are the highest-risk parts of this document?"

### Getting Better Answers
- Be specific about what you want to know
- Reference particular sections if needed
- Ask follow-up questions for clarification
- Use simple, conversational language

## Language Translation

### Supported Languages
- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)
- Urdu (اردو)
- Odia (ଓଡ଼ିଆ)
- Assamese (অসমীয়া)

### Translation Features
- **Clause Translation**: Individual clause translation with context
- **Batch Translation**: Translate entire documents
- **Legal Context**: Translations maintain legal accuracy
- **Rate Limited**: Processed gradually to avoid API limits

### Using Translation
1. Select your preferred language from the dropdown
2. Click "Translate Document" 
3. Wait for processing (may take several minutes for large documents)
4. Review translated clauses alongside originals

## Advanced Features

### Contract Templates
Generate new contracts using AI:
1. Go to the "Contract Templates" tab
2. Select contract type (Employment, NDA, Service Agreement, etc.)
3. Fill in party details and specific requirements
4. Choose risk level and language complexity
5. Generate and review the template

### Real-time Monitoring
The app automatically monitors the `uploads/` folder:
- New documents are processed automatically
- Processing status is shown in the sidebar
- Results appear in the document list when complete

### Batch Processing
Process multiple documents efficiently:
- Upload multiple files at once
- Each document is analyzed independently
- Results are saved and accessible from the sidebar

## Tips for Best Results

### Document Quality
- Use high-resolution scans for image files
- Ensure text is clearly readable
- Avoid heavily watermarked documents
- Convert complex layouts to single-column format when possible

### AI Features
- Add API keys for enhanced simplification and translation
- Without API keys, the app uses pattern-based analysis
- AI features work best with standard legal language
- Complex or highly technical clauses may need manual review

### Performance
- Large documents may take several minutes to process
- OCR processing is slower than PDF text extraction
- AI translation is rate-limited to avoid service restrictions
- Close unused browser tabs to improve performance

## Troubleshooting

### Common Issues

**"No text extracted from document"**
- Check if the file is corrupted
- For images, ensure text is clearly visible
- Try converting the document to a different format

**"API key not working"**
- Verify the API key is correctly copied to `.env`
- Check that the key has proper permissions
- Ensure the API service is active and funded

**"Processing stuck"**
- Refresh the browser page
- Check the console for error messages
- Try uploading a smaller or simpler document first

**"Translation failed"**
- API translation requires active Google Gemini key
- Try smaller batches if processing large documents
- Check internet connection for API calls

### Performance Issues
- Large files (>50MB) may process slowly
- Multiple simultaneous uploads can affect performance
- Clear browser cache if the interface becomes unresponsive

### Getting Help
- Check the console output for detailed error messages
- Ensure all dependencies are installed correctly
- Verify file permissions for the uploads directory
- Review the logs for specific error details

## Security and Privacy

### Data Handling
- Documents are processed locally on your machine
- Only simplified text is sent to AI services (not full documents)
- No document content is stored by external services
- All processing happens in your browser session

### API Usage
- API calls are made only for text simplification and translation
- No sensitive document metadata is transmitted
- Rate limiting prevents excessive API usage
- API keys are stored locally in environment variables

### Best Practices
- Don't upload highly sensitive documents without reviewing AI settings
- Keep API keys secure and don't share them
- Regularly clear the uploads folder of processed documents
- Use strong passwords if deploying on shared systems

## Frequently Asked Questions

**Q: Do I need API keys to use SignSafe?**
A: No, the basic functionality works without API keys using pattern-based analysis. API keys enhance the AI features.

**Q: What happens to my documents?**
A: Documents are processed locally. Only text snippets are sent to AI services for simplification, never full documents.

**Q: Can I process confidential documents?**
A: Yes, but review the privacy settings. For maximum security, use the app without API keys for offline processing.

**Q: How accurate is the risk assessment?**
A: The risk assessment identifies common problematic clauses but isn't a substitute for legal advice. Always consult an attorney for important contracts.

**Q: Can I export the results?**
A: Currently, results are displayed in the web interface. Export functionality is planned for future releases.

**Q: Does SignSafe work offline?**
A: Basic document analysis works offline. AI features require internet connection and API keys.