# import fitz # PyMuPDF


# pdf_path = "./pdf/B.pdf"
# doc = fitz.open(pdf_path)
# for i, page in enumerate(doc):
#     pix = page.get_pixmap()
#     pix.save(f"page_{i+1}.png")
# doc.close()
########################################################
# import easyocr
# reader = easyocr.Reader(['en']) # Specify language(s)
# result = reader.readtext("./page_1.png")
# extracted_text = " ".join([text[1] for text in result])
# print(extracted_text)

###############################################################################
# import pytesseract
# from PIL import Image

# # Set the path to the Tesseract executable (if not in your system's PATH)
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

# # Open the image
# img = Image.open('./page_1.png')

# # Perform OCR, specifying English as the language
# text = pytesseract.image_to_string(img, lang='eng')

# print(text) 

#############################################################################
# from PIL import Image
# import pytesseract

#     # Set the path to your Tesseract executable (if not in system PATH)
#     # pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

# def extract_text_from_image(image_path):
#         """Extracts text from an image using Pytesseract."""
#         try:
#             img = Image.open(image_path)
#             # text = pytesseract.image_to_string(img)
#             config = '--psm 6 -l eng'
#             text = pytesseract.image_to_string(img, config=config)
#             return text
#         except Exception as e:
#             return f"Error: {e}"

#     # Example usage
# image_file = './page_1.png'  # Replace with your image file
# extracted_text = extract_text_from_image(image_file )
# print(extracted_text)

###################################################################################


import easyocr
reader = easyocr.Reader(['en']) # For English text
result = reader.readtext('./page_1.png')
print(result)