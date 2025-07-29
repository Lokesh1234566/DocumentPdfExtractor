import pdfplumber

output_file_path = "clean_output.txt"  # Final cleaned output file

with open(output_file_path, "w", encoding="utf-8") as out_file:
    with pdfplumber.open("./pdf/B.pdf") as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    # Replace None with "" and "(cid:299)" with "RS" in each cell
                    cleaned_row = [
                        (cell.replace("(cid:299)", "RS") if isinstance(cell, str) else "")
                        for cell in row
                    ]
                    out_file.write(str(cleaned_row) + "\n")
