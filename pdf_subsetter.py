import PyPDF2

INPUT_PATH = r"C:\Users\maria\Downloads\Hardware.pdf"
OUTPUT_PATH = r"C:\Users\maria\Downloads\HardwareSubset.pdf"


def subset_pdf(start_page, end_page, input_path=INPUT_PATH, output_path=OUTPUT_PATH):
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        print("Subsetting complete!")


user_input_start_page = int(input("Enter the start page you want to subset: "))
user_input_end_page = int(input("Enter the end page you want to subset: "))

subset_pdf(user_input_start_page, user_input_end_page)
