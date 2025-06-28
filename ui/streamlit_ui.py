import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="wide")

    # ✅ Ali Abdaal–style fonts + base styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'DM Sans', sans-serif !important;
            background: linear-gradient(135deg, #fdfcfb, #e2d1c3);
        }

        .hero {
            background: linear-gradient(135deg, #c471f5, #fa71cd);
            padding: 4rem 2rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 40px;
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }

        .hero p {
            font-size: 1.3rem;
        }

        .clause-card {
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            background: white;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.06);
        }

        .risk-strip {
            padding: 8px 20px;
            font-weight: bold;
            border-radius: 8px;
            margin-top: 12px;
            text-align: center;
        }

        .risk-high {
            background-color: #ffe3e3;
            color: #d50000;
        }

        .risk-medium {
            background-color: #fff4d6;
            color: #b36b00;
        }

        .risk-low {
            background-color: #d6ffe6;
            color: #007a33;
        }

        .footer {
            text-align: center;
            font-size: 13px;
            margin-top: 50px;
            padding: 12px;
            color: #444;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🌈 Hero section (Ali-style)
    st.markdown("""
        <div class="hero">
            <h1>📜 SignSafe</h1>
            <p>Understand any legal document – even if you can't read legal language.</p>
        </div>
    """, unsafe_allow_html=True)

    # 📤 Upload UI
    st.subheader("📂 Upload a Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX, or image",
        type=["pdf", "png", "jpg", "jpeg", "docx"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.subheader("🧠 Here's what we found:")

        # 💡 Replace this with backend later
        clauses = [
            {
                "original": "The lessee shall indemnify the lessor for any damages...",
                "simple": "If anything gets damaged while you're living there, you have to pay for it.",
                "risk": "high"
            },
            {
                "original": "This agreement shall renew automatically unless terminated...",
                "simple": "It will auto-renew unless you cancel it yourself.",
                "risk": "medium"
            },
            {
                "original": "This contract is governed by the laws of another state...",
                "simple": "If there’s a problem, it’ll be settled in a different state’s court.",
                "risk": "low"
            }
        ]

        for i, clause in enumerate(clauses, start=1):
            st.markdown("<div class='clause-card'>", unsafe_allow_html=True)
            st.markdown(f"### 📜 Clause {i}")
            st.markdown(f"**Original:** {clause['original']}")
            st.markdown(f"**In Simple Words:** {clause['simple']}")

            risk_class = {
                "high": "risk-high",
                "medium": "risk-medium",
                "low": "risk-low"
            }.get(clause["risk"], "risk-low")

            risk_label = {
                "high": "🔴 High Risk",
                "medium": "🟡 Medium Risk",
                "low": "🟢 Low Risk"
            }.get(clause["risk"], "🟢 Low Risk")

            st.markdown(f"<div class='risk-strip {risk_class}'>{risk_label}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 📌 Footer
    st.markdown("<div class='footer'>🚀 Built by Team SignSafe for Microsoft Code Cubicle 4.0</div>", unsafe_allow_html=True)
