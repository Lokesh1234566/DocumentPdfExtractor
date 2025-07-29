from docling_core.types.doc.page import TextCellUnit
from docling_parse.pdf_parser import DoclingPdfParser, PdfDocument

parser = DoclingPdfParser()

pdf_doc: PdfDocument = parser.load(
    path_or_stream="./pdf/B.pdf"
)

# PdfDocument.iterate_pages() will automatically populate pages as they are yielded.
for page_no, pred_page in pdf_doc.iterate_pages():

    # iterate over the word-cells
    for word in pred_page.iterate_cells(unit_type=TextCellUnit.WORD):
        print(word.rect, ": ", word.text)

        # create a PIL image with the char cells
    img = pred_page.render_as_image(cell_unit=TextCellUnit.CHAR)
    img.show()