import pytesseract
from PIL import Image
import re


def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="fra")
    return text


def extract_invoice_data(text):
    data = {}

    # Numéro de facture
    match = re.search(r"N[°º]\s*FACTURE\s*:\s*([A-Z0-9-]+)", text, re.IGNORECASE)

    if match:
        data["invoice_number"] = match.group(1)

    # Date de facture
    match = re.search(r"DATE\s*:\s*(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)

    if match:
        data["date"] = match.group(1)

     # Fournisseur
    match = re.search(
        r"^(.*?)\s*\n\s*(SARL|SA|SUARL|SAS)\s*$",
        text,
        re.IGNORECASE | re.MULTILINE
    )

    if match:
        data["supplier"] = f"{match.group(1).strip()} {match.group(2).strip()}"
        # Total TTC
    match = re.search(
        r"TOTAL\s*TTC.*?([\d\s]+,\d{3})\s*DT",
        text,
        re.IGNORECASE
    )

    if match:
        amount = match.group(1)
        amount = amount.replace(" ", "").replace(",", ".")
        data["total_ttc"] = float(amount)
     # TVA
    match = re.search(
        r"TVA\s*\(\s*\d+\s*%\s*\)\s+([\d\s]+,\d{3})",
        text,
        re.IGNORECASE
    )

    if match:
        amount = match.group(1)
        amount = amount.replace(" ", "").replace(",", ".")
        data["vat"] = float(amount)
        # Sous-total
    match = re.search(
        r"SOUS[-\s]?TOTAL\s+([\d\s]+,\d{3})",
        text,
        re.IGNORECASE
    )

    if match:
        amount = match.group(1)
        amount = amount.replace(" ", "").replace(",", ".")
        data["subtotal"] = float(amount)
    return data
    

    if match:
        amount = match.group(1)
        amount = amount.replace(" ", "").replace(",", ".")
        data["total_ttc"] = float(amount)

text = extract_text("invoices/invoice_test.png")

invoice_data = extract_invoice_data(text)

print(invoice_data)