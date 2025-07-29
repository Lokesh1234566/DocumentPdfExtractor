from docling.document_converter import DocumentConverter

# For a local file
source_path = "./pdf/G.pdf"  # Replace with your local document path

# Create a converter and convert the file
converter = DocumentConverter()
result = converter.convert(source_path)

# Access the converted document
document = result.document

# Export to HTML format
md_output = document.export_to_markdown()

# Save the output to an HTML file
output_path = "./Docling_G.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(md_output)

print(f"HTML saved to: {output_path}")
