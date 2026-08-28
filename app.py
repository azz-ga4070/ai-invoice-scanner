
import streamlit as st
import pandas as pd

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
# Style
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
    "Automatically extract and validate information from invoices using OCR."
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload your invoices",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)


# ---------------------------------------------------------
# Process invoices
# ---------------------------------------------------------

if uploaded_files:

    st.divider()

    st.write(
        f"📄 **{len(uploaded_files)} invoice(s) selected**"
    )

    if st.button(
        "🔍 Process Invoices",
        use_container_width=True,
    ):

        results = []

        progress_bar = st.progress(0)

        for index, uploaded_file in enumerate(uploaded_files):

            try:

                with st.spinner(
                    f"Processing {uploaded_file.name}..."
                ):

                    text = extract_text(uploaded_file)

                    invoice_data = extract_invoice_data(text)

                results.append(
                    {
                        "filename": uploaded_file.name,
                        "data": invoice_data,
                        "ocr_text": text,
                        "error": None,
                    }
                )

            except Exception as error:

                results.append(
                    {
                        "filename": uploaded_file.name,
                        "data": {},
                        "ocr_text": "",
                        "error": str(error),
                    }
                )

            progress_bar.progress(
                (index + 1) / len(uploaded_files)
            )

        st.session_state["invoice_results"] = results


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

if "invoice_results" in st.session_state:

    results = st.session_state["invoice_results"]

    st.divider()

    st.success(
        f"✅ {len(results)} invoice(s) processed successfully!"
    )


    # -----------------------------------------------------
    # Build dataframe
    # -----------------------------------------------------

    rows = []

    for result in results:

        data = result["data"]

        subtotal = data.get("subtotal")
        vat = data.get("vat")
        total_ttc = data.get("total_ttc")

        amounts_consistent = data.get(
            "amounts_consistent"
        )

        if amounts_consistent is True:
            status = "✅ Valid"

        elif amounts_consistent is False:
            status = "⚠️ Inconsistent"

        else:
            status = "❓ Incomplete"

        rows.append(
            {
                "Invoice": data.get(
                    "invoice_number",
                    "Not detected",
                ),
                "Date": data.get(
                    "date",
                    "Not detected",
                ),
                "Supplier": data.get(
                    "supplier",
                    "Not detected",
                ),
                "Subtotal": subtotal,
                "VAT": vat,
                "Total TTC": total_ttc,
                "Status": status,
            }
        )


    df = pd.DataFrame(rows)


    # -----------------------------------------------------
    # Global statistics
    # -----------------------------------------------------

    st.subheader("📊 Global Summary")

    total_invoices = len(df)

    valid_count = sum(
        df["Status"] == "✅ Valid"
    )

    inconsistent_count = sum(
        df["Status"] == "⚠️ Inconsistent"
    )

    incomplete_count = sum(
        df["Status"] == "❓ Incomplete"
    )

    total_subtotal = (
        df["Subtotal"]
        .dropna()
        .sum()
    )

    total_vat = (
        df["VAT"]
        .dropna()
        .sum()
    )

    total_ttc = (
        df["Total TTC"]
        .dropna()
        .sum()
    )


    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Invoices",
            total_invoices,
        )

    with col2:

        st.metric(
            "Valid",
            valid_count,
        )

    with col3:

        st.metric(
            "Inconsistent",
            inconsistent_count,
        )

    with col4:

        st.metric(
            "Incomplete",
            incomplete_count,
        )


    st.write("### 💰 Financial Totals")


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Subtotal",
            f"{total_subtotal:,.2f} DT",
        )

    with col2:

        st.metric(
            "Total VAT",
            f"{total_vat:,.2f} DT",
        )

    with col3:

        st.metric(
            "Total TTC",
            f"{total_ttc:,.2f} DT",
        )


    # -----------------------------------------------------
    # Global table
    # -----------------------------------------------------

    st.write("### 📋 All Invoices")

    display_df = df.copy()

    display_df["Subtotal"] = display_df[
        "Subtotal"
    ].apply(
        lambda x:
        f"{x:,.2f} DT"
        if pd.notna(x)
        else "Not detected"
    )

    display_df["VAT"] = display_df[
        "VAT"
    ].apply(
        lambda x:
        f"{x:,.2f} DT"
        if pd.notna(x)
        else "Not detected"
    )

    display_df["Total TTC"] = display_df[
        "Total TTC"
    ].apply(
        lambda x:
        f"{x:,.2f} DT"
        if pd.notna(x)
        else "Not detected"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


    # -----------------------------------------------------
    # CSV Export
    # -----------------------------------------------------

    st.write("### 📥 Export Results")

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name="invoice_results.csv",
        mime="text/csv",
        use_container_width=True,
    )


    # -----------------------------------------------------
    # Individual invoices
    # -----------------------------------------------------

    st.write("### 📄 Invoice Details")

    for index, result in enumerate(results):

        filename = result["filename"]
        invoice_data = result["data"]
        error = result["error"]

        with st.expander(
            f"Invoice {index + 1} — {filename}",
            expanded=False,
        ):

            if error:

                st.error(
                    f"Unable to process invoice: {error}"
                )

                continue


            # ---------------------------------------------
            # Invoice information
            # ---------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write("**Invoice Number**")

                st.info(
                    invoice_data.get(
                        "invoice_number",
                        "Not detected",
                    )
                )

            with col2:

                st.write("**Date**")

                st.info(
                    invoice_data.get(
                        "date",
                        "Not detected",
                    )
                )

            with col3:

                st.write("**Supplier**")

                st.info(
                    invoice_data.get(
                        "supplier",
                        "Not detected",
                    )
                )


            # ---------------------------------------------
            # Financial summary
            # ---------------------------------------------

            st.write("### 💰 Financial Summary")

            subtotal = invoice_data.get("subtotal")
            vat = invoice_data.get("vat")
            total_ttc = invoice_data.get("total_ttc")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Subtotal",
                    f"{subtotal:,.2f} DT"
                    if subtotal is not None
                    else "Not detected",
                )

            with col2:

                st.metric(
                    "VAT",
                    f"{vat:,.2f} DT"
                    if vat is not None
                    else "Not detected",
                )

            with col3:

                st.metric(
                    "Total TTC",
                    f"{total_ttc:,.2f} DT"
                    if total_ttc is not None
                    else "Not detected",
                )


            # ---------------------------------------------
            # Validation
            # ---------------------------------------------

            if (
                subtotal is not None
                and vat is not None
                and total_ttc is not None
            ):

                expected_total = (
                    subtotal + vat
                )

                difference = abs(
                    expected_total - total_ttc
                )

                if invoice_data.get(
                    "amounts_consistent",
                    False,
                ):

                    st.success(
                        "✅ Amounts are consistent."
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


            # ---------------------------------------------
            # OCR
            # ---------------------------------------------

            with st.expander("📝 Show OCR text"):

                st.text(
                    result["ocr_text"]
                )
