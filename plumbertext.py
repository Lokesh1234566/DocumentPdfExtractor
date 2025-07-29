import pdfplumber

def extract_text_with_layout(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        print(f"Total number of pages: {page_count}\n")
        for page in pdf.pages:
            full_text += page.extract_text(layout=True) + "\n"
    return full_text

# Usage
text = extract_text_with_layout("./pdf/E.pdf")
print(text)
