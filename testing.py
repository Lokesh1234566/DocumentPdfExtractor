"""
PDF Invoice Data Extractor

This script extracts invoice data from PDF files and converts it to JSON format.
It uses multiple PDF parsing libraries and regex patterns to extract common invoice fields.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

try:
    import pdfplumber
    import PyPDF2
    from decimal import Decimal, InvalidOperation
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install required packages: pip install pdfplumber PyPDF2")
    sys.exit(1)


class InvoiceExtractor:
    """Extract invoice data from PDF files and convert to JSON."""

    def __init__(self):
        self.invoice_patterns = {
            'invoice_number': [
                r'(?:invoice\s*(?:no|number|#)?[:\s]*)([\w\-/]+)',
                r'(?:bill\s*(?:no|number|#)?[:\s]*)([\w\-/]+)',
                r'(?:reference\s*(?:no|number|#)?[:\s]*)([\w\-/]+)',
                r'(?:doc\s*(?:no|number|#)?[:\s]*)([\w\-/]+)'
            ],
            'date': [
                r'(?:date[:\s]*)((?:\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})|(?:\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}))',
                r'(?:invoice\s*date[:\s]*)((?:\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})|(?:\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}))',
                r'(?:bill\s*date[:\s]*)((?:\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})|(?:\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}))',
                r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{2,4})'
            ],
            'total_amount': [
                r'(?:total\s*amount?[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:grand\s*total[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:amount\s*due[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:net\s*amount[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:final\s*amount[:\s])[^\d]?([\d,]+\.?\d*)'
            ],
            'tax_amount': [
                r'(?:tax\s*amount?[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:vat[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:gst[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:sales\s*tax[:\s])[^\d]?([\d,]+\.?\d*)'
            ],
            'subtotal': [
                r'(?:sub\s*total[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:subtotal[:\s])[^\d]?([\d,]+\.?\d*)',
                r'(?:net\s*subtotal[:\s])[^\d]?([\d,]+\.?\d*)'
            ],
            'vendor_name': [
                r'(?:from[:\s])(.?)(?:\n|$)',
                r'(?:vendor[:\s])(.?)(?:\n|$)',
                r'(?:supplier[:\s])(.?)(?:\n|$)',
                r'(?:company[:\s])(.?)(?:\n|$)'
            ],
            'customer_name': [
                r'(?:to[:\s])(.?)(?:\n|$)',
                r'(?:bill\s*to[:\s])(.?)(?:\n|$)',
                r'(?:customer[:\s])(.?)(?:\n|$)',
                r'(?:client[:\s])(.?)(?:\n|$)'
            ],
            'currency': [
                r'(?:currency[:\s]*)([A-Z]{3})',
                r'\b(USD|EUR|GBP|INR|CAD|AUD|JPY|CNY)\b',
                r'([₹$€£¥₩])'
            ]
        }

        self.currency_symbols = {
            '₹': 'INR', '$': 'USD', '€': 'EUR', '£': 'GBP',
            '¥': 'JPY', '₩': 'KRW'
        }

    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
        return text

    def extract_text_pypdf2(self, pdf_path: str) -> str:
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
        return text

    def extract_text(self, pdf_path: str) -> str:
        text = self.extract_text_pdfplumber(pdf_path)
        if not text.strip():
            text = self.extract_text_pypdf2(pdf_path)
        return text

    def clean_amount(self, amount_str: str) -> Optional[float]:
        if not amount_str:
            return None
        cleaned = re.sub(r'[₹$€£¥₩,\s]', '', amount_str)
        try:
            return float(cleaned)
        except (ValueError, InvalidOperation):
            return None

    def extract_field(self, text: str, field_name: str) -> Optional[str]:
        patterns = self.invoice_patterns.get(field_name, [])
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                match = matches[0].strip()
                if match:
                    return match
        return None

    def extract_line_items(self, text: str) -> List[Dict[str, Any]]:
        line_items = []
        item_patterns = [
            r'(\d+)\s+([^\d\n]+?)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            r'([^\n]+?)\s+(\d+)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)'
        ]
        for pattern in item_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                if len(match) >= 4:
                    item = {
                        'description': match[1] if len(match) > 4 else match[0],
                        'quantity': match[0] if len(match) > 4 else match[1],
                        'unit_price': self.clean_amount(match[2] if len(match) > 4 else match[2]),
                        'total_price': self.clean_amount(match[-1])
                    }
                    line_items.append(item)
        return line_items

    def extract_invoice_data(self, pdf_path: str) -> Dict[str, Any]:
        text = self.extract_text(pdf_path)
        if not text.strip():
            return {"error": "Could not extract text from PDF"}
        invoice_data = {
            "file_name": Path(pdf_path).name,
            "extraction_date": datetime.now().isoformat(),
            "invoice_number": self.extract_field(text, 'Invoice No.'),
            "date": self.extract_field(text, 'date'),
            "vendor_name": self.extract_field(text, 'vendor_name'),
            "customer_name": self.extract_field(text, 'customer_name'),
            "currency": self.extract_field(text, 'currency'),
            "subtotal": self.clean_amount(self.extract_field(text, 'subtotal')),
            "tax_amount": self.clean_amount(self.extract_field(text, 'tax_amount')),
            "total_amount": self.clean_amount(self.extract_field(text, 'total_amount')),
            "line_items": self.extract_line_items(text),
            "raw_text":  text
        }
        if invoice_data["currency"] in self.currency_symbols:
            invoice_data["currency"] = self.currency_symbols[invoice_data["currency"]]
        return invoice_data

    def process_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        invoice_data = self.extract_invoice_data(pdf_path)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(invoice_data, f, indent=2, ensure_ascii=False)
            print(f"Invoice data saved to: {output_path}")
        return invoice_data

    def process_multiple_pdfs(self, pdf_directory: str, output_directory: Optional[str] = None) -> List[Dict[str, Any]]:
        pdf_dir = Path(pdf_directory)
        all_invoice_data = []
        if output_directory:
            output_dir = Path(output_directory)
            output_dir.mkdir(exist_ok=True)
        for pdf_file in pdf_dir.glob("*.pdf"):
            print(f"Processing: {pdf_file.name}")
            invoice_data = self.extract_invoice_data(str(pdf_file))
            all_invoice_data.append(invoice_data)
            if output_directory:
                output_file = output_dir / f"{pdf_file.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(invoice_data, f, indent=2, ensure_ascii=False)
        return all_invoice_data


def main():
    parser = argparse.ArgumentParser(description='Extract invoice data from PDF files')
    # parser.add_argument('input', help='Input PDF file or directory')
    # parser.add_argument('-o', '--output', help='Output JSON file or directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    extractor = InvoiceExtractor()
    input_path = Path("./pdf/B.pdf")

    if input_path.is_file() and input_path.suffix.lower() == '.pdf':
        output_path = Path("./pdf/B.json") 
        invoice_data = extractor.process_pdf(str(input_path), output_path)
        if args.verbose:
            print(json.dumps(invoice_data, indent=2, ensure_ascii=False))

    elif input_path.is_dir():
        output_dir = args.output or "extracted_invoices"
        all_data = extractor.process_multiple_pdfs(str(input_path), output_dir)
        if args.verbose:
            for data in all_data:
                print(json.dumps(data, indent=2, ensure_ascii=False))
                print("-" * 50)
    else:
        print(f"Error: {input_path} is not a valid PDF file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
