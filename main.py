import PySimpleGUI as Psg
from pdf_subsetter_v2 import writes_new_pdf
import os

title = Psg.Text("PDF Subsetter")
source_pdf_showcase = Psg.Input(key="source_pdf_browser")
source_pdf_browser = Psg.FileBrowse("Choose PDF")

text1 = Psg.Text("Start page:")
user_input_start_page = Psg.Input(key="start_page")
text2 = Psg.Text("End page:")
user_input_end_page = Psg.Input(key="end_page")

target_pdf_showcase = Psg.Input(key="target_pdf_browser")
target_pdf_browser = Psg.FolderBrowse("Select target folder")
text3 = Psg.Text("Enter the name of the new file: ")
output_file_name = Psg.Input(key="output_file_name")

subset_pdf_button = Psg.Button("Subset PDF", key="subset_button")
output = Psg.Text("", key="output", text_color="green")

layout = [[title],
          [source_pdf_showcase, source_pdf_browser],
          [text1, user_input_start_page],
          [text2, user_input_end_page],
          [target_pdf_showcase, target_pdf_browser],
          [text3, output_file_name],
          [subset_pdf_button],
          [output]]

window = Psg.Window("PDF Subsetter", layout=layout)

while True:
    event, values = window.read()

    if event == Psg.WIN_CLOSED:
        break

    if event == "subset_button":
        source_pdf_filepath = values["source_pdf_browser"]

        try:
            start_page = int(values["start_page"])
            end_page = int(values["end_page"])
        except ValueError:
            output.update("You must enter an integer number when providing start and end page. Try again.",
                          text_color="red")
            continue

        target_pdf_folder_path = values["target_pdf_browser"]
        output_file_name = values["output_file_name"]
        if not output_file_name.endswith(".pdf"):
            output_file_name = f"{values['output_file_name']}.pdf"
        complete_filepath = os.path.join(target_pdf_folder_path, output_file_name)

        try:
            writes_new_pdf(source_pdf_filepath, start_page, end_page,  complete_filepath)
        except OSError:
            output.update("Make sure you choose a file with a .pdf extension. Try again.", text_color="red")
            continue
        except ValueError as exc:
            output.update(str(exc), text_color="red")
            continue
        print("Completed")

        output.update("Process completed.", text_color='green')
