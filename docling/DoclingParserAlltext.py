
from docling_core.types.doc.page import TextCellUnit
from docling_parse.pdf_parser import DoclingPdfParser, PdfDocument
from docling.document_converter import DocumentConverter
parser = DoclingPdfParser()

# pdf_doc: PdfDocument = parser.load(
#     path_or_stream="C:\Allfiles\A.pdf"
# )
converter = DocumentConverter()
result = converter.convert("../pdf/sb_tech_1.pdf")
# print(result.document.export_to_markdown()) 
print(result.document.export_to_text())
# PdfDocument.iterate_pages() will automatically populate pages as they are yielded.
#for page_no, pred_page in pdf_doc.iterate_pages():

    # iterate over the word-cells
   # for word in pred_page.iterate_cells(unit_type=TextCellUnit.WORD):
          # iterate over the word-cells   print(word.rect, ": ", word.text)
    #    print( word.text)

        # create a PIL image with the char cells
     #img = pred_page.render_as_image(cell_unit=TextCellUnit.CHAR)
     #img.show()