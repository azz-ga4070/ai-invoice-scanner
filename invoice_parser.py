
import re

import pytesseract
from PIL import Image


def extract_text(image_source):
    """Extract text from an invoice image using Tesseract OCR."""
    image = Image.open(image_source)

    text = pytesseract.image_to_string(
        image,
        lang="fra",
    )

    return text


def parse_amount(amount):
    """Convert a French-formatted amount into a float."""

    amount = (
        amount
        .replace(" ", "")
        .replace("\u00a0", "")
        .replace(",", ".")
    )

    return float(amount)


def extract_invoice_data(text):
    """Extract structured information from OCR text."""

    data = {}


    # -----------------------------------------------------
    # Clean OCR text
    # -----------------------------------------------------

    text = text.replace("\r", "")

    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.split("\n")
        if line.strip()
    ]


    # -----------------------------------------------------
    # Invoice number
    # -----------------------------------------------------

    match = re.search(
        r"N[°ºo]?\s*FACTURE\s*:?\s*([A-Z0-9-]+)",
        text,
        re.IGNORECASE,
    )

    if match:

        data["invoice_number"] = (
            match.group(1).strip()
        )


    # -----------------------------------------------------
    # Invoice date
    # -----------------------------------------------------

    match = re.search(
        r"DATE\s*:?\s*(\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE,
    )

    if match:

        data["date"] = (
            match.group(1).strip()
        )


    # -----------------------------------------------------
    # Supplier
    # -----------------------------------------------------

    supplier = None

    # Pattern 1:
    # COMPANY
    # SARL

    for index, line in enumerate(lines):

        if re.fullmatch(
            r"(SARL|SUARL|SAS|SA)",
            line,
            re.IGNORECASE,
        ):

            if index > 0:

                previous_line = lines[index - 1]

                if len(previous_line) <= 80:

                    supplier = (
                        f"{previous_line} {line}"
                    )

                    break


    # Pattern 2:
    # COMPANY SARL

    if supplier is None:

        for line in lines:

            match = re.search(
                r"^(.{2,70}?)\s+"
                r"(SARL|SUARL|SAS|SA)$",
                line,
                re.IGNORECASE,
            )

            if match:

                supplier = (
                    f"{match.group(1)} "
                    f"{match.group(2)}"
                )

                break


    # Pattern 3:
    # Search around FACTURE

    if supplier is None:

        for index, line in enumerate(lines):

            if re.search(
                r"FACTURE",
                line,
                re.IGNORECASE,
            ):

                candidates = lines[
                    max(0, index - 3):index
                ]

                for candidate in candidates:

                    if re.search(
                        r"(SARL|SUARL|SAS|SA)",
                        candidate,
                        re.IGNORECASE,
                    ):

                        supplier = candidate
                        break

            if supplier:
                break


    if supplier:

        supplier = re.sub(
            r"\s+",
            " ",
            supplier,
        ).strip()

        data["supplier"] = supplier


    # -----------------------------------------------------
    # Total TTC
    # -----------------------------------------------------

    match = re.search(
        r"TOTAL\s*TTC"
        r".*?"
        r"([\d\s\u00a0]+,\d{3})"
        r"\s*(?:DT|D|TND)?",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if match:

        data["total_ttc"] = parse_amount(
            match.group(1)
        )


    # -----------------------------------------------------
    # VAT
    # -----------------------------------------------------

    match = re.search(
        r"TVA"
        r"(?:\s*\(\s*\d+\s*%\s*\))?"
        r"\s*:?\s*"
        r"([\d\s\u00a0]+,\d{3})",
        text,
        re.IGNORECASE,
    )

    if match:

        data["vat"] = parse_amount(
            match.group(1)
        )


    # -----------------------------------------------------
    # Subtotal
    # -----------------------------------------------------

    match = re.search(
        r"SOUS[-\s]?TOTAL"
        r"\s*:?\s*"
        r"([\d\s\u00a0]+,\d{3})",
        text,
        re.IGNORECASE,
    )

    if match:

        data["subtotal"] = parse_amount(
            match.group(1)
        )


    # -----------------------------------------------------
    # Validate amounts
    # -----------------------------------------------------

    if all(
        key in data
        for key in [
            "subtotal",
            "vat",
            "total_ttc",
        ]
    ):

        expected_total = (
            data["subtotal"]
            + data["vat"]
        )

        difference = abs(
            expected_total
            - data["total_ttc"]
        )

        data["amounts_consistent"] = (
            difference < 0.01
        )


    return data


def main():
    """Run the invoice parser on a test invoice."""

    image_path = (
        "invoices/invoice_test.png"
    )

    text = extract_text(
        image_path
    )

    invoice_data = extract_invoice_data(
        text
    )

    print(invoice_data)


if __name__ == "__main__":

    main()
