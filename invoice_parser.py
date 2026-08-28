import re

import pytesseract
from PIL import Image


def extract_text(image_source):
    """Extract text from an invoice image using Tesseract OCR."""
    image = Image.open(image_source)
    text = pytesseract.image_to_string(image, lang="fra")
    return text

def parse_amount(amount):
    """Convert a French-formatted amount into a float."""
    amount = amount.replace(" ", "").replace(",", ".")
    return float(amount)


def extract_invoice_data(text):
    """Extract structured information from OCR text."""
    data = {}

    # Invoice number
    match = re.search(
        r"N[°º]\s*FACTURE\s*:\s*([A-Z0-9-]+)",
        text,
        re.IGNORECASE,
    )

    if match:
        data["invoice_number"] = match.group(1)

    # Invoice date
    match = re.search(
        r"DATE\s*:\s*(\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE,
    )

    if match:
        data["date"] = match.group(1)

    # Supplier
    match = re.search(
        r"^(.*?)\s*\n\s*(SARL|SA|SUARL|SAS)\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    )

    if match:
        data["supplier"] = (
            f"{match.group(1).strip()} {match.group(2).strip()}"
        )

    # Total TTC
    match = re.search(
        r"TOTAL\s*TTC.*?([\d\s]+,\d{3})\s*DT",
        text,
        re.IGNORECASE,
    )

    if match:
        data["total_ttc"] = parse_amount(match.group(1))

    # VAT
    match = re.search(
        r"TVA\s*\(\s*\d+\s*%\s*\)\s+([\d\s]+,\d{3})",
        text,
        re.IGNORECASE,
    )

    if match:
        data["vat"] = parse_amount(match.group(1))

    # Subtotal
    match = re.search(
        r"SOUS[-\s]?TOTAL\s+([\d\s]+,\d{3})",
        text,
        re.IGNORECASE,
    )

    if match:
        data["subtotal"] = parse_amount(match.group(1))
    # Validate invoice amounts
    if all(
        key in data
        for key in ["subtotal", "vat", "total_ttc"]
    ):
        expected_total = data["subtotal"] + data["vat"]

        data["amounts_consistent"] = (
            abs(expected_total - data["total_ttc"]) < 0.01
        )
    return data


def main():
    """Run the invoice parser on a test invoice."""
    image_path = "invoices/invoice_test.png"

    text = extract_text(image_path)
    invoice_data = extract_invoice_data(text)

    print(invoice_data)


if __name__ == "__main__":
    main()