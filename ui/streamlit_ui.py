import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="wide")

    # ✅ Custom Fonts + Advanced Styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(145deg, #e0eafc, #cfdef3);
        color: #2c3e50;
    }

    .hero {
        background: radial-gradient(circle at top left, #667eea, #764ba2);
        color: white;
        padding: 5rem 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }

    .hero h1 {
        font-size: 3.5rem;
        margin-bottom: 0.2em;
    }

    .hero p {
        font-size: 1.25rem;
        font-weight: 300;
        opacity: 0.9;
    }

    .upload-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        margin-top: -50px;
        margin-bottom: 40px;
    }

    .clause-block {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(8px);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    .clause-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #34495e;
    }

    .risk-tag {
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }

    .risk-high {
        background-color: #ffdddd;
        color: #c0392b;
    }

    .risk-medium {
        background-color: #fff3cd;
        color: #b36b00;
    }

    .risk-low {
        background-color: #d4edda;
        color: #155724;
    }

    .footer {
        text-align: center;
        font-size: 13px;
        margin-top: 50px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

    # 🌈 Hero Section
    st.markdown("""
    <div class="hero">
        <h1>📜 SignSafe</h1>
        <p>Your Legal Documents, Explained Clearly — With a Voice</p>
    </div>
    """, unsafe_allow_html=True)

    # ⬆ Upload Panel
    st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
    st.subheader("📂 Upload a Contract or Document")
    uploaded_file = st.file_uploader("Supported formats: PDF, DOCX, JPG, PNG", type=["pdf", "docx", "jpg", "jpeg", "png"])
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        st.success("✅ File uploaded! Here's what we found:")
        clauses = [
            {
                "original": "The lessee shall indemnify the lessor for any damages...",
                "simple": "If anything breaks while you're there, you have to pay.",
                "risk": "high"
            },
            {
                "original": "Auto-renewal clause activates every 12 months unless stopped...",
                "simple": "This keeps going unless you cancel it yourself.",
                "risk": "medium"
            },
            {
                "original": "Jurisdiction is under the court of Maharashtra...",
                "simple": "Any problems will go to court in Maharashtra.",
                "risk": "low"
            }
        ]

        # 📄 Clause Panels
        for i, clause in enumerate(clauses, 1):
            st.markdown("<div class='clause-block'>", unsafe_allow_html=True)
            st.markdown(f"<div class='clause-title'>📜 Clause {i}</div>", unsafe_allow_html=True)
            st.markdown(f"**Original Text:** {clause['original']}")
            st.markdown(f"**Simple Explanation:** {clause['simple']}")

            risk_class = {
                "high": "risk-high",
                "medium": "risk-medium",
                "low": "risk-low"
            }.get(clause["risk"], "risk-low")

            label = {
                "high": "🔴 High Risk",
                "medium": "🟡 Medium Risk",
                "low": "🟢 Low Risk"
            }.get(clause["risk"])

            st.markdown(f"<div class='risk-tag {risk_class}'>{label}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>Made by Team SignSafe • Microsoft Code Cubicle 4.0</div>", unsafe_allow_html=True)
