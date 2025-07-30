import os
import pdfplumber

input_file_path = "./pdf/A.pdf"
input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]  # "B"
output_dir = "./boxplumber"
os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist
output_file_path = os.path.join(output_dir, f"{input_file_name}.txt")

with open(output_file_path, "w", encoding="utf-8") as out_file:
    with pdfplumber.open(input_file_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    # Replace None with "" and "(cid:299)" with "RS" in each cell
                    cleaned_row = [
                        (cell.replace("(cid:299)", "RS") if isinstance(cell, str) else "")
                        for cell in row
                    ]
                    out_file.write(str(cleaned_row) + "\n")
