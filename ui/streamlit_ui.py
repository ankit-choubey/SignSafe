import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="wide")

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f5f7fa;
        color: #222;
    }

    .hero {
        background-color: #2c3e50;
        color: white;
        padding: 3rem 2rem;
        border-radius: 0 0 20px 20px;
        text-align: center;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 600;
        margin: 2.5rem 0 1rem;
        color: #2c3e50;
    }

    .upload-area {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        margin-bottom: 2rem;
    }

    .clause {
        background-color: #ffffff;
        border-left: 5px solid #5dade2;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .risk-label {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 10px;
    }

    .risk-high {
        background-color: #f8d7da;
        color: #a94442;
    }

    .risk-medium {
        background-color: #fff3cd;
        color: #856404;
    }

    .risk-low {
        background-color: #d4edda;
        color: #155724;
    }

    .footer {
        text-align: center;
        font-size: 13px;
        color: #777;
        margin-top: 50px;
        padding: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # 🧠 Hero
    st.markdown("""
    <div class="hero">
        <h1>📜 SignSafe</h1>
        <p>Understand any legal document — in simple language, out loud</p>
    </div>
    """, unsafe_allow_html=True)

    # 📤 Upload Section
    st.markdown("<div class='section-title'>📂 Upload Document</div>", unsafe_allow_html=True)
    st.markdown("<div class='upload-area'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF, Word, or image file", type=["pdf", "docx", "jpg", "jpeg", "png"])
    st.markdown("</div>", unsafe_allow_html=True)

    # 🔍 Example Output
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.markdown("<div class='section-title'>🧠 Here's what we found:</div>", unsafe_allow_html=True)

        sample_clauses = [
            {
                "original": "The lessee shall indemnify the lessor for any damages...",
                "simple": "If anything breaks while you're living there, you’ll have to pay.",
                "risk": "high"
            },
            {
                "original": "This contract auto-renews unless canceled in writing.",
                "simple": "It will continue unless you cancel it yourself.",
                "risk": "medium"
            },
            {
                "original": "All disputes will be handled in Delhi courts.",
                "simple": "Any problem will go to Delhi court.",
                "risk": "low"
            }
        ]

        for i, clause in enumerate(sample_clauses, 1):
            risk_class = {
                "high": "risk-high",
                "medium": "risk-medium",
                "low": "risk-low"
            }[clause["risk"]]

            risk_label = {
                "high": "High Risk",
                "medium": "Medium Risk",
                "low": "Low Risk"
            }[clause["risk"]]

            st.markdown(f"""
            <div class='clause'>
                <h4>Clause {i}</h4>
                <p><strong>Original:</strong> {clause['original']}</p>
                <p><strong>In Simple Words:</strong> {clause['simple']}</p>
                <div class='risk-label {risk_class}'>{risk_label}</div>
            </div>
            """, unsafe_allow_html=True)

    # 🧾 Footer
    st.markdown("<div class='footer'>© 2025 Team SignSafe • Microsoft Code Cubicle 4.0</div>", unsafe_allow_html=True)
