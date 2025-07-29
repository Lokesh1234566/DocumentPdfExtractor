import pymupdf

# Open some document, for example a PDF (could also be EPUB, XPS, etc.)
doc = pymupdf.open("./pdf/A.pdf")

# Load a desired page. This works via 0-based numbers
page = doc[1]  # this is the first page

# Look for tables on this page and display the table count
tables = page.find_tables()
print(f"{len(tables.tables)} table(s) on {page}")

# We will see a message like "1 table(s) on page 0 of input.pdf"
if tables.tables:
    for index, table in enumerate(tables):
        print(f"Table {index+1} found:")
            # Convert table to Markdown
        md_table = table.to_markdown()
        print("Markdown representation:")
        print(md_table)

            # Convert table to a Pandas DataFrame for further analysis
        df_table = table.to_pandas()
        df_table.to_excel(f"{doc.name}-{page.number}.xlsx")
        print("Pandas DataFrame:")
        print(df_table)

            # Optional: Export the DataFrame to other formats (CSV, JSON, Excel)
            # df_table.to_csv(f"table_{index+1}.csv", index=False)
else:
    print("No tables found on this page.")