import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="wide")

    # 🧠 Theme Toggle
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    mode = st.toggle("🌗 Toggle Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = mode

    # 🎨 CSS Styles (Dark + Light)
    if mode:  # Dark Mode
        st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #1e1e1e;
            color: #f0f0f0;
            font-family: 'Poppins', sans-serif;
        }
        .hero {
            background-color: #121212;
            color: #ffffff;
            padding: 3rem 2rem;
            border-radius: 0 0 20px 20px;
            text-align: center;
        }
        .clause {
            background-color: #2a2a2a;
            border-left: 5px solid #5dade2;
            color: #f0f0f0;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
        }
        .risk-label {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            margin-top: 10px;
        }
        .risk-high { background: #e74c3c33; color: #e74c3c; }
        .risk-medium { background: #f39c1233; color: #f39c12; }
        .risk-low { background: #27ae6033; color: #27ae60; }
        .footer {
            text-align: center;
            font-size: 13px;
            color: #999;
            margin-top: 50px;
        }
        </style>
        """, unsafe_allow_html=True)

    else:  # Light Mode
        st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #f5f7fa;
            color: #222;
            font-family: 'Poppins', sans-serif;
        }
        .hero {
            background-color: #2c3e50;
            color: white;
            padding: 3rem 2rem;
            border-radius: 0 0 20px 20px;
            text-align: center;
        }
        .clause {
            background-color: #ffffff;
            border-left: 5px solid #5dade2;
            color: #222222 !important;
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
        .risk-high { background: #f8d7da; color: #a94442; }
        .risk-medium { background: #fff3cd; color: #856404; }
        .risk-low { background: #d4edda; color: #155724; }
        .footer {
            text-align: center;
            font-size: 13px;
            color: #777;
            margin-top: 50px;
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

    # 📤 Upload Section (cleaned, no box)
    st.markdown("### 📂 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF, Word, or image file", type=["pdf", "docx", "jpg", "jpeg", "png"])

    # 🧠 Sample Output
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.markdown("### 🧠 Here's what we found:")

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
