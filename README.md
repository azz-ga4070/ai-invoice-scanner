# AI Invoice Scanner
An intelligent invoice processing application built with Python and Streamlit.
The application uses OCR (Optical Character Recognition) to extract structured information from invoice images and automatically validate financial amounts.
## Overview
AI Invoice Scanner is a Python application designed to automate the extraction of important information from invoices.
The user uploads an invoice image, and the system processes the document through an OCR pipeline to extract key information such as:
Invoice number
Invoice date
Supplier
Subtotal
VAT
Total TTC
The application also performs a basic financial consistency check by comparing:
Subtotal + VAT
       ↓
Expected Total
       ↓
Compared with
       ↓
Detected Total TTC
This allows the system to identify potential inconsistencies in the extracted amounts.
## Features
- Upload invoice images
- OCR text extraction
- Automatic invoice number extraction
- Date extraction
- Supplier extraction
- Subtotal extraction
- VAT extraction
- Total TTC extraction
- Financial consistency validation
- Detection of amount discrepancies
- Interactive Streamlit web interface
- Display of raw OCR text
## Technologies
Python :main programming language
Tesseract OCR :extract text from invoice images
pytesseract :python interface for tesseract
Pillow :image processing and loading 
Regex :pattern-based information extraction
Streamlit :web application interface
## Architecture
           Invoice Image 
                 │ 
                 ▼ 
          ┌──────────────┐ 
          │   Pillow     │ 
          │ Image Loading│ 
          └──────┬───────┘ 
                 │
                 ▼    
          ┌──────────────┐   
          │  Tesseract   │
          │     OCR      │
          └──────┬───────┘ 
                 ▼ 
          ┌──────────────┐
          │     Regex    │ 
          │     Parser   │ 
          └──────┬───────┘ 
                 │ 
                 ▼           
      Structured Invoice Data             
                 │ 
                 ▼  
          ┌──────────────┐
          │  Validation  │ 
          │ Subtotal+VAT │
          │       vs TTC │ 
          └──────┬───────┘ 
                 │
                 ▼ 
           Streamlit Interface

           1. Upload
The user uploads an invoice in PNG, JPG or JPEG format.
2. OCR
Tesseract OCR analyzes the image and converts the visible text into machine-readable text.
3. Information Extraction
The extracted text is analyzed using Python regular expressions to identify specific invoice fields.
Example:
Invoice Number → INV-2026-0042
Date           → 28/08/2026
Supplier       → TECH SOLUTIONS SARL
Subtotal       → 2690.00 DT
VAT            → 511.10 DT
Total TTC      → 2975.10 DT
4. Financial Validation
The system calculates:
Expected Total = Subtotal + VAT
and compares the result with the detected TTC amount.
If the values differ, the application displays a warning and shows the detected difference.

## Installation
Clone the repository
git clone https://github.com/azz-ga4070/ai-invoice-scanner.git
cd ai-invoice-scanner
Create a virtual environment
python -m venv .venv
Activate the environment
macOS / Linux:
source .venv/bin/activate
Install Python dependencies
pip install -r requirements.txt
Install Tesseract OCR
On macOS with Homebrew:
brew install tesseract
brew install tesseract-lang
## Usage
Start the Streamlit application:
streamlit run app.py
Then open the local URL displayed in the terminal.
Upload an invoice and click:
Extract Data
The application will display the extracted information and financial validation results.
## Example
Example invoice:
Invoice Number: INV-2026-0042
Date: 28/08/2026
Supplier: TECH SOLUTIONS SARL

Subtotal: 2690.00 DT
VAT: 511.10 DT
Total TTC: 2975.10 DT
The application extracts:
Invoice Number    INV-2026-0042
Date              28/08/2026
Supplier          TECH SOLUTIONS SARL
Subtotal          2690.00 DT
VAT               511.10 DT
Total TTC         2975.10 DT
## Project Structure
ai-invoice-scanner/
│
├── app.py
├── invoice_parser.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── invoices/
    └── invoice_test.png
app.py
Contains the Streamlit user interface and application workflow.
invoice_parser.py
Contains the OCR processing and invoice information extraction logic.
requirements.txt
Contains the Python dependencies required by the project.
invoices/
Contains invoice images used for testing.
## Limitations
The current version is a prototype and has several limitations:
The parser relies on predefined regular-expression patterns.
Different invoice layouts may require additional patterns.
OCR accuracy depends on image quality.
Handwritten invoices are not currently supported.
Complex tables may not be extracted correctly.
The application currently processes one uploaded invoice at a time.
Financial validation only checks the relationship between extracted subtotal, VAT and total TTC.
An important limitation is that an OCR or parsing error can produce an incorrect value. Therefore, the validation result should be considered an indicator rather than a definitive accounting decision.
## Future Improvements
Document Processing
Image preprocessing with OpenCV
Automatic image rotation
Noise reduction
Better OCR accuracy
Support for additional invoice formats
Extraction
More robust field detection
Support for different invoice layouts
Automatic currency detection
Product and line-item extraction
Application
Multiple invoice upload
Invoice history
Search and filtering
JSON / CSV / Excel export
Database integration
User authentication
AI / Document Understanding
A future version could integrate a document-understanding model or LLM-based extraction system to improve generalization across different invoice layouts.

