import os
import re
import datauri

from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral

# Configuration
load_dotenv()
client = Mistral(api_key="RKeFQOVcNf0aYwiCJ5Uv3tr32wHSFOS6")
doc = Path("./pdf/A.pdf")

# File upload
uploaded_doc = client.files.upload(
    file={"file_name": doc.stem, "content": Path(doc).read_bytes()},
    purpose="ocr",
)
url = client.files.get_signed_url(file_id=uploaded_doc.id).url

# OCR processing
response = client.ocr.process(
    model="mistral-ocr-latest",
    document={"type": "document_url", "document_url": url},
    include_image_base64=True,
)

# Save markdown and images
with open("mistraljsonA", "wt",encoding='utf-8') as f:
    for page in response.pages:
        f.write(page.model_dump_json)
        for img in page.images:
            image_data = datauri.parse(img.image_base64).data
            with open(f"{img.id}", "wb") as img_file:
                img_file.write(image_data)