import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="wide")

    # ✨ Custom background and CSS
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #f0f4ff, #ffffff);
        }
        .clause-card {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            transition: all 0.2s ease-in-out;
        }
        .clause-card:hover {
            transform: scale(1.01);
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        .risk-pill {
            padding: 6px 12px;
            border-radius: 50px;
            font-weight: bold;
            display: inline-block;
            font-size: 13px;
        }
        .risk-high {
            background-color: #ffe5e5;
            color: #d90000;
        }
        .risk-medium {
            background-color: #fff4e5;
            color: #b36b00;
        }
        .risk-low {
            background-color: #e6ffe6;
            color: #007a33;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: gray;
            margin-top: 50px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🧠 Hero section
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 30px 0;'>
            <h1 style='font-size: 42px;'>📜 SignSafe</h1>
            <p style='font-size: 20px;'>Understand any legal document – even if you can't read legal language.</p>
        </div>
    """, unsafe_allow_html=True)

    # 📤 Upload section
    st.subheader("📂 Upload a Document")
    uploaded_file = st.file_uploader(
        "Drag & drop a PDF, DOCX, or image file",
        type=["pdf", "png", "jpg", "jpeg", "docx"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.subheader("🧠 Here's what we found:")
        st.markdown("")

        # 🧪 Dummy data
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
                "risk": "medium"
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

            st.markdown(
                f"<div class='risk-pill {risk_class}'>{risk_label}</div>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # 🔒 Footer
    st.markdown("<div class='footer'>🔒 SignSafe is built for Microsoft Code Cubicle 4.0 • Team SignSafe</div>", unsafe_allow_html=True)
