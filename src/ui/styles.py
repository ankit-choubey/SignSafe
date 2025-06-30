"""
Modern UI styles for SignSafe
Professional, clean styling components
"""

import streamlit as st

def inject_custom_css():
    """Inject custom CSS for modern professional UI."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Variables */
    :root {
        --primary-color: #2563eb;
        --primary-hover: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --border-color: #e2e8f0;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main App Container */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Custom Page Title */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(135deg, var(--primary-color), #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Navigation Tabs */
    .nav-container {
        background: var(--surface-color);
        border-radius: var(--radius-lg);
        padding: 0.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    /* Cards and Containers */
    .card {
        background: var(--surface-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }
    
    .card-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
        white-space: normal;
    }
    
    /* Metrics Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--surface-color), #f1f5f9);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Upload Area */
    .upload-area {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border: 2px dashed var(--border-color);
        border-radius: var(--radius-xl);
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 2rem 0;
    }
    
    .upload-area:hover {
        border-color: var(--primary-color);
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        margin: 0.25rem;
    }
    
    .status-high {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    
    .status-medium {
        background: #fffbeb;
        color: #d97706;
        border: 1px solid #fed7aa;
    }
    
    .status-low {
        background: #f0fdf4;
        color: #16a34a;
        border: 1px solid #bbf7d0;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: var(--radius-md);
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
        color: white;
    }
    
    /* Secondary Button */
    .stButton > button[kind="secondary"] {
        background: var(--surface-color);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    /* Expandable Sections */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
        background: var(--surface-color);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .streamlit-expanderContent {
        background: var(--surface-color);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--surface-color), #f8fafc);
        border-right: 1px solid var(--border-color);
    }
    
    /* Text Styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        font-weight: 600;
    }
    
    .stMarkdown p {
        font-family: 'Inter', sans-serif;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Code Blocks */
    .stCode {
        font-family: 'JetBrains Mono', monospace;
        background: #f1f5f9;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
    }
    
    /* Info/Warning/Error Messages */
    .stAlert {
        border-radius: var(--radius-md);
        border: none;
        box-shadow: var(--shadow-sm);
        font-family: 'Inter', sans-serif;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-color), #3b82f6);
        border-radius: var(--radius-sm);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary) !important;
    }
    
    /* Selectbox text and options */
    .stSelectbox div[data-baseweb="select"] {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        color: var(--text-primary) !important;
        background: var(--surface-color) !important;
    }
    
    /* Selectbox dropdown options */
    .stSelectbox ul {
        background: var(--surface-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox li {
        color: var(--text-primary) !important;
        background: var(--surface-color) !important;
    }
    
    .stSelectbox li:hover {
        background: rgba(37, 99, 235, 0.1) !important;
        color: var(--text-primary) !important;
    }
    
    /* Selectbox selected value */
    .stSelectbox [role="combobox"] {
        color: var(--text-primary) !important;
        background: var(--surface-color) !important;
    }
    
    /* Additional selectbox text fixes */
    .stSelectbox * {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox input {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Selectbox placeholder and value text */
    .stSelectbox [data-baseweb="select"] span {
        color: var(--text-primary) !important;
    }
    
    /* Make selectbox width fit content */
    .stSelectbox > div {
        max-width: fit-content !important;
        width: auto !important;
    }
    
    .stSelectbox select {
        width: auto !important;
        min-width: 200px !important;
        max-width: 300px !important;
    }
    
    /* Inline language selector styling */
    .language-selector-row {
        display: flex !important;
        align-items: center !important;
        gap: 15px !important;
        margin-bottom: 20px !important;
    }
    
    .language-selector-row .stSelectbox {
        margin: 0 !important;
        min-width: auto !important;
    }
    
    .language-selector-row .stSelectbox > div {
        margin: 0 !important;
    }
    
    /* Fix text visibility in clause sections */
    .stExpander .stMarkdown p {
        color: #ffffff !important;
        font-weight: 400 !important;
        opacity: 1 !important;
    }
    
    /* Ensure all text in expanders is visible */
    .stExpander div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    
    /* Original text styling */
    .stExpander .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Make sure all text content is visible */
    .stExpander * {
        color: inherit !important;
    }
    
    .stExpander p, .stExpander div {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    
    /* Risk indicator styling - fit content width */
    .stAlert {
        width: fit-content !important;
        max-width: 400px !important;
        display: inline-block !important;
    }
    
    .stAlert > div {
        width: fit-content !important;
        max-width: 400px !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: var(--surface-color);
        border: 2px dashed var(--border-color);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
    }
    
    /* Only target filename text specifically */
    .stFileUploader div[data-testid="stFileUploaderFileName"] {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        background: transparent !important;
    }
    
    /* Target uploaded file name display */
    .stFileUploader small {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Ensure browse button and drag text remain visible */
    .stFileUploader section[data-testid="stFileUploadDropzone"] {
        color: inherit !important;
    }
    
    .stFileUploader section[data-testid="stFileUploadDropzone"] button {
        color: inherit !important;
        background: inherit !important;
    }
    
    /* File upload help text visibility */
    .stFileUploader small,
    .stFileUploader [data-testid="stFileUploaderHelpText"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    
    /* File size and format text */
    .stFileUploader div[data-testid="stFileUploadDropzone"] small {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }
    
    /* More specific targeting for file upload limits text */
    .stFileUploader [data-baseweb="file-uploader"] small {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Additional targeting for file limits */
    .stFileUploader div small,
    .stFileUploader span small {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    

    

    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        .upload-area {
            padding: 2rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Create professional header with branding."""
    return """
    <div class="fade-in" style="text-align: center; padding: 2rem 0;">
        <h1 class="main-title">SignSafe</h1>
        <p class="main-subtitle">AI-Powered Legal Document Analysis Platform</p>
    </div>
    """

def create_card(title, content, icon="📄"):
    """Create a professional card component."""
    return f"""
    <div class="card fade-in">
        <div class="card-header">
            {icon} {title}
        </div>
        <div>
            {content}
        </div>
    </div>
    """

def create_metric_card(value, label, color="primary"):
    """Create a metric display card."""
    return f"""
    <div class="metric-card fade-in">
        <div class="metric-value" style="color: var(--{color}-color);">
            {value}
        </div>
        <div class="metric-label">
            {label}
        </div>
    </div>
    """

def create_status_pill(text, status="low"):
    """Create a status pill component."""
    return f"""
    <span class="status-pill status-{status}">
        {text}
    </span>
    """

def create_upload_area():
    """Create professional upload area."""
    return """
    <div class="upload-area">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
        <h3 style="margin-bottom: 0.5rem; color: var(--text-primary);">Upload Legal Document</h3>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Drag & drop your PDF or image files here, or click to browse
        </p>
    </div>
    """

def create_voice_chat_section():
    """Create simple voice chat section."""
    return ""