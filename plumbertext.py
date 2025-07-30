import os
import pdfplumber

def extract_text_with_layout(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        print(f"Total number of pages: {page_count}\n")
        for page in pdf.pages:
            text = page.extract_text(layout=True)
            if text:
                full_text += text + "\n"
    return full_text

# Input PDF
input_file_path = "./pdf/vaco_2.pdf"
input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]

# Output directory and file path
output_dir = "./plumbertext"
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, f"{input_file_name}.txt")

# Extract text and save to file
text = extract_text_with_layout(input_file_path)
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\nExtracted text saved to: {output_file_path}")
