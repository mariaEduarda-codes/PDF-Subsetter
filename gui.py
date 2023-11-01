import PySimpleGUI as sg
import time
import os
import re
from pathlib import Path
from pdf_subsetter_v2 import writes_new_pdf
from pdf_merger import pdf_merger

sg.theme('DarkTeal12')

title = sg.Text("PDF Subsetter")
source_pdf_showcase_subsetter = sg.Input(key="source_pdf_browser_subsetter")
source_pdf_browser_subsetter = sg.FileBrowse("Choose PDF")

text1 = sg.Text("Start page:")
user_input_start_page = sg.Input(key="start_page")
text2 = sg.Text("End page:")
user_input_end_page = sg.Input(key="end_page")

target_pdf_showcase_subsetter = sg.Input(key="target_pdf_browser_subsetter")
target_pdf_browser_subsetter = sg.FolderBrowse("Select target folder")
text3 = sg.Text("Enter the name of the new file: ")
output_file_name_subsetter = sg.Input(key="output_file_name_subsetter")

subset_pdf_button = sg.Button("Subset PDF", key="subset_button")
output1_subsetter = sg.Text("", key="output1_subsetter")
output2_subsetter = sg.Text("", key="output2_subsetter")

layout_tab_pdf_subsetter = [[title],
                            [source_pdf_showcase_subsetter, source_pdf_browser_subsetter],
                            [text1, user_input_start_page],
                            [text2, user_input_end_page],
                            [target_pdf_showcase_subsetter, target_pdf_browser_subsetter],
                            [text3, output_file_name_subsetter],
                            [subset_pdf_button],
                            [output1_subsetter],
                            [output2_subsetter]]

title = sg.Text("PDF Merger")
source_pdf_showcase_merger1 = sg.Input(key="source_pdf_browser_merger1")
source_pdf_browser_merger1 = sg.FileBrowse("Choose 1st PDF")

source_pdf_showcase_merger2 = sg.Input(key="source_pdf_browser_merger2")
source_pdf_browser_merger2 = sg.FileBrowse("Choose 2nd PDF")

target_pdf_showcase_merger = sg.Input(key="target_pdf_browser_merger")
target_pdf_browser_merger = sg.FolderBrowse("Select target folder")

text4 = sg.Text("Enter the name of the new file: ")
output_file_name_merger = sg.Input(key="output_file_name_merger")

merge_pdf_button = sg.Button("Merge PDF", key="merge_button")
output1_merger = sg.Text('', key="output1_merger")
output2_merger = sg.Text('', key="output2_merger")

layout_tab_pdf_merger = [[title],
                         [source_pdf_showcase_merger1, source_pdf_browser_merger1],
                         [source_pdf_showcase_merger2, source_pdf_browser_merger2],
                         [target_pdf_showcase_merger, target_pdf_browser_merger],
                         [text4, output_file_name_merger],
                         [merge_pdf_button],
                         [output1_merger],
                         [output2_merger]]

layout = [
    [sg.TabGroup([
        [sg.Tab('PDF Subsetter', layout_tab_pdf_subsetter, key='pdf_subsetter_tab')],
        [sg.Tab('PDF Merger', layout_tab_pdf_merger, key="pdf_merger_tab")]
    ])]
]

