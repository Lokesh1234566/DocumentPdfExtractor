import fitz  # PyMuPDF
import cv2
import numpy as np

pdf_path = "./pdf/B.pdf"
doc = fitz.open(pdf_path)
page = doc.load_page(0)  # Load the first page
pix = page.get_pixmap()
img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
    (pix.height, pix.width, pix.n)
)
# Convert to BGR for OpenCV if necessary (PyMuPDF often gives RGB)
if pix.n == 4: # RGBA
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
elif pix.n == 3: # RGB
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

# Now 'img_array' is an OpenCV-compatible image

gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV) # Adjust threshold value


contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

bounding_boxes = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    bounding_boxes.append((x, y, w, h))

# Optionally, draw the bounding boxes on the original image
for (x, y, w, h) in bounding_boxes:
    cv2.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 0), 2) # Green rectangle
    
cv2.imshow("Image with Bounding Boxes", img_array)
cv2.waitKey(0)
cv2.destroyAllWindows()