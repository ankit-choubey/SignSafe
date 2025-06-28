import streamlit as st
from pathlib import Path

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="centered")

    # 💡 Global Styles
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background: #f4f7fa;
        }
        .main-title {
            text-align: center;
            font-size: 48px;
            margin-bottom: 0px;
            color: #2c3e50;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            margin-top: 0px;
            color: #7f8c8d;
        }
        .upload-box {
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin-top: 30px;
        }
        .clause-block {
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        }
        .risk {
            padding: 5px 10px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: bold;
            display: inline-block;
        }
        .risk-high { background-color: #ffe0e0; color: #c0392b; }
        .risk-medium { background-color: #fff4d6; color: #b36b00; }
        .risk-low { background-color: #d6ffe6; color: #16a085; }
        .footer {
            text-align: center;
            font-size: 13px;
            margin-top: 50px;
            color: #95a5a6;
        }
    </style>
    """, unsafe_allow_html=True)

    # 🎉 HEADER
    st.markdown("<h1 class='main-title'>📜 SignSafe</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Legal documents, explained simply and clearly</p>", unsafe_allow_html=True)

    # 📂 UPLOAD SECTION
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    st.subheader("📂 Upload your contract")
    uploaded_file = st.file_uploader(
        "Supported formats: PDF, DOCX, JPG, PNG",
        type=["pdf", "docx", "jpg", "jpeg", "png"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        st.success("✅ File uploaded! Processing now...")

        # 💡 Placeholder for clause output
        sample_clauses = [
            {
                "original": "The lessee shall indemnify the lessor for any damages...",
                "simple": "You’ll have to pay for anything broken – even if it's not your fault.",
                "risk": "high"
            },
            {
                "original": "This agreement will auto-renew unless terminated...",
                "simple": "This will keep going unless you cancel it yourself.",
                "risk": "medium"
            },
            {
                "original": "All disputes shall be resolved under laws of State X...",
                "simple": "If something goes wrong, you’ll deal with it in State X’s courts.",
                "risk": "medium"
            }
        ]

        st.markdown("## 🧠 AI Breakdown", unsafe_allow_html=True)
        for i, clause in enumerate(sample_clauses, 1):
            st.markdown("<div class='clause-block'>", unsafe_allow_html=True)
            st.markdown(f"### Clause {i}")
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

            st.markdown(
                f"<div class='risk {risk_class}'>{risk_label}</div>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # 💬 Voice Q&A Placeholder
        st.markdown("### ❓ Ask a Question")
        user_q = st.text_input("Type your question here...")
        if user_q:
            st.info("🧠 Feature coming soon: Ask SignSafe about any clause!")

    # 🔚 Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>🔒 Built with care by Team SignSafe • Code Cubicle 4.0</div>", unsafe_allow_html=True)
