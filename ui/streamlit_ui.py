# ui/streamlit_ui.py

import streamlit as st
from pathlib import Path

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="centered")
    st.title("📜 SignSafe")
    st.markdown("**Understand any legal document – even if you can't read legal language.**")

    st.header("📂 Upload a Document")
    uploaded_file = st.file_uploader("Choose a PDF or image", type=["pdf", "png", "jpg", "jpeg", "docx"])

    # Placeholder for now – simulate output
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.subheader("🧠 Here's what we found:")

        sample_clauses = [
            {
                "original": "The lessee shall indemnify the lessor for any damages...",
                "simple": "If anything gets damaged while you're living there, you have to pay for it.",
                "risk": "high",
                "audio_path": "assets/audio/clause1.mp3"
            },
            {
                "original": "This agreement shall renew automatically unless terminated...",
                "simple": "It will auto-renew unless you cancel it yourself.",
                "risk": "medium",
                "audio_path": "assets/audio/clause2.mp3"
            },
            {
                "original": "This contract is governed by the laws of another state...",
                "simple": "If there’s a problem, it’ll be settled in a different state’s court.",
                "risk": "medium",
                "audio_path": "assets/audio/clause3.mp3"
            }
        ]

        risk_color = {
            "high": "🔴 High Risk",
            "medium": "🟡 Medium Risk",
            "low": "🟢 Low Risk"
        }

        for i, clause in enumerate(sample_clauses, start=1):
            st.markdown(f"### 📜 Clause {i}")
            st.markdown(f"**Original:** {clause['original']}")
            st.markdown(f"**In Simple Words:** {clause['simple']}")
            st.markdown(f"**Risk Level:** {risk_color[clause['risk']]}")
            st.audio(clause['audio_path'], format='audio/mp3')
            st.markdown("---")
