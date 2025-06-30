"""
SignSafe - Legal Document Analyzer
Main application entry point
"""

import streamlit as st
import os
import sys
import traceback

# Try to import config, fall back to environment variables
try:
    import config
    os.environ['GEMINI_API_KEY'] = config.GEMINI_API_KEY
    os.environ['OMNIDIMENSION_API_KEY'] = config.OMNIDIMENSION_API_KEY
except ImportError:
    # Fall back to .env file if config.py doesn't exist
    from dotenv import load_dotenv
    load_dotenv()

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def main():
    """Main entry point for the SignSafe application."""
    # Set page configuration
    st.set_page_config(
        page_title="SignSafe - Legal Document Analyzer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(current_dir, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Try to import and run the main application
    try:
        from ui.streamlit_ui import SignSafeApp
        app = SignSafeApp()
        app.run()
    except ImportError as e:
        st.error(f"Import error: {e}")
        st.code(f"Python path: {sys.path}")
        st.code(f"Current directory: {current_dir}")
        st.code(f"Source directory: {src_dir}")
        st.code(f"Traceback: {traceback.format_exc()}")
    except Exception as e:
        st.error(f"Application error: {e}")
        st.code(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()