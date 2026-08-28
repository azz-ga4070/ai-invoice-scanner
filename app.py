import streamlit as st

from invoice_parser import extract_text, extract_invoice_data


st.set_page_config(
    page_title="AI Invoice Scanner",
    page_icon="🧾",
    layout="wide",
)

st.title("🧾 AI Invoice Scanner")
st.write("Automatically extract key information from invoices using OCR.")

uploaded_file = st.file_uploader(
    "Upload an invoice",
    type=["png", "jpg", "jpeg"],
)


if uploaded_file is not None:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Invoice")
        st.image(uploaded_file, use_container_width=True)

    with col2:
        st.subheader("Extracted Information")

        if st.button("🔍 Extract Data", use_container_width=True):

            with st.spinner("Processing invoice..."):

                text = extract_text(uploaded_file)
                invoice_data = extract_invoice_data(text)

            if invoice_data:

                st.success("Invoice processed successfully!")

                st.write("### Invoice details")

                invoice_col1, invoice_col2 = st.columns(2)

                with invoice_col1:
                    st.write("**Invoice Number**")
                    st.info(
                        invoice_data.get(
                            "invoice_number",
                            "Not detected"
                        )
                    )

                    st.write("**Date**")
                    st.info(
                        invoice_data.get(
                            "date",
                            "Not detected"
                        )
                    )

                with invoice_col2:
                    st.write("**Supplier**")
                    st.info(
                        invoice_data.get(
                            "supplier",
                            "Not detected"
                        )
                    )

                st.write("### Financial Summary")

                financial_col1, financial_col2, financial_col3 = st.columns(3)

                with financial_col1:
                    st.metric(
                        "Subtotal",
                        f"{invoice_data.get('subtotal', 0):,.2f} DT",
                    )

                with financial_col2:
                    st.metric(
                        "VAT",
                        f"{invoice_data.get('vat', 0):,.2f} DT",
                    )

                with financial_col3:
                    st.metric(
                        "Total TTC",
                        f"{invoice_data.get('total_ttc', 0):,.2f} DT",
                    )

            else:
                st.warning("No invoice information could be detected.")