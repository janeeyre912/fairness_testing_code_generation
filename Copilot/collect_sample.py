import os.path
import time
from os.path import join
import json
import jsonlines
import os
import subprocess
import pyautogui
import pyperclip


def get_code_line_info(folder_path):
    """
    Gets the total line number including empty lines and comments for each Python file in the given folder
    and stores them in a list.

    :param folder_path: The path to the folder containing Python files.
    :return: A list of tuples, each containing the file path and its total line number.
    """
    code_line_info = []

    # List all files in the given folder
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Check if the current item is a file and has a .py extension
        if os.path.isfile(file_path) and filename.endswith('.py'):
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # The total line number is the count of all lines
                total_line_number = len(lines)

                # Append the file path and total line number as a tuple to the list
                code_line_info.append((file_path, total_line_number))

    return code_line_info


def run_robot(file, line, index):
    # run vscode from terminal and goto
    subprocess.run(['code', '--goto', f'{file}:{line + 1}'], shell=True)
    time.sleep(15)
    # pyautogui.hotkey('enter')
    # time.sleep(2)
    # pyautogui.hotkey('up')
    # time.sleep(2)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(20)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(3)
    copied_text = pyperclip.paste()
    # copied_text = copied_text.replace("=======\nSuggestion", "=======\n# Suggestion")
    print("Copied Text:", copied_text)

    # if "Synthesizing" not in copied_text:
    #     print("Error: Copilot not working")
    #     print("printed text:\n", copied_text)
    #     exit()

    pyautogui.hotkey('alt', 'f4')
    time.sleep(3)

    with open("output/output" + str(index) + ".txt", "w") as f:
        f.write(copied_text)
    print("Saved to:", "output/output" + str(index) + ".txt")
    time.sleep(3)


# Example usage
folder_path = 'C:/Master/Test_code_generation/Code_Tests/dataset/separate_prompt'
code_info = get_code_line_info(folder_path)
output_no = 1
for file_path, total_lines in code_info:
    # print(f"File: {file_path}, Total lines (including empty lines and comments): {total_lines}")
    run_robot(file_path, total_lines, output_no)
    time.sleep(2)
    output_no = output_no + 1
