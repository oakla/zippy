"""take input file or folder as argument
ask for password or generate one
zip input file or folder to a pre-defined location"""

import argparse
import subprocess
from pathlib import Path
import tkinter as tk
# from tkinter import simpledialog
import random
import string
import pyperclip
import os
from pathlib import Path
import sys

WINZIP_PATH = r"c:\program files\winzip\wzzip"
WORDS_FILE_NAME = r"eff.org_files_2016_07_18_eff_large_wordlist.txt"
words_file_path = Path(__file__).resolve().with_name(WORDS_FILE_NAME)


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
    print(f"sys._MEIPASS: {sys._MEIPASS}") # type: ignore
else:
    # print('running in a normal Python process')
    ...


with open(words_file_path, 'r') as fp:
    words = [x.split('\t')[1] for x in fp.read().splitlines() if len(x) > 1]

def uniquify(path:Path, modifier:int=0):
    """
    If the path exists, append a number to it to make it unique.
    """
    if modifier == 0:
        candidate_path = path
    else:
        candidate_path = Path(path.parent, path.stem + "(" +str(modifier) + ")" + path.suffix)
    if not candidate_path.exists():
        return candidate_path
    else:
        return uniquify(path, modifier+1)

# def get_output_to_parent_folder_path(source_path:Path):
#     """
#     If the source is a file, return a path to a file with the same name in the same folder.
#     If the source is a folder, return a path to a file with the same name in the parent folder.
#     """
#     if source_path.is_file():
#         return source_path.with_suffix('.zip')
#     if source_path.is_dir():
#         return source_path.parent / (source_path.name + '.zip')
    
# def get_output_to_desktop_path(source_path:Path):
#     # desktop_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#     desktop_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), "OneDrive - Colonial First State", 'Desktop')
#     if source_path.is_file():
#         return Path(desktop_folder) / source_path.with_suffix('.zip').name
#     if source_path.is_dir():
#         return Path(desktop_folder) / (source_path.name + '.zip')

def get_output_path(source_paths:list[Path], to_desktop:bool=True):
    """
    Two options:
    - Send to desktop
    - Send to the parent folder
    """
    if to_desktop:
        output_path_parent = Path(os.path.join(os.path.join(os.environ['USERPROFILE']), "OneDrive - Colonial First State", 'Desktop'))
    else:
        output_path_parent = source_paths[0].parent

    if len(source_paths) > 1:
        output_file_name = "archive"
    elif len(source_paths) == 1:
        output_file_name = source_paths[0].name
    else:
        print("Something went wrong. No source files were provided.")
        input("Press Enter to continue...")
        exit()

    return uniquify((output_path_parent / output_file_name).with_suffix('.zip'))

def get_source_paths():
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument("source_paths", nargs='*', help="input file or folder")
        args = parser.parse_args()
        source_paths = [Path(arg) for arg in args.source_paths]
    except Exception as e:
        exit()
    return source_paths

def zip_with_key(source_paths:list[Path], secure_key=""):
    dest_path = get_output_path(source_paths)
    
    print(f"source_path: {source_paths}")
    print(f"dest_path: {dest_path}")
    commands = [WINZIP_PATH]
    if secure_key:
        commands.append(f"-s{secure_key}")

    commands += [dest_path] + source_paths

    subprocess.run(commands, shell=True)


# Create a function to handle the button click event
def submit_key(option, text_input, source_paths):
    # if option == 1:
    #     zip_with_key(text_input.get())
    # elif option == 2:
    #     zip_with_key(text_input.get())
    # elif option == 3:
    #     zip_with_key(text_input.get())
    # else:
    #     print("No option selected")
    selected_text = text_input.get()
    pyperclip.copy(selected_text)
    zip_with_key(source_paths, selected_text)
    root.destroy()

# Function to update the text input based on the selected radio button
def update_text_input():
    selected_option = radio_var.get()

    if selected_option == 1:
        input_var.set(generate_passpharse())
    elif selected_option == 2:
        input_var.set(generate_password())
    elif selected_option == 3:
        input_var.set("")

def generate_passpharse(k_words:int=3):
    passpharse = []
    for i in range(k_words):
        passpharse.append(random.choice(words))
    return " ".join(passpharse)

def generate_password(length:int = 12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


try:
    source_paths = get_source_paths()
    if __name__ == "__main__" and not source_paths:
        source_paths = [Path(r"C:\Users\Alexander.Oakley\OneDrive - Colonial First State\Desktop\words_pos.csv")]
    if not source_paths:
        exit()
    # Create the main application window
    root = tk.Tk()
    root.title("Create a secure key")
    root.geometry("400x250")

    # Create a variable to store the selected radio button value
    radio_var = tk.IntVar()
    radio_var.set(1)

    # Create radio buttons
    radio_option1 = tk.Radiobutton(root, text="Generate Passphrase", variable=radio_var, value=1, command=update_text_input, font=("Arial", 10))
    radio_option2 = tk.Radiobutton(root, text="Generate Password", variable=radio_var, value=2, command=update_text_input, font=("Arial", 10))
    radio_option3 = tk.Radiobutton(root, text="Custom Key", variable=radio_var, value=3, command=update_text_input, font=("Arial", 10))

    radio_option1.pack(padx=10, pady=5, anchor='w')
    radio_option2.pack(padx=10, pady=5, anchor ='w')
    radio_option3.pack(padx=10, pady=5, anchor ='w')

    # Create a label for the text input box
    input_label = tk.Label(root, text="Chosen key:", font=("Arial", 10))
    input_label.pack(pady=10)

    # Create a text input box
    input_var = tk.StringVar()
    input_var.set(generate_passpharse())
    text_input = tk.Entry(root, textvariable=input_var, font=("Arial", 10), width=50)
    text_input.pack()

    # Bind the <FocusIn> event to the text_input widget
    text_input.bind("<FocusIn>", lambda event: radio_var.set(3))

    # Bind the <Return> event to the text_input widget
    text_input.bind("<Return>", lambda event: submit_key(radio_var.get(), text_input, source_paths))

    # Create a button to trigger the dialogue
    dialogue_button = tk.Button(root, text="Submit and copy key to clipboard", command=lambda: submit_key(radio_var.get(), text_input, source_paths), font=("Arial", 10))
    dialogue_button.pack(pady=10)

    # Set the background color of the GUI
    root.configure(bg="#F0F0F0")

    # Start the main GUI loop
    root.mainloop()

    # input("Press Enter to continue...")
except Exception as e:
    print(e)
    # input("Press Enter to continue...")

