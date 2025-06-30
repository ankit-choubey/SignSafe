# SignSafe 📜⚖️

**AI-Powered Legal Document Analyzer for Everyone**

> **Transform complex legal jargon into plain English instantly**
> Upload any contract, get simplified explanations, risk assessments, and ask questions in your native language.

[🌐 **Try Live Demo**](https://signsafepro.onrender.com/) | [📖 **Documentation**](#documentation) | [🚀 **Quick Start**](#quick-start) | [🤝 **Contributing**](#contributing)

## 🌟 What is SignSafe?

SignSafe revolutionizes how people understand legal documents by breaking down complex contracts into simple, actionable insights. Whether you're a small business owner reviewing a vendor agreement or an individual signing a lease, SignSafe makes legal language accessible to everyone.

### ✨ Key Features

🔍 **Smart Document Analysis**

- **PDF \& Image Support**: Upload contracts in any format (PDF, PNG, JPG, JPEG, TIFF, BMP)
- **AI-Powered Simplification**: Convert legal jargon to plain English using SignSafe 
- **Clause-by-Clause Breakdown**: Understand every section individually with categorization

⚠️ **Risk Assessment**

- **Risk Level Indicators**: High, Medium, Low risk classification with visual indicators
- **Vulnerability Detection**: Identify problematic clauses automatically including unlimited liability, personal guarantees, and harsh termination penalties
- **Actionable Recommendations**: Get specific advice for each risk area

🗣️ **Interactive Voice Chat**

- Ask questions about your documents in natural language
- "What are my main obligations?"
- "How can this contract be terminated?"
- "What are the payment terms?"

🌐 **Multi-Language Support**

- **12+ Indian Languages**: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, Assamese
- **Contextual Translation**: Maintains legal accuracy across languages
- **Cultural Adaptation**: Understands regional legal contexts
- **DataBase Check**: All the legal documents are assessed, checked in real time using pathway and then using Omnidimension API and our Backend API all through our pipeline

📊 **Professional Templates**

- Generate new contracts using AI including Employment agreements, NDAs, service contracts
- Customizable risk levels and complexity


## 🎯 Who Is This For?

- **Small Business Owners**: Review vendor contracts and agreements safely
- **Freelancers**: Understand client contracts before signing
- **Students**: Learn contract analysis and legal document structure
- **Legal Professionals**: Speed up preliminary document review
- **Anyone**: Who needs to understand legal documents without expensive legal fees


## 🚀 Quick Start

### 🌐 Try Online (Recommended)

Visit our live deployment: **[SignSafe Pro](https://signsafepro.onrender.com/)**

### 💻 Local Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/signsafe.git
cd signsafe
```

2. **Install dependencies**

```bash
python install_dependencies.py
```

3. **Configure API keys (Optional)**

```bash
cp .env.template .env
# Add your Google Gemini API key for enhanced AI features
```

4. **Run the application**

```bash
streamlit run app.py
```

5. **Open your browser** to the displayed URL (typically `http://localhost:8501`)

### 📋 Requirements

- **Python 3.8+**
- **Streamlit** for web interface
- **PyPDF2** for PDF processing
- **pytesseract** for OCR (Optional: for image documents)


## 🔧 How It Works

The application follows a modular pipeline architecture:

```
Document Upload → Text Extraction → Clause Segmentation → AI Simplification → Risk Analysis → Results Display
```

1. **Upload**: Drag \& drop PDFs or images (max 200MB)
2. **Extract**: Automatic text extraction with OCR fallback
3. **Analyze**: AI-powered clause identification and categorization into types like liability, termination, warranty, financial, confidentiality
4. **Simplify**: Convert legal language to plain English
5. **Assess**: Risk scoring and vulnerability detection
6. **Interact**: Ask questions and get translations

## 📱 Features in Detail

### Document Processing

- **Supported Formats**: PDF, PNG, JPG, JPEG, TIFF, BMP
- **Maximum File Size**: 200MB
- **Batch Processing**: Handle multiple documents simultaneously
- **Real-time Monitoring**: Auto-process files dropped in folders using Watchdog library


### AI Capabilities

- **Google Gemini Integration**: Advanced text processing and analysis
- **Omnidimension API**: Alternative AI service for processing
- **Fallback Processing**: Pattern-based analysis when APIs unavailable
- **Context Awareness**: Maintains legal context during simplification


### Security \& Privacy

- **Local Processing**: Documents processed on your machine
- **No Data Storage**: External services only receive text snippets, not full documents
- **API Security**: Environment-based key management
- **Privacy First**: No sensitive document metadata transmitted


## 🏗️ Architecture

SignSafe follows a modular pipeline architecture designed for scalability and maintainability[^1]:

### Core Components

- **User Interface**: Streamlit-based web application[^1]
- **Processing Pipeline**: OCR → Clause Splitting → Simplification → Risk Analysis[^1]
- **AI Integration**: Google Gemini and Omnidimension APIs with fallback services[^1]
- **Utility Layer**: Translation, monitoring, and voice chat handlers[^1]


### Technology Stack

- **Frontend**: Streamlit with custom styling[^1]
- **Backend**: Python with modular pipeline design[^1]
- **AI Services**: Google Gemini API, Omnidimension API[^1]
- **Document Processing**: PyPDF2, pytesseract, Pillow[^1]
- **Monitoring**: Watchdog for real-time file monitoring[^1]


## 📚 Documentation

### User Guides

- **[Architecture Guide](ARCHITECTURE.md)**: Technical architecture details[^1]
- **[User Guide](USER_GUIDE.md)**: Comprehensive usage instructions[^3]


### Quick Links

- [Installation Guide](#quick-start)
- [Troubleshooting](USER_GUIDE.md#troubleshooting)[^3]
- [Security \& Privacy](USER_GUIDE.md#security-and-privacy)[^3]


## 🤝 Contributing

We welcome contributions from the community! SignSafe is built to help democratize legal document understanding.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/yourusername/signsafe.git
cd signsafe
python install_dependencies.py
cp .env.template .env
streamlit run app.py
```


### Areas for Contribution

- **New Language Support**: Add translations for additional languages
- **Document Types**: Extend support for new contract types
- **AI Providers**: Integrate additional AI services
- **UI/UX Improvements**: Enhance user interface and experience
- **Performance Optimization**: Improve processing speed and efficiency


## 🛣️ Roadmap

### 🎯 Current (v1.0)

- ✅ Basic document analysis and simplification
- ✅ Risk assessment and scoring
- ✅ Multi-language translation
- ✅ Voice chat interface
- ✅ Contract template generation


### 🚀 Upcoming (v1.1)

- [ ] **Batch Document Processing**: Handle multiple contracts simultaneously[^1]
- [ ] **Advanced Clause Comparison**: Compare terms across documents[^1]
- [ ] **Export Functionality**: PDF reports and summaries[^1]
- [ ] **Document History**: Track analysis over time[^1]
- [ ] **Enhanced Mobile Experience**: Responsive design improvements


### 🔮 Future (v2.0)

- [ ] **Multi-user Collaboration**: Team contract review[^1]
- [ ] **Database Integration**: Persistent document storage[^1]
- [ ] **API Endpoints**: Third-party integrations[^1]
- [ ] **Advanced Analytics**: Usage patterns and insights[^1]
- [ ] **Cloud Deployment**: Scalable cloud infrastructure[^1]


## 📊 Performance Characteristics

- **PDF Extraction**: ~1-3 seconds per document[^1]
- **OCR Processing**: ~5-15 seconds depending on image quality[^1]
- **AI Simplification**: ~2-5 seconds per clause (with rate limiting)[^1]
- **Risk Analysis**: ~1-2 seconds per document[^1]


## 🔧 Troubleshooting

### Common Issues

**"No text extracted from document"**[^3]

- Check if the file is corrupted
- For images, ensure text is clearly visible
- Try converting the document to a different format

**"API key not working"**[^3]

- Verify the API key is correctly copied to `.env`
- Check that the key has proper permissions
- Ensure the API service is active and funded

**"Processing stuck"**[^3]

- Refresh the browser page
- Check the console for error messages
- Try uploading a smaller or simpler document first


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powering our intelligent text processing[^1][^2]
- **Streamlit Community** for the amazing web framework[^1]
- **Legal Tech Community** for feedback and feature suggestions
- **Open Source Contributors** who make this project possible
- **Beta Testers** who helped refine the user experience


## 📞 Contact \& Support

### 🐛 Found a Bug?

- [Report Issues](https://github.com/yourusername/signsafe/issues) on GitHub
- Check [Common Issues](USER_GUIDE.md#troubleshooting) first[^3]


### 💡 Have an Idea?

- [Feature Requests](https://github.com/yourusername/signsafe/discussions) welcome
- Join our community discussions


### 🆘 Need Help?

- [User Guide](USER_GUIDE.md) - Comprehensive documentation[^3]
- [FAQ Section](USER_GUIDE.md#frequently-asked-questions) - Common questions[^3]

<div align="center">

**Made with ❤️ for legal transparency and accessibility**

[🌐 **Try SignSafe Pro**](https://signsafepro.onrender.com/) | [⭐ **Star this repo**](https://github.com/yourusername/signsafe) | [🐦 **Follow updates**](https://twitter.com/signsafepro)

*"Democratizing legal document understanding, one contract at a time."*
