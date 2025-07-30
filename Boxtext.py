# import pdfplumber

# with pdfplumber.open("./pdf/B.pdf") as pdf:
#     for p in pdf.pages:
#         for t in p.extract_tables():
#             for r in t:
#                 print(r) 


import os
import pdfplumber

# Input file path
input_file_path = "./pdf/ups_2021_02_16 6_59 pm Office Lens_02.pdf"

# Extract file name without extension
input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]

# Output directory and file path
output_dir = "./Boxtextplumber"
os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist
output_file_path = os.path.join(output_dir, f"{input_file_name}.txt")

# Extract tables and write to output file
with open(output_file_path, "w", encoding="utf-8") as out_file:
    with pdfplumber.open(input_file_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    out_file.write(str(row) + "\n")

