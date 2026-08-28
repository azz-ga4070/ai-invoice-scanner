import streamlit as st

from invoice_parser import extract_text, extract_invoice_data


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Invoice Scanner",
    page_icon="🧾",
    layout="wide",
)


# ---------------------------------------------------------
# Style simple
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f7f7;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #666666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .result-box {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e5e5;
        margin-bottom: 15px;
    }

    .result-label {
        color: #777777;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .result-value {
        font-size: 20px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🧾 AI Invoice Scanner</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Automatically extract information from invoices using OCR.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your invoice",
    type=["png", "jpg", "jpeg"],
)


# ---------------------------------------------------------
# Processing
# ---------------------------------------------------------

if uploaded_file is not None:

    st.divider()

    # -----------------------------------------------------
    # Invoice + button
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📄 Invoice")

        st.image(
            uploaded_file,
            use_container_width=True,
        )

    with col2:

        st.subheader("🔍 Analysis")

        st.write(
            "Click the button to extract the invoice information."
        )

        if st.button(
            "Extract Data",
            use_container_width=True,
        ):

            with st.spinner("Processing invoice..."):

                text = extract_text(
                    uploaded_file
                )

                invoice_data = extract_invoice_data(
                    text
                )

            # Save results
            st.session_state["invoice_data"] = invoice_data
            st.session_state["ocr_text"] = text


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

if "invoice_data" in st.session_state:

    invoice_data = st.session_state["invoice_data"]

    st.divider()

    st.success("Invoice processed successfully!")

    # -----------------------------------------------------
    # Invoice details
    # -----------------------------------------------------

    st.subheader("📋 Invoice Details")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="result-box">
                <div class="result-label">
                    Invoice Number
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
                <div class="result-value">
                    {invoice_data.get(
                        "invoice_number",
                        "Not detected"
                    )}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="result-box">
                <div class="result-label">
                    Date
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
                <div class="result-value">
                    {invoice_data.get(
                        "date",
                        "Not detected"
                    )}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="result-box">
                <div class="result-label">
                    Supplier
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
                <div class="result-value">
                    {invoice_data.get(
                        "supplier",
                        "Not detected"
                    )}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # -----------------------------------------------------
    # Financial summary
    # -----------------------------------------------------

    st.subheader("💰 Financial Summary")

    subtotal = invoice_data.get("subtotal")
    vat = invoice_data.get("vat")
    total_ttc = invoice_data.get("total_ttc")

    col1, col2, col3 = st.columns(3)

    with col1:

        if subtotal is not None:

            st.metric(
                "Subtotal",
                f"{subtotal:,.2f} DT",
            )

        else:

            st.metric(
                "Subtotal",
                "Not detected",
            )

    with col2:

        if vat is not None:

            st.metric(
                "VAT",
                f"{vat:,.2f} DT",
            )

        else:

            st.metric(
                "VAT",
                "Not detected",
            )

    with col3:

        if total_ttc is not None:

            st.metric(
                "Total TTC",
                f"{total_ttc:,.2f} DT",
            )

        else:

            st.metric(
                "Total TTC",
                "Not detected",
            )


    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    if (
        subtotal is not None
        and vat is not None
        and total_ttc is not None
    ):

        st.subheader("🔎 Amount Validation")

        expected_total = subtotal + vat

        difference = abs(
            expected_total - total_ttc
        )

        amounts_consistent = invoice_data.get(
            "amounts_consistent",
            False,
        )

        if amounts_consistent:

            st.success(
                "✅ Amounts are consistent."
            )

            st.write(
                f"Expected Total: "
                f"**{expected_total:,.2f} DT**"
            )

            st.write(
                f"Detected Total: "
                f"**{total_ttc:,.2f} DT**"
            )

        else:

            st.warning(
                "⚠️ Amount inconsistency detected."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Expected Total",
                    f"{expected_total:,.2f} DT",
                )

            with col2:

                st.metric(
                    "Detected Total",
                    f"{total_ttc:,.2f} DT",
                )

            with col3:

                st.metric(
                    "Difference",
                    f"{difference:,.2f} DT",
                )


    # -----------------------------------------------------
    # OCR text
    # -----------------------------------------------------

    st.subheader("📝 OCR Text")

    with st.expander("Show extracted text"):

        st.text(
            st.session_state.get(
                "ocr_text",
                "",
            )
        )