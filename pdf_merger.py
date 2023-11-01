from PyPDF2 import PdfReader, PdfWriter


def pdf_merger(source_pdf1_complete_filepath, source_pdf2_complete_filepath, target_pdf_complete_filepath):
    """

    :param source_pdf1_complete_filepath: The complete filepath of the first PDF to be added
    :param source_pdf2_complete_filepath: The complete filepath of the second PDF to be added
    :param target_pdf_complete_filepath: The complete filepath, including the name, of the new PDF,
    which is a combination of both PDFs previously provided
    :return: returns the merged file
    """
    new_pdf = PdfWriter()

    with open(source_pdf1_complete_filepath, 'rb') as source1:
        source_pdf1 = PdfReader(source1)
        for page in source_pdf1.pages:
            new_pdf.add_page(page)

    with open(source_pdf2_complete_filepath, "rb") as source2:
        source_pdf2 = PdfReader(source2)
        for page in source_pdf2.pages:
            new_pdf.add_page(page)

    with open(target_pdf_complete_filepath, "wb") as final_file:
        return new_pdf.write(final_file)
