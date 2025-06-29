import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="wide")

    # Global Styles
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(to bottom right, #e0eafc, #fdfbfb);
        color: #2c3e50;
    }

    .hero {
        background: linear-gradient(to right, #667eea, #764ba2);
        color: white;
        padding: 4rem 2rem 3rem 2rem;
        text-align: center;
        border-radius: 0 0 40px 40px;
        margin-bottom: 3rem;
    }

    .hero h1 {
        font-size: 3.5rem;
        margin-bottom: 0.5em;
    }

    .hero p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }

    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        margin-top: 3rem;
        margin-bottom: 1rem;
        color: #34495e;
    }

    .clause {
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
        border-left: 6px solid #667eea;
        background: rgba(255,255,255,0.5);
        border-radius: 12px;
    }

    .risk-high {
        color: #e74c3c;
        font-weight: bold;
    }

    .risk-medium {
        color: #f39c12;
        font-weight: bold;
    }

    .risk-low {
        color: #27ae60;
        font-weight: bold;
    }

    .footer {
        text-align: center;
        font-size: 13px;
        margin-top: 50px;
        color: #7f8c8d;
    }
    </style>
    """, unsafe_allow_html=True)

    # 🌈 Hero
    st.markdown("""
    <div class="hero">
        <h1>📜 SignSafe</h1>
        <p>Understand legal documents, even if you can’t read legal jargon</p>
    </div>
    """, unsafe_allow_html=True)

    # ⬆ Upload Panel (Inline, no box)
    st.markdown("<div class='section-header'>📂 Upload Your Document</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or Image", type=["pdf", "docx", "jpg", "jpeg", "png"])

    if uploaded_file:
        st.success("✅ File uploaded! Here's what we found:")

        sample_clauses = [
            {
                "original": "The lessee shall indemnify the lessor for any damages...",
                "simple": "If something breaks while you're staying there, you must pay for it.",
                "risk": "high"
            },
            {
                "original": "This contract will renew automatically unless cancelled...",
                "simple": "It keeps renewing unless you stop it manually.",
                "risk": "medium"
            },
            {
                "original": "Any disputes must be resolved in Delhi courts only.",
                "simple": "If something goes wrong, Delhi court will handle the issue.",
                "risk": "low"
            }
        ]

        st.markdown("<div class='section-header'>🧠 Clause-by-Clause Explanation</div>", unsafe_allow_html=True)

        for i, clause in enumerate(sample_clauses, 1):
            risk_class = {
                "high": "risk-high",
                "medium": "risk-medium",
                "low": "risk-low"
            }[clause["risk"]]

            risk_label = {
                "high": "🔴 High Risk",
                "medium": "🟡 Medium Risk",
                "low": "🟢 Low Risk"
            }[clause["risk"]]

            st.markdown(f"""
            <div class="clause">
                <h4>📜 Clause {i}</h4>
                <p><strong>Original:</strong> {clause['original']}</p>
                <p><strong>Simple:</strong> {clause['simple']}</p>
                <p class="{risk_class}">{risk_label}</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>🔒 Team SignSafe • Built for Microsoft Code Cubicle 4.0</div>", unsafe_allow_html=True)
