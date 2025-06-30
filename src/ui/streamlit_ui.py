import streamlit as st
import os
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any

# Import pipeline components
from pipeline.ocr_parser import OCRParser
from pipeline.clause_splitter import ClauseSplitter
from pipeline.simplifier import LegalSimplifier
from pipeline.risk_analyzer import RiskAnalyzer
from utils.pathway_monitor import PathwayMonitor
from utils.voice_chat import VoiceChatHandler
from utils.gemini_simplifier import GeminiSimplifier
from utils.translator import MultiLanguageTranslator
from ui.styles import inject_custom_css, create_header, create_card, create_metric_card, create_status_pill, create_upload_area, create_voice_chat_section

class SignSafeApp:
    """Main Streamlit application for SignSafe legal document analyzer."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Initialize pipeline components
        self.ocr_parser = OCRParser()
        self.clause_splitter = ClauseSplitter()
        self.simplifier = LegalSimplifier()
        self.risk_analyzer = RiskAnalyzer()
        self.voice_chat = VoiceChatHandler()
        self.gemini_simplifier = GeminiSimplifier()
        self.translator = MultiLanguageTranslator()
        
        # Initialize session state
        self.init_session_state()
        
        # Setup uploads directory
        self.uploads_dir = "uploads"
        os.makedirs(self.uploads_dir, exist_ok=True)
        
        # Initialize folder monitor
        self.setup_folder_monitor()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def init_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'processed_documents' not in st.session_state:
            st.session_state.processed_documents = {}
        
        if 'current_document' not in st.session_state:
            st.session_state.current_document = None
        
        if 'processing_status' not in st.session_state:
            st.session_state.processing_status = {}
        
        if 'voice_chat_active' not in st.session_state:
            st.session_state.voice_chat_active = False
        
        if 'app_mode' not in st.session_state:
            st.session_state.app_mode = "landing"  # landing, contract_review, contract_creation
        
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = "📤 Upload & Process"
    
    def setup_folder_monitor(self):
        """Setup Pathway folder monitoring."""
        try:
            self.pathway_monitor = PathwayMonitor(
                folder_path=self.uploads_dir,
                callback=self.process_new_file
            )
            
            # Start monitoring in a separate thread
            if 'monitor_thread' not in st.session_state:
                monitor_thread = threading.Thread(
                    target=self.pathway_monitor.start_monitoring,
                    daemon=True
                )
                monitor_thread.start()
                st.session_state.monitor_thread = monitor_thread
                
        except Exception as e:
            self.logger.error(f"Error setting up folder monitor: {str(e)}")
    
    def run(self):
        """Main application entry point."""
        # Inject custom CSS for professional styling
        inject_custom_css()
        
        # Route based on app mode
        if st.session_state.app_mode == "landing":
            self.render_landing_page()
        elif st.session_state.app_mode == "contract_review":
            self.render_contract_review_mode()
        elif st.session_state.app_mode == "contract_creation":
            self.render_contract_creation_mode()
    
    def render_landing_page(self):
        """Render the main landing page with two primary options."""
        # Professional header - only show on landing page
        st.markdown(create_header(), unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Main landing page content
        landing_html = """
        <div style="text-align: center; padding: 3rem 0;">
            <h2 style="color: var(--text-primary); font-size: 2.5rem; margin-bottom: 1rem; font-weight: 600;">
                Choose Your Service
            </h2>
            <p style="color: var(--text-secondary); font-size: 1.2rem; margin-bottom: 3rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Select the legal service you need. Whether reviewing existing contracts or creating new ones, we've got you covered.
            </p>
        </div>
        """
        st.markdown(landing_html, unsafe_allow_html=True)
        
        # Two main option cards
        col1, col2, col3 = st.columns([1, 8, 1])
        
        with col2:
            subcol1, subcol2 = st.columns(2)
            
            with subcol1:
                contract_review_card = """
                <div class="card" style="text-align: center; min-height: 300px; display: flex; flex-direction: column; justify-content: center; cursor: pointer; transition: all 0.3s ease;">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">📊</div>
                    <h3 style="color: var(--primary-color); font-size: 1.8rem; margin-bottom: 1rem;">Contract Review</h3>
                    <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
                        Upload and analyze existing legal documents. Get AI-powered risk assessment, clause simplification, and detailed insights.
                    </p>
                    <div style="margin-top: auto;">
                        <strong style="color: var(--primary-color);">• Document Upload & Analysis</strong><br>
                        <strong style="color: var(--primary-color);">• Risk Assessment</strong><br>
                        <strong style="color: var(--primary-color);">• Multi-Language Support</strong>
                    </div>
                </div>
                """
                st.markdown(contract_review_card, unsafe_allow_html=True)
                
                if st.button("Start Contract Review", key="start_review", type="primary", use_container_width=True):
                    st.session_state.app_mode = "contract_review"
                    st.rerun()
            
            with subcol2:
                contract_creation_card = """
                <div class="card" style="text-align: center; min-height: 300px; display: flex; flex-direction: column; justify-content: center; cursor: pointer; transition: all 0.3s ease;">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">📝</div>
                    <h3 style="color: var(--primary-color); font-size: 1.8rem; margin-bottom: 1rem;">Contract Creation</h3>
                    <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
                        Generate professional legal contracts from scratch. AI-powered templates customized for your specific needs and jurisdiction.
                    </p>
                    <div style="margin-top: auto;">
                        <strong style="color: var(--primary-color);">• AI-Generated Templates</strong><br>
                        <strong style="color: var(--primary-color);">• Multiple Contract Types</strong><br>
                        <strong style="color: var(--primary-color);">• Jurisdiction-Specific</strong>
                    </div>
                </div>
                """
                st.markdown(contract_creation_card, unsafe_allow_html=True)
                
                if st.button("Start Contract Creation", key="start_creation", type="primary", use_container_width=True):
                    st.session_state.app_mode = "contract_creation"
                    st.rerun()
    
    def render_contract_review_mode(self):
        """Render the contract review mode without navigation buttons."""
        # Check if there's a current document to review
        if (st.session_state.current_document and 
            st.session_state.current_document in st.session_state.processed_documents):
            # Show document analysis automatically after processing
            self.render_document_analysis()
        else:
            # Show upload tab if no document is processed
            self.render_upload_tab()
    
    def render_document_analysis(self):
        """Render the document analysis view."""
        if st.session_state.current_document:
            doc_data = st.session_state.processed_documents[st.session_state.current_document]
            self.display_document_analysis(doc_data)
        
        # Add option to upload new document
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Upload New Document", key="upload_new_doc", type="secondary", use_container_width=True):
                st.session_state.current_document = None
                # Reset risk summary toggle when uploading new document
                st.session_state.show_risk_summary = False
                st.rerun()
    
    def render_contract_creation_mode(self):
        """Render the contract creation mode without navigation buttons."""
        # Show contract templates directly without navigation
        self.render_contract_templates_tab()
    
    def render_navigation_bar(self, mode):
        """Render navigation bar based on mode."""
        # Back to home button
        col1, col2 = st.columns([1, 8])
        with col1:
            if st.button("🏠 Home", key="back_home", use_container_width=True):
                st.session_state.app_mode = "landing"
                st.rerun()
        
        st.markdown('<div class="nav-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
        
        if mode == "contract_review":
            # Contract Review navigation
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📤 Upload & Process", key="nav_upload", use_container_width=True):
                    st.session_state.active_tab = "📤 Upload & Process"
            with col2:
                if st.button("📊 Document Review", key="nav_review", use_container_width=True):
                    st.session_state.active_tab = "📊 Document Review"
            with col3:
                if st.button("🎯 Risk Summary", key="nav_risk", use_container_width=True):
                    st.session_state.active_tab = "🎯 Risk Summary"
        
        elif mode == "contract_creation":
            # Contract Creation navigation (single tab)
            col1, col2, col3 = st.columns([2, 4, 2])
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 1rem; background: var(--primary-color); color: white; border-radius: 8px; font-weight: 600;">
                    📝 Contract Creation
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with document list and status."""
        st.sidebar.header("📁 Documents")
        
        # Show folder monitoring status
        if os.path.exists(self.uploads_dir):
            file_count = len([f for f in os.listdir(self.uploads_dir) 
                            if f.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg'))])
            st.sidebar.info(f"Monitoring: {self.uploads_dir}/\nFiles: {file_count}")
        
        # Document list
        if st.session_state.processed_documents:
            st.sidebar.subheader("Processed Documents")
            
            for doc_name, doc_data in st.session_state.processed_documents.items():
                # Truncate long filenames for sidebar display
                display_doc_name = doc_name if len(doc_name) <= 25 else f"{doc_name[:22]}..."
                
                with st.sidebar.expander(f"📄 {display_doc_name}"):
                    # Show full filename in the content if truncated
                    if len(doc_name) > 25:
                        st.write(f"**File:** {doc_name}")
                    
                    st.write(f"**Processed:** {doc_data.get('timestamp', 'Unknown')}")
                    st.write(f"**Clauses:** {len(doc_data.get('clauses', []))}")
                    
                    risk_summary = doc_data.get('risk_summary', {})
                    overall_risk = risk_summary.get('overall_risk', 'unknown')
                    
                    if overall_risk == 'high':
                        st.error(f"🔴 High Risk")
                    elif overall_risk == 'medium':
                        st.warning(f"🟡 Medium Risk")
                    else:
                        st.success(f"🟢 Low Risk")
                    
                    # Truncate button text for long filenames
                    button_text = f"View {doc_name}" if len(doc_name) <= 15 else "View Document"
                    if st.button(button_text, key=f"view_{doc_name}"):
                        st.session_state.current_document = doc_name
                        st.rerun()
        else:
            st.sidebar.info("No documents processed yet.")
        
        # API Status
        st.sidebar.subheader("🔗 API Status")
        omnidimension_key = os.getenv("OMNIDIMENSION_API_KEY", "")
        if omnidimension_key:
            st.sidebar.success("✅ Omnidimension API Connected")
        else:
            st.sidebar.warning("⚠️ Omnidimension API Not Connected")
    
    def render_upload_tab(self):
        """Render the file upload and processing tab with modern design."""
        # Professional upload area
        st.markdown(create_upload_area(), unsafe_allow_html=True)
        
        # File upload with custom styling
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            help="Upload PDF or image files containing legal text",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # File info card with proper text overflow handling
            # Truncate long filenames for display
            display_name = uploaded_file.name if len(uploaded_file.name) <= 30 else f"{uploaded_file.name[:27]}..."
            
            file_info_html = f"""
            <div class="card">
                <div class="card-header">📄 File Information</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                    <div class="metric-card">
                        <div class="metric-value" style="font-size: 1.2rem; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%;" title="{uploaded_file.name}">{display_name}</div>
                        <div class="metric-label">File Name</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" style="font-size: 1.5rem;">{uploaded_file.size:,}</div>
                        <div class="metric-label">Size (bytes)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" style="font-size: 1.5rem;">{uploaded_file.type}</div>
                        <div class="metric-label">File Type</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(file_info_html, unsafe_allow_html=True)
            
            # Analyze button with enhanced styling
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
                    self.process_uploaded_file(uploaded_file)
        
        # Processing status with modern cards
        if st.session_state.processing_status:
            st.markdown('<div class="card"><div class="card-header">⚙️ Processing Status</div>', unsafe_allow_html=True)
            for filename, status in st.session_state.processing_status.items():
                self.display_processing_status(filename, status)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def render_review_tab(self):
        """Render the document review tab."""
        st.header("Document Review")
        
        # Language selector
        if self.translator.is_available():
            col1, col2 = st.columns([2, 1])
            with col2:
                languages = self.translator.get_supported_languages()
                language_options = ["English"] + [f"{lang.title()} ({script})" for lang, script in languages.items()]
                
                selected_language = st.selectbox(
                    "Choose your preferred language:",
                    language_options,
                    key="selected_language"
                )
                
                # Store selected language
                if selected_language == "English":
                    st.session_state.translation_language = None
                else:
                    # Extract language code from selection
                    for lang_code, script in languages.items():
                        if f"{lang_code.title()} ({script})" == selected_language:
                            st.session_state.translation_language = lang_code
                            break
        else:
            st.warning("Translation service not available. Please check GEMINI_API_KEY.")
        
        if not st.session_state.current_document and st.session_state.processed_documents:
            # Auto-select the most recent document
            doc_names = list(st.session_state.processed_documents.keys())
            st.session_state.current_document = doc_names[-1]
        
        if st.session_state.current_document:
            doc_data = st.session_state.processed_documents[st.session_state.current_document]
            self.display_document_analysis(doc_data)
        else:
            st.info("No document selected. Upload and analyze a document first.")
    
    def render_risk_summary_tab(self):
        """Render the risk summary tab."""
        st.header("Risk Analysis Summary")
        
        if st.session_state.current_document:
            doc_data = st.session_state.processed_documents[st.session_state.current_document]
            risk_summary = doc_data.get('risk_summary', {})
            
            if risk_summary:
                self.display_risk_summary(risk_summary)
            else:
                st.warning("No risk analysis available for this document.")
        else:
            st.info("Select a document to view risk analysis.")
    

    
    def render_contract_templates_tab(self):
        """Render the contract templates generation tab."""
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 24px;">📋 AI Contract Templates</h2>
            <p style="margin: 10px 0 0 0; font-size: 16px;">Generate custom legal contracts using AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contract type selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            contract_type = st.selectbox(
                "Select Contract Type:",
                [
                    "Employment Agreement", 
                    "Non-Disclosure Agreement (NDA)", 
                    "Service Agreement", 
                    "Rental/Lease Agreement", 
                    "Sales Agreement", 
                    "Partnership Agreement",
                    "Consulting Agreement",
                    "Software License Agreement",
                    "Freelance Agreement",
                    "Custom Contract"
                ]
            )
        
        with col2:
            jurisdiction = st.selectbox(
                "Legal Jurisdiction:",
                ["India", "USA", "UK", "Canada", "Australia", "Other"]
            )
        
        # Contract details form
        st.subheader("Contract Details")
        
        # Basic information
        col3, col4 = st.columns(2)
        
        with col3:
            party1_name = st.text_input("First Party Name:", placeholder="Company or Individual Name")
            party1_type = st.selectbox("First Party Type:", ["Company", "Individual", "Organization"])
            
        with col4:
            party2_name = st.text_input("Second Party Name:", placeholder="Company or Individual Name")
            party2_type = st.selectbox("Second Party Type:", ["Company", "Individual", "Organization"])
        
        # Contract-specific details
        st.subheader("Specific Requirements")
        
        if contract_type == "Employment Agreement":
            col5, col6 = st.columns(2)
            with col5:
                job_title = st.text_input("Job Title:", placeholder="e.g., Software Developer")
                salary = st.text_input("Salary/Compensation:", placeholder="e.g., ₹50,000 per month")
            with col6:
                start_date = st.date_input("Start Date:")
                employment_type = st.selectbox("Employment Type:", ["Full-time", "Part-time", "Contract"])
                
        elif contract_type == "Non-Disclosure Agreement (NDA)":
            purpose = st.text_area("Purpose of NDA:", placeholder="e.g., Discussion of potential business partnership")
            duration = st.selectbox("NDA Duration:", ["1 year", "2 years", "3 years", "5 years", "Indefinite"])
            
        elif contract_type == "Service Agreement":
            service_description = st.text_area("Service Description:", placeholder="Describe the services to be provided")
            payment_terms = st.text_input("Payment Terms:", placeholder="e.g., ₹10,000 upon completion")
            duration = st.text_input("Service Duration:", placeholder="e.g., 3 months")
            
        elif contract_type == "Rental/Lease Agreement":
            col7, col8 = st.columns(2)
            with col7:
                property_address = st.text_area("Property Address:")
                rent_amount = st.text_input("Monthly Rent:", placeholder="e.g., ₹25,000")
            with col8:
                lease_duration = st.selectbox("Lease Duration:", ["6 months", "1 year", "2 years", "3 years"])
                security_deposit = st.text_input("Security Deposit:", placeholder="e.g., ₹50,000")
                
        # Additional clauses
        st.subheader("Additional Requirements")
        special_clauses = st.text_area(
            "Special Clauses or Requirements:", 
            placeholder="Any specific terms, conditions, or clauses you want to include...",
            height=100
        )
        
        # Risk preferences
        col9, col10 = st.columns(2)
        with col9:
            risk_level = st.selectbox(
                "Risk Tolerance:",
                ["Conservative (More protection)", "Balanced", "Liberal (More flexibility)"]
            )
        with col10:
            language_complexity = st.selectbox(
                "Language Complexity:",
                ["Simple (Easy to understand)", "Standard (Legal but clear)", "Complex (Full legal language)"]
            )
        
        # Generate button
        if st.button("🚀 Generate Contract Template", type="primary"):
            if party1_name and party2_name:
                with st.spinner("Generating your custom contract template..."):
                    contract_content = self.generate_contract_template(
                        contract_type, jurisdiction, party1_name, party1_type, 
                        party2_name, party2_type, special_clauses, risk_level,
                        language_complexity, locals()
                    )
                    
                    if contract_content:
                        st.success("Contract template generated successfully!")
                        
                        # Display the contract
                        st.subheader("Generated Contract Template")
                        
                        # Create download button
                        st.download_button(
                            label="📄 Download Contract (TXT)",
                            data=contract_content,
                            file_name=f"{contract_type.replace(' ', '_')}_template.txt",
                            mime="text/plain"
                        )
                        
                        # Display contract in expandable section
                        with st.expander("📋 View Contract Template", expanded=True):
                            st.text_area(
                                "Contract Content:",
                                value=contract_content,
                                height=400,
                                disabled=True
                            )
                        
                        # Risk analysis of generated contract
                        st.subheader("📊 Template Risk Analysis")
                        risk_analysis = self.analyze_template_risks(contract_content, contract_type)
                        
                        col11, col12, col13 = st.columns(3)
                        with col11:
                            st.metric("Risk Level", risk_analysis.get('risk_level', 'Medium'))
                        with col12:
                            st.metric("Completeness", f"{risk_analysis.get('completeness', 85)}%")
                        with col13:
                            st.metric("Legal Strength", risk_analysis.get('legal_strength', 'Good'))
                        
                        # Risk recommendations
                        if risk_analysis.get('recommendations'):
                            st.warning("⚠️ Recommendations:")
                            for rec in risk_analysis['recommendations']:
                                st.write(f"• {rec}")
                        
                        # Next steps
                        st.info("""
                        **Next Steps:**
                        1. Review the generated template carefully
                        2. Consult with a legal professional for jurisdiction-specific advice
                        3. Customize the template for your specific needs
                        4. Have all parties review before signing
                        """)
                    else:
                        st.error("Failed to generate contract template. Please try again.")
            else:
                st.error("Please fill in both party names to generate the contract.")
    
    def generate_contract_template(self, contract_type, jurisdiction, party1_name, party1_type, 
                                 party2_name, party2_type, special_clauses, risk_level, 
                                 language_complexity, form_data):
        """Generate AI-powered contract template using Gemini AI."""
        try:
            # Check if Gemini API is available
            import google.generativeai as genai
            
            gemini_key = os.getenv('GEMINI_API_KEY')
            if not gemini_key:
                return self.generate_basic_contract_template(contract_type, party1_name, party2_name, form_data)
            
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Create detailed prompt based on contract type and requirements
            prompt = f"""
            Generate a comprehensive {contract_type} for {jurisdiction} jurisdiction with the following details:
            
            **Parties:**
            - First Party: {party1_name} ({party1_type})
            - Second Party: {party2_name} ({party2_type})
            
            **Contract Requirements:**
            - Contract Type: {contract_type}
            - Jurisdiction: {jurisdiction}
            - Risk Level: {risk_level}
            - Language Complexity: {language_complexity}
            
            **Specific Details:**
            {self.extract_contract_specifics(contract_type, form_data)}
            
            **Special Requirements:**
            {special_clauses if special_clauses else "No special clauses specified"}
            
            **Instructions:**
            1. Create a complete, legally sound contract template
            2. Include all standard clauses for this contract type
            3. Use {language_complexity.split('(')[0].strip().lower()} language
            4. Include appropriate protection based on {risk_level.split('(')[0].strip().lower()} risk tolerance
            5. Make it specific to {jurisdiction} legal requirements
            6. Include signature blocks and date fields
            7. Add clear section headers and numbering
            8. Include termination and dispute resolution clauses
            
            Format the contract professionally with proper legal structure.
            """
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Error generating AI contract: {str(e)}")
            return self.generate_basic_contract_template(contract_type, party1_name, party2_name, form_data)
    
    def extract_contract_specifics(self, contract_type, form_data):
        """Extract contract-specific details from form data."""
        specifics = []
        
        if contract_type == "Employment Agreement":
            if form_data.get('job_title'):
                specifics.append(f"Job Title: {form_data['job_title']}")
            if form_data.get('salary'):
                specifics.append(f"Compensation: {form_data['salary']}")
            if form_data.get('employment_type'):
                specifics.append(f"Employment Type: {form_data['employment_type']}")
                
        elif contract_type == "Non-Disclosure Agreement (NDA)":
            if form_data.get('purpose'):
                specifics.append(f"Purpose: {form_data['purpose']}")
            if form_data.get('duration'):
                specifics.append(f"Duration: {form_data['duration']}")
                
        elif contract_type == "Service Agreement":
            if form_data.get('service_description'):
                specifics.append(f"Services: {form_data['service_description']}")
            if form_data.get('payment_terms'):
                specifics.append(f"Payment: {form_data['payment_terms']}")
                
        elif contract_type == "Rental/Lease Agreement":
            if form_data.get('property_address'):
                specifics.append(f"Property: {form_data['property_address']}")
            if form_data.get('rent_amount'):
                specifics.append(f"Rent: {form_data['rent_amount']}")
            if form_data.get('lease_duration'):
                specifics.append(f"Lease Term: {form_data['lease_duration']}")
                
        return "\n".join(specifics) if specifics else "Standard contract terms apply"
    
    def generate_basic_contract_template(self, contract_type, party1_name, party2_name, form_data):
        """Generate basic contract template when AI is not available."""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        template = f"""
{contract_type.upper()}

This {contract_type} ("Agreement") is entered into on {current_date}, between:

FIRST PARTY: {party1_name} ("First Party")
SECOND PARTY: {party2_name} ("Second Party")

WHEREAS, the parties wish to enter into this agreement for the purposes outlined herein;

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:

1. PURPOSE AND SCOPE
   [Specify the purpose and scope of this agreement]

2. TERMS AND CONDITIONS
   [Detail the specific terms and conditions]

3. PAYMENT TERMS
   [Specify payment terms and schedules]

4. DURATION
   [Specify the duration of this agreement]

5. TERMINATION
   This agreement may be terminated by either party with [30] days written notice.

6. CONFIDENTIALITY
   Both parties agree to maintain confidentiality of any proprietary information shared.

7. GOVERNING LAW
   This agreement shall be governed by the laws of [Jurisdiction].

8. DISPUTE RESOLUTION
   Any disputes shall be resolved through [mediation/arbitration].

9. ENTIRE AGREEMENT
   This agreement constitutes the entire agreement between the parties.

IN WITNESS WHEREOF, the parties have executed this agreement on the date first written above.

FIRST PARTY:                    SECOND PARTY:

_____________________          _____________________
{party1_name}                  {party2_name}
Date: _______________          Date: _______________

        """
        return template.strip()
    
    def analyze_template_risks(self, contract_content, contract_type):
        """Analyze the generated contract template for potential risks."""
        risks = {
            'risk_level': 'Medium',
            'completeness': 85,
            'legal_strength': 'Good',
            'recommendations': []
        }
        
        # Basic risk analysis based on content
        content_lower = contract_content.lower()
        
        # Check for important clauses
        important_clauses = [
            'termination', 'liability', 'confidentiality', 
            'dispute resolution', 'governing law', 'payment'
        ]
        
        missing_clauses = [clause for clause in important_clauses 
                          if clause not in content_lower]
        
        if missing_clauses:
            risks['recommendations'].extend([
                f"Consider adding {clause} clause" for clause in missing_clauses
            ])
            risks['completeness'] = max(60, 85 - len(missing_clauses) * 5)
        
        # Risk level based on contract type
        high_risk_contracts = ['Partnership Agreement', 'Employment Agreement']
        if contract_type in high_risk_contracts:
            risks['risk_level'] = 'High'
            risks['recommendations'].append("High-risk contract type - strongly recommend legal review")
        
        # Check for jurisdiction-specific requirements
        if 'governing law' not in content_lower:
            risks['recommendations'].append("Specify governing law and jurisdiction")
        
        return risks
    
    def process_uploaded_file(self, uploaded_file):
        """Process an uploaded file through the analysis pipeline."""
        filename = uploaded_file.name
        
        # Initialize processing status
        st.session_state.processing_status[filename] = {
            'stage': 'Starting',
            'progress': 0,
            'status': 'processing'
        }
        
        # Create progress container
        progress_container = st.container()
        
        try:
            with progress_container:
                # Stage 1: Text Extraction
                self.update_processing_status(filename, 'Extracting text...', 20)
                
                text = self.ocr_parser.extract_text_from_uploaded_file(uploaded_file)
                
                if not text.strip():
                    st.error("Could not extract text from the document.")
                    return
                
                # Stage 2: Clause Splitting
                self.update_processing_status(filename, 'Splitting into clauses...', 40)
                
                clauses = self.clause_splitter.split_into_clauses(text)
                
                # Stage 3: Add explanations (skip automatic simplification)
                self.update_processing_status(filename, 'Adding explanations...', 60)
                
                # Add explanations without automatic simplification
                for clause in clauses:
                    # Generate explanation using the existing simplifier's explanation method
                    simplified_result = self.simplifier.simplify_clause(clause['text'], clause['type'])
                    clause['explanation'] = simplified_result.get('explanation', 'This clause contains important legal terms.')
                    clause['original'] = clause['text']  # Ensure 'original' field exists
                
                # Stage 4: Risk Analysis
                self.update_processing_status(filename, 'Analyzing risks...', 80)
                
                for clause in clauses:
                    risk_analysis = self.risk_analyzer.analyze_risk(
                        clause['original'],
                        clause['type'],
                        clause['importance']
                    )
                    clause.update(risk_analysis)
                
                # Stage 5: Generate Summary
                self.update_processing_status(filename, 'Generating summary...', 90)
                
                risk_summary = self.risk_analyzer.generate_risk_summary(clauses)
                clause_summary = self.clause_splitter.get_clause_summary(clauses)
                
                # Stage 6: Complete
                self.update_processing_status(filename, 'Complete!', 100)
                
                # Store results
                st.session_state.processed_documents[filename] = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'original_text': text,
                    'clauses': clauses,
                    'risk_summary': risk_summary,
                    'clause_summary': clause_summary
                }
                
                st.session_state.current_document = filename
                
                # Professional success notification
                success_html = f"""
                <div class="card" style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; margin: 1rem 0; border: none;">
                    <div style="padding: 1.5rem; text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎉</div>
                        <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">Analysis Complete</div>
                        <div style="font-size: 1rem; opacity: 0.9;">Document '{filename[:30]}{'...' if len(filename) > 30 else ''}' has been successfully processed and analyzed</div>
                        <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.2); border-radius: 8px; font-size: 0.9rem;">
                            Automatically showing detailed clause analysis below
                        </div>
                    </div>
                </div>
                """
                st.markdown(success_html, unsafe_allow_html=True)
                
                # Clear processing status
                if filename in st.session_state.processing_status:
                    del st.session_state.processing_status[filename]
                
                # Wait a moment for user to see success message, then automatically show analysis
                time.sleep(2)
                st.rerun()
                
        except Exception as e:
            self.logger.error(f"Error processing uploaded file: {str(e)}")
            st.error(f"Error processing document: {str(e)}")
            
            # Update status to error
            if filename in st.session_state.processing_status:
                st.session_state.processing_status[filename]['status'] = 'error'
                st.session_state.processing_status[filename]['stage'] = f'Error: {str(e)}'
    
    def process_new_file(self, file_path: str):
        """Process a new file detected by the folder monitor."""
        try:
            filename = os.path.basename(file_path)
            self.logger.info(f"Processing new file from folder: {filename}")
            
            # Initialize processing status
            st.session_state.processing_status[filename] = {
                'stage': 'Starting',
                'progress': 0,
                'status': 'processing'
            }
            
            # Process the file
            text = self.ocr_parser.process_file(file_path)
            
            if text.strip():
                clauses = self.clause_splitter.split_into_clauses(text)
                
                # Add explanations without automatic simplification
                for clause in clauses:
                    simplified_result = self.simplifier.simplify_clause(clause['text'], clause['type'])
                    clause['explanation'] = simplified_result.get('explanation', 'This clause contains important legal terms.')
                    clause['original'] = clause['text']
                
                for clause in clauses:
                    risk_analysis = self.risk_analyzer.analyze_risk(
                        clause['original'],
                        clause['type'],
                        clause['importance']
                    )
                    clause.update(risk_analysis)
                
                risk_summary = self.risk_analyzer.generate_risk_summary(clauses)
                clause_summary = self.clause_splitter.get_clause_summary(clauses)
                
                # Store results
                st.session_state.processed_documents[filename] = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'original_text': text,
                    'clauses': clauses,
                    'risk_summary': risk_summary,
                    'clause_summary': clause_summary
                }
                
                # Clear processing status
                if filename in st.session_state.processing_status:
                    del st.session_state.processing_status[filename]
                
                self.logger.info(f"Successfully processed: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error processing new file {file_path}: {str(e)}")
    
    def update_processing_status(self, filename: str, stage: str, progress: int):
        """Update processing status for a file."""
        if filename in st.session_state.processing_status:
            st.session_state.processing_status[filename].update({
                'stage': stage,
                'progress': progress
            })
    
    def display_processing_status(self, filename: str, status: Dict[str, Any]):
        """Display processing status for a file."""
        with st.container():
            st.write(f"**{filename}**")
            
            if status['status'] == 'processing':
                st.progress(status['progress'] / 100)
                st.write(f"Stage: {status['stage']}")
            elif status['status'] == 'error':
                st.error(f"Error: {status['stage']}")
            else:
                st.success("Processing complete!")
    
    def display_document_analysis(self, doc_data: Dict[str, Any]):
        """Display comprehensive document analysis with modern design."""
        # Document header with proper filename handling
        filename = st.session_state.current_document
        # Truncate long filenames for display
        display_filename = filename if len(filename) <= 50 else f"{filename[:47]}..."
        
        doc_header_html = f"""
        <div class="card">
            <div class="card-header" style="word-wrap: break-word; overflow-wrap: break-word; max-width: 100%; white-space: normal;">
                📄 <span title="{filename}" style="display: inline-block; max-width: calc(100% - 30px); text-overflow: ellipsis; overflow: hidden; white-space: nowrap; vertical-align: top;">{display_filename}</span>
            </div>
        </div>
        """
        st.markdown(doc_header_html, unsafe_allow_html=True)
        
        # Document metrics with modern cards
        risk_summary = doc_data.get('risk_summary', {})
        high_risk_count = risk_summary.get('high_risk_count', 0)
        overall_risk = risk_summary.get('overall_risk', 'unknown')
        
        # Risk status color
        risk_color = "error" if overall_risk == 'high' else "warning" if overall_risk == 'medium' else "success"
        risk_icon = "🔴" if overall_risk == 'high' else "🟡" if overall_risk == 'medium' else "🟢"
        
        # Display metrics using Streamlit columns to avoid HTML rendering issues
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_metric_card(len(doc_data.get('clauses', [])), "Total Clauses", "primary"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(high_risk_count, "High Risk Clauses", "error"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(f"{risk_icon} {overall_risk.title()}", "Overall Risk Level", risk_color), unsafe_allow_html=True)
        
        # Add spacing before Clause Analysis
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Clause analysis
        st.subheader("📋 Clause Analysis")
        
        # Language selection for translation
        if self.translator.is_available():
            supported_languages = self.translator.get_supported_languages()
            language_options = ["English (Original)"] + list(supported_languages.keys())
            
            # Create seamless inline layout
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <span style="color: white; font-size: 16px; white-space: nowrap;">Select language for clause translation:</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Position selectbox inline using negative margin
            st.markdown('<div style="margin-top: -45px; margin-left: 350px; width: 250px;">', unsafe_allow_html=True)
            selected_language = st.selectbox(
                "Language",
                language_options,
                key="language_selector",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Handle language selection
            if selected_language != "English (Original)":
                translation_language = None
                for code, name in supported_languages.items():
                    if code == selected_language:
                        translation_language = code
                        break
                st.session_state.translation_language = translation_language
            else:
                st.session_state.translation_language = None
            
            # Show translate button if language is selected
            if st.session_state.get('translation_language'):
                translation_language = st.session_state.translation_language
                if translation_language:  # Type safety check
                    doc_translate_key = f"doc_translated_{st.session_state.current_document}_{translation_language}"
                    
                    if st.button("🌐 Translate All Clauses", type="primary", key="translate_all_btn"):
                        language_name = supported_languages.get(translation_language, translation_language)
                        with st.spinner(f"Translating all clauses to {language_name}... This may take a few minutes."):
                            # Get current clauses
                            current_clauses = doc_data.get('clauses', [])
                            # Use batch translation method
                            translated_clauses = self.translator.translate_document_clauses(current_clauses, translation_language)
                            
                            # Update the document with translated clauses
                            st.session_state.processed_documents[st.session_state.current_document]['clauses'] = translated_clauses
                            st.session_state[doc_translate_key] = True
                            
                            # Clear individual translation cache
                            for i in range(len(current_clauses)):
                                translate_key = f"translated_{i}_{translation_language}_{current_clauses[i].get('id', i)}"
                                if translate_key in st.session_state:
                                    del st.session_state[translate_key]
                            
                            st.success(f"Successfully translated all {len(current_clauses)} clauses!")
                            st.rerun()
                    
                    # Show current translation status
                    if doc_translate_key in st.session_state:
                        st.success("Document translated!")
        
        # Get clauses (updated or original)
        clauses = doc_data.get('clauses', [])
        translation_language = st.session_state.get('translation_language')
        
        # Update clauses reference after potential translation
        if translation_language and st.session_state.current_document in st.session_state.processed_documents:
            clauses = st.session_state.processed_documents[st.session_state.current_document]['clauses']
        
        for i, clause in enumerate(clauses):
            with st.expander(f"Clause {i+1}: {clause.get('type', 'General').title()} ({clause.get('risk_level', 'unknown')} risk)"):
                
                # Risk information at the top
                if clause.get('risk_level'):
                    risk_level = clause['risk_level']
                    risk_color = clause.get('color', 'gray')
                    
                    if risk_level == 'high':
                        st.error(f"🔴 High Risk - Score: {clause.get('risk_score', 0)}")
                    elif risk_level == 'medium':
                        st.warning(f"🟡 Medium Risk - Score: {clause.get('risk_score', 0)}")
                    else:
                        st.success(f"🟢 Low Risk - Score: {clause.get('risk_score', 0)}")
                
                # Display text based on translation availability
                if translation_language:
                    # Check if clause has been translated
                    if clause.get('original_translated'):
                        st.write(f"**Text in {self.translator.get_supported_languages().get(translation_language, translation_language)}:**")
                        st.write(clause['original_translated'])
                        
                        # Show original as expandable section
                        with st.expander("Show English version", expanded=False):
                            st.write(clause.get('original', ''))
                    else:
                        st.write("**Original Text (English):**")
                        st.write(clause.get('original', ''))
                        st.info("Use 'Translate All Clauses' button above to translate this document.")
                else:
                    st.write("**Original Text:**")
                    st.write(clause.get('original', ''))
                
                # Explanation section
                st.write("**What This Means:**")
                if translation_language and clause.get('explanation_translated'):
                    st.info(clause['explanation_translated'])
                else:
                    explanation = clause.get('explanation', 'This clause contains important legal terms that should be reviewed carefully.')
                    st.info(explanation)
                
                # Simplified text display
                st.write("**Simplified Version:**")
                
                # Check if we have translated simplified text
                if translation_language and clause.get('simplified_translated'):
                    st.success(clause['simplified_translated'])
                elif clause.get('simplified'):
                    st.success(clause['simplified'])
                else:
                    # Create unique key for each clause
                    simplify_key = f"simplify_{i}_{clause.get('id', i)}"
                    simplified_key = f"simplified_{i}_{clause.get('id', i)}"
                    
                    # Check if this clause has been simplified
                    if simplified_key not in st.session_state:
                        st.session_state[simplified_key] = None
                    
                    if st.session_state[simplified_key] is None:
                        # Show simplify button
                        if st.button(f"🤖 Simplify with AI", key=simplify_key, type="primary"):
                            with st.spinner("Simplifying with Gemini AI..."):
                                try:
                                    if self.gemini_simplifier.is_available():
                                        result = self.gemini_simplifier.simplify_clause(
                                            clause.get('original', ''), 
                                            clause.get('type', 'general')
                                        )
                                        
                                        if 'error' in result:
                                            st.error(f"❌ {result['error']}")
                                            st.session_state[simplified_key] = f"**Error:** {result['error']}"
                                        else:
                                            st.session_state[simplified_key] = result['simplified']
                                            # Update the clause in session state
                                            st.session_state.processed_documents[st.session_state.current_document]['clauses'][i]['simplified'] = result['simplified']
                                            st.success("✅ Simplified successfully!")
                                            time.sleep(1)
                                        
                                        st.rerun()
                                    else:
                                        error_msg = "Gemini API not available. Please check your GEMINI_API_KEY."
                                        st.error(f"❌ {error_msg}")
                                        st.session_state[simplified_key] = f"**Error:** {error_msg}"
                                        st.rerun()
                                except Exception as e:
                                    error_msg = f"Unexpected error: {str(e)}"
                                    st.error(f"❌ {error_msg}")
                                    st.session_state[simplified_key] = f"**Error:** {error_msg}"
                                    st.rerun()
                        

                    else:
                        # Show simplified text and reset button
                        st.success(st.session_state[simplified_key])
                        if st.button(f"🔄 Simplify Again", key=f"reset_{i}_{clause.get('id', i)}", type="secondary"):
                            st.session_state[simplified_key] = None
                            st.rerun()
                

                
                # Risk factors
                risk_factors = clause.get('risk_factors', [])
                if risk_factors:
                    st.write("**Risk Factors:**")
                    for factor in risk_factors:
                        st.write(f"• {factor}")
                
                # Warnings
                warnings = clause.get('warnings', [])
                if warnings:
                    st.write("**Warnings:**")
                    # Use translated warnings if available, otherwise original
                    if translation_language and clause.get('warnings_translated'):
                        for warning in clause['warnings_translated']:
                            st.warning(warning)
                    else:
                        for warning in warnings:
                            st.warning(warning)
                
                # Recommendations
                recommendations = clause.get('recommendations', [])
                if recommendations:
                    st.write("**Recommendations:**")
                    
                    # Get the recommendations to display
                    recs_to_display = []
                    if translation_language and clause.get('recommendations_translated'):
                        recs_to_display = clause['recommendations_translated']
                    else:
                        recs_to_display = recommendations
                    
                    # Display recommendations in two columns
                    if len(recs_to_display) > 1:
                        # Split recommendations into two groups
                        mid_point = (len(recs_to_display) + 1) // 2
                        left_recs = recs_to_display[:mid_point]
                        right_recs = recs_to_display[mid_point:]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            for rec in left_recs:
                                st.info(f"💡 {rec}")
                        
                        with col2:
                            for rec in right_recs:
                                st.info(f"💡 {rec}")
                    else:
                        # Single recommendation, display normally
                        for rec in recs_to_display:
                            st.info(f"💡 {rec}")
        
        # Toggle button for Risk Summary
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Initialize risk summary display state
        if 'show_risk_summary' not in st.session_state:
            st.session_state.show_risk_summary = False
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            button_text = "🎯 View Risk Summary" if not st.session_state.show_risk_summary else "📋 Back to Clauses"
            if st.button(button_text, key="toggle_risk_summary", type="primary", use_container_width=True):
                st.session_state.show_risk_summary = not st.session_state.show_risk_summary
                st.rerun()
        
        # Show risk summary if toggled on
        if st.session_state.show_risk_summary:
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            st.header("🎯 Risk Summary Dashboard")
            
            # Get current document data
            if (st.session_state.current_document and 
                st.session_state.current_document in st.session_state.processed_documents):
                doc_data = st.session_state.processed_documents[st.session_state.current_document]
                risk_summary = doc_data.get('risk_summary', {})
                self.display_risk_summary(risk_summary)

    
    def render_voice_chat_widget(self):
        """Render the Omnidimension AI voice chat widget with modern design."""
        import streamlit.components.v1 as components
        
        # Professional voice chat section
        st.markdown(create_voice_chat_section(), unsafe_allow_html=True)
        
        # Enhanced widget container with modern styling
        widget_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>SignSafe Document Assistant</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
                
                body {
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                    font-family: 'Inter', sans-serif;
                    min-height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .widget-container {
                    width: 100%;
                    max-width: 600px;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    padding: 2rem;
                    text-align: center;
                    border: 1px solid #e2e8f0;
                    position: relative;
                    overflow: hidden;
                }
                
                .widget-container::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #2563eb, #3b82f6, #6366f1);
                }
                
                .assistant-status {
                    color: #2563eb;
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                }
                
                .assistant-subtitle {
                    color: #64748b;
                    font-size: 0.95rem;
                    margin-bottom: 1.5rem;
                    line-height: 1.5;
                }
                
                .features-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                    gap: 1rem;
                    margin-top: 1.5rem;
                }
                
                .feature-item {
                    background: #f1f5f9;
                    padding: 0.75rem;
                    border-radius: 8px;
                    font-size: 0.85rem;
                    color: #475569;
                    font-weight: 500;
                    border: 1px solid #e2e8f0;
                    transition: all 0.2s ease;
                }
                
                .feature-item:hover {
                    background: #dbeafe;
                    border-color: #2563eb;
                    color: #2563eb;
                    transform: translateY(-1px);
                }
                
                .chat-indicator {
                    background: linear-gradient(135deg, #10b981, #059669);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 500;
                    display: inline-block;
                    margin-top: 1rem;
                    animation: pulse 2s infinite;
                }
                
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.7; }
                    100% { opacity: 1; }
                }
            </style>
        </head>
        <body>
            <div class="widget-container">
                <div class="assistant-status">
                    🤖 AI Document Assistant Active
                </div>
                <div class="assistant-subtitle">
                    Your intelligent legal document companion is ready to answer questions, explain clauses, and provide risk analysis
                </div>
                
                <div class="features-grid">
                    <div class="feature-item">
                        🎤 Voice Chat
                    </div>
                    <div class="feature-item">
                        💬 Text Questions
                    </div>
                    <div class="feature-item">
                        📄 Clause Analysis
                    </div>
                    <div class="feature-item">
                        🔍 Risk Assessment
                    </div>
                </div>
                
                <div class="chat-indicator">
                    ● Chat widget will appear in bottom-right corner
                </div>
                
                <script id="omnidimension-web-widget" async src="https://backend.omnidim.io/web_widget.js?secret_key=b45069849cfaedd6106c15a0314c973b"></script>
            </div>
        </body>
        </html>
        """
        
        components.html(widget_html, height=300)
    
    def display_risk_summary(self, risk_summary: Dict[str, Any]):
        """Display risk summary dashboard."""
        # Overall risk metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clauses", risk_summary.get('total_clauses', 0))
        
        with col2:
            high_risk = risk_summary.get('high_risk_count', 0)
            st.metric("High Risk", high_risk)
        
        with col3:
            medium_risk = risk_summary.get('medium_risk_count', 0)
            st.metric("Medium Risk", medium_risk)
        
        with col4:
            low_risk = risk_summary.get('low_risk_count', 0)
            st.metric("Low Risk", low_risk)
        
        # Overall assessment
        overall_risk = risk_summary.get('overall_risk', 'unknown')
        
        if overall_risk == 'high':
            st.error("🔴 **HIGH RISK DOCUMENT**")
            st.write("This document contains significant risks that require careful review.")
        elif overall_risk == 'medium':
            st.warning("🟡 **MEDIUM RISK DOCUMENT**")
            st.write("This document contains some risks that should be reviewed.")
        else:
            st.success("🟢 **LOW RISK DOCUMENT**")
            st.write("This document appears to have minimal risks.")
        
        # Top risk factors
        top_risks = risk_summary.get('top_risk_factors', [])
        if top_risks:
            st.subheader("🎯 Top Risk Factors")
            for i, risk in enumerate(top_risks, 1):
                st.write(f"{i}. {risk}")
        
        # Critical warnings
        warnings = risk_summary.get('critical_warnings', [])
        if warnings:
            st.subheader("⚠️ Critical Warnings")
            for warning in warnings:
                st.warning(warning)
        
        # Overall recommendation
        recommendation = risk_summary.get('recommendation', '')
        if recommendation:
            st.subheader("💡 Recommendation")
            st.info(recommendation)
        
        # Risk distribution chart
        if risk_summary.get('total_clauses', 0) > 0:
            st.subheader("📊 Risk Distribution")
            
            risk_data = {
                'High Risk': risk_summary.get('high_risk_count', 0),
                'Medium Risk': risk_summary.get('medium_risk_count', 0),
                'Low Risk': risk_summary.get('low_risk_count', 0)
            }
            
            st.bar_chart(risk_data)
        
        # Add voice chat widget at the bottom of risk summary
        self.render_voice_chat_widget()