window = sg.Window('PDF Toolkit', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'subset_button':
        output1_subsetter.update('')
        output2_subsetter.update('')
        source_pdf_filepath = values["source_pdf_browser_subsetter"]

        try:
            start_page = int(values["start_page"])
            end_page = int(values["end_page"])
        except ValueError:
            output1_subsetter.update("You must enter an integer number when providing start and end page. "
                                     "Try again.", text_color="red")
            continue

        target_pdf_folder_path = values["target_pdf_browser_subsetter"]
        if target_pdf_folder_path == '':
            # If no Target Folder is provided, send the file to the Downloads directory
            target_pdf_folder_path = str(Path.home() / "Downloads")
            output1_subsetter.update(f"Since no Target Folder was provided, "
                                     f"you'll find your file in {target_pdf_folder_path}")

        output_file_name_subsetter = values["output_file_name_subsetter"]

        if output_file_name_subsetter == '':
            output_file_name_subsetter = f"{time.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"

        if not output_file_name_subsetter.endswith(".pdf"):
            output_file_name_subsetter = f"{values['output_file_name_subsetter']}.pdf"

        # Prevents duplicate files from being overwritten
        list_of_files_in_chosen_directory = os.listdir(target_pdf_folder_path)

        count_existing = 0
        pattern = r'\s?(\(\d\)\.pdf)'

        for file in list_of_files_in_chosen_directory:
            match = re.search(pattern, file)
            if match is None:
                output_file_name_subsetter = f"{output_file_name_subsetter}"
                if output_file_name_subsetter == file:
                    output_file_name_subsetter = (f"{output_file_name_subsetter.strip('.pdf')} "
                                                  f"({count_existing + 1}).pdf")
                continue
            elif output_file_name_subsetter.strip(match.group(0)).strip('.pdf') == file.strip(match.group(0)).strip():
                count_existing += 1
                output_file_name_subsetter = (f"{output_file_name_subsetter.strip(match.group(0)).strip('.pdf')} "
                                              f"({count_existing + 1}).pdf")

        complete_filepath = os.path.join(target_pdf_folder_path, output_file_name_subsetter)
        # End of block - Prevents duplicate files from being overwritten

        try:
            writes_new_pdf(source_pdf_filepath, start_page, end_page, complete_filepath)
        except OSError:
            output1_subsetter.update("Make sure you choose a file with a .pdf extension. Try again.", text_color="red")
            continue
        except ValueError as exc:
            output1_subsetter.update(str(exc), text_color="red")
            continue
        print("Completed")

        output2_subsetter.update("Process completed.", text_color='green')

    if event == 'merge_button':
        output1_merger.update('')
        output2_merger.update('')

        source_pdf_filepath_merger1 = values["source_pdf_browser_merger1"]
        source_pdf_filepath_merger2 = values["source_pdf_browser_merger2"]

        target_pdf_folder_path_merger = values["target_pdf_browser_merger"]
        if target_pdf_folder_path_merger == '':
            target_pdf_folder_path_merger = str(Path.home() / "Downloads")
            output1_merger.update(f"Since no target folder was provided, you'll find your file at "
                                  f"{target_pdf_folder_path_merger}")

        output_file_name_merger = values["output_file_name_merger"]
        if output_file_name_merger == '':
            output_file_name_merger = f"{time.strftime('%d-%m-%Y_%H-%M-%S')}.pdf"

        if not output_file_name_merger.endswith(".pdf"):
            output_file_name_merger = f"{values['output_file_name_merger']}.pdf"

        list_of_files_in_chosen_directory = os.listdir(target_pdf_folder_path_merger)

        count_existing = 0
        pattern = r'\s?(\(\d\)\.pdf)'

        for file in list_of_files_in_chosen_directory:
            match = re.search(pattern, file)
            if match is None:
                output_file_name_merger = f"{output_file_name_merger}"
                if output_file_name_merger == file:
                    output_file_name_merger = f"{output_file_name_merger.strip('.pdf')} ({count_existing + 1}).pdf"
                continue
            elif output_file_name_merger.strip(match.group(0)).strip('.pdf') == file.strip(match.group(0)).strip():
                count_existing += 1
                output_file_name_merger = (f"{output_file_name_merger.strip(match.group(0)).strip('.pdf')}"
                                           f" ({count_existing + 1}).pdf")

        target_pdf_complete_filepath_merger = os.path.join(target_pdf_folder_path_merger, output_file_name_merger)

        try:
            pdf_merger(source_pdf_filepath_merger1, source_pdf_filepath_merger2, target_pdf_complete_filepath_merger)
        except OSError:
            output1_merger.update("Make sure you choose a file with a .pdf extension. Try again.", text_color='red')
            continue
        print("Merge completed")

        output2_merger.update("Process completed.", text_color='green')
