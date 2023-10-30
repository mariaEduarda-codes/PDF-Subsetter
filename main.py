import PySimpleGUI as Psg
from pdf_subsetter_v2 import writes_new_pdf
import os
import time
import re
from pathlib import Path

Psg.theme('DarkTeal12')

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
output1 = Psg.Text("", key="output1")
output2 = Psg.Text("", key="output2")

layout = [[title],
          [source_pdf_showcase, source_pdf_browser],
          [text1, user_input_start_page],
          [text2, user_input_end_page],
          [target_pdf_showcase, target_pdf_browser],
          [text3, output_file_name],
          [subset_pdf_button],
          [output1],
          [output2]]

window = Psg.Window("PDF Subsetter", layout=layout)

while True:
    event, values = window.read()

    if event == Psg.WIN_CLOSED:
        break

    if event == "subset_button":
        output1.update('')
        output2.update('')
        source_pdf_filepath = values["source_pdf_browser"]

        try:
            start_page = int(values["start_page"])
            end_page = int(values["end_page"])
        except ValueError:
            output1.update("You must enter an integer number when providing start and end page. Try again.",
                           text_color="red")
            continue

        target_pdf_folder_path = values["target_pdf_browser"]
        if target_pdf_folder_path == '':
            # If no Target Folder is provided, send the file to the Downloads directory
            target_pdf_folder_path = str(Path.home() / "Downloads")
            output1.update(f"Since no Target Folder was provided, you'll find your file in {target_pdf_folder_path}")

        output_file_name = values["output_file_name"]

        if output_file_name == '':
            output_file_name = f"{time.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"

        if not output_file_name.endswith(".pdf"):
            output_file_name = f"{values['output_file_name']}.pdf"

        # Prevents duplicate files from being overwritten
        list_of_files_in_chosen_directory = os.listdir(target_pdf_folder_path)

        count_existing = 0
        pattern = r'\s?(\(\d\)\.pdf)'

        for file in list_of_files_in_chosen_directory:
            match = re.search(pattern, file)
            if match is None:
                output_file_name = f"{output_file_name}"
                if output_file_name == file:
                    output_file_name = f"{output_file_name.strip('.pdf')} ({count_existing + 1}).pdf"
                continue
            elif output_file_name.strip(match.group(0)).strip('.pdf') == file.strip(match.group(0)).strip():
                count_existing += 1
                output_file_name = f"{output_file_name.strip(match.group(0)).strip('.pdf')} ({count_existing + 1}).pdf"

        complete_filepath = os.path.join(target_pdf_folder_path, output_file_name)
        # End of block - Prevents duplicate files from being overwritten

        try:
            writes_new_pdf(source_pdf_filepath, start_page, end_page,  complete_filepath)
        except OSError:
            output1.update("Make sure you choose a file with a .pdf extension. Try again.", text_color="red")
            continue
        except ValueError as exc:
            output1.update(str(exc), text_color="red")
            continue
        print("Completed")

        output2.update("Process completed.", text_color='green')
