import pdfplumber

with pdfplumber.open("./pdf/B.pdf") as pdf:
    for p in pdf.pages:
        for t in p.extract_tables():
            for r in t:
                print(r) 