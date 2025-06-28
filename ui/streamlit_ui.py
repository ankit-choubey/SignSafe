import streamlit as st

def launch_ui():
    st.set_page_config(page_title="SignSafe", layout="centered")
    st.markdown(
        """
        <h1 style='text-align: center;'>📜 SignSafe</h1>
        <p style='text-align: center; font-size: 18px;'>
        <b>Understand any legal document – even if you can't read legal language.</b>
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.subheader("📂 Upload a Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or image",
            type=["pdf", "png", "jpg", "jpeg", "docx"],
            label_visibility="collapsed"
        )

    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.subheader("🧠 Here's what we found:")
        st.markdown(" ")

        # Replace later with real backend
        sample_clauses = [
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

        # Display each clause inside a nice card
        for i, clause in enumerate(sample_clauses, start=1):
            with st.container():
                st.markdown(f"""
                    <div style="
                        background-color: #f9f9f9;
                        border-radius: 12px;
                        padding: 20px;
                        margin-bottom: 20px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                    ">
                        <h4>📜 Clause {i}</h4>
                        <p><b>Original:</b> {clause['original']}</p>
                        <p><b>In Simple Words:</b> {clause['simple']}</p>
                """, unsafe_allow_html=True)

                if clause["risk"] == "high":
                    st.markdown("<p style='color:red; font-weight:bold;'>🔴 High Risk</p>", unsafe_allow_html=True)
                elif clause["risk"] == "medium":
                    st.markdown("<p style='color:orange; font-weight:bold;'>🟡 Medium Risk</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color:green; font-weight:bold;'>🟢 Low Risk</p>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:13px; color:gray;'>🔒 SignSafe is built for Microsoft Code Cubicle 4.0 • Team SignSafe</p>",
        unsafe_allow_html=True
    )
