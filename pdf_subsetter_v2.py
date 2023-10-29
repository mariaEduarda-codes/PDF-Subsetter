import PyPDF2


def writes_new_pdf(source_pdf_file_path, start_page, end_page, target_pdf_complete_filepath):
    """

    :param source_pdf_file_path:
    :param start_page:
    :param end_page:
    :param target_pdf_complete_filepath:
    :return: final_target_file

    Receives the source PDF file as an argument.
    Receives the number of the page that will be the first page of the new PDF file.
    Receives the number of the page that will be the last page of the new PDF file.
    Receives the complete filepath of the new file, including its name.
    Returns the final_target_file rightfully written.
    """

    # Initializing the object that will write the new PDF
    pdf_writer = PyPDF2.PdfWriter()

    # Opens the source file in read mode and writes it to a target_file. Checks for extensions different from .pdf
    with open(source_pdf_file_path, 'rb') as source_pdf_filepath:
        source_pdf_file = PyPDF2.PdfReader(source_pdf_filepath)

        # if not (0 < start_page <= len(source_pdf_file.pages)):
        #     raise ValueError(f"Start page not in range. Maximum of {len(source_pdf_file.pages)} pages allowed.")
        # elif not (start_page <= end_page <= len(source_pdf_file.pages)):
        #     raise ValueError(f"End page not in range. Maximum of {len(source_pdf_file.pages)} pages allowed.")

        if not (0 < start_page <= len(source_pdf_file.pages)):
            raise ValueError(f"Start page not in range. Maximum of {len(source_pdf_file.pages)} pages allowed.")
        elif not (start_page <= end_page):
            raise ValueError(f"End page cannot be less than start page.")
        elif not (end_page <= len(source_pdf_file.pages)):
            raise ValueError(f"End page not in range. Maximum of {len(source_pdf_file.pages)} pages allowed.")

        for page_number in range(start_page - 1, min(end_page, len(source_pdf_file.pages))):
            pdf_writer.add_page(source_pdf_file.pages[page_number])

    with open(target_pdf_complete_filepath, 'wb') as target_file:
        final_target_file = pdf_writer.write(target_file)

    return final_target_file
