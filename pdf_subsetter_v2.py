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

    with open(source_pdf_file_path, 'rb') as source_pdf_filepath:
        source_pdf_file = PyPDF2.PdfReader(source_pdf_filepath)

        for page_number in range(start_page - 1, min(end_page, len(source_pdf_file.pages))):
            pdf_writer.add_page(source_pdf_file.pages[page_number])

    with open(target_pdf_complete_filepath, 'wb') as target_file:
        final_target_file = pdf_writer.write(target_file)

    return final_target_file


if __name__ == "__main__":
    name_of_source_filepath = input("Enter the complete source filepath: ")
    print(name_of_source_filepath)

    user_input_start_page = int(input("Enter the start page of the file: "))
    user_input_end_page = int(input("Enter the end page of the file: "))
    name_of_target_complete_filepath = input("Enter the complete target filepath (including the name of the file): ")

    name_of_target_pdf = writes_new_pdf(name_of_source_filepath, user_input_start_page, user_input_end_page,
                                        name_of_target_complete_filepath)
    print("Operation complete")
