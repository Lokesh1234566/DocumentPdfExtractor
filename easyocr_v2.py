import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        pix = doc.load_page(page_num).get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        text += pytesseract.image_to_string(img) + "\n"
    return text

# Usage
ocr_text = extract_text_with_ocr("./pdf/A.pdf")
print(ocr_text)
