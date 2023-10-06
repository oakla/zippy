"""take input file or folder as argument
ask for password or generate one
zip input file or folder to a pre-defined location"""

import argparse
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import string
from typing import Optional
import pyperclip
import os
from pathlib import Path
import sys
import toml

WORDS_FILE_NAME = r"eff.org_files_2016_07_18_eff_large_wordlist.txt"
words_file_path = Path(__file__).resolve().with_name(WORDS_FILE_NAME)
CONFIG_FILE = r"config.toml"
config_file_path = Path(__file__).resolve().with_name(CONFIG_FILE)
config_dict = toml.load(config_file_path)

def get_default_winzip_path():
    return config_dict["DEFAULT"]["winzip_cli_path"]

def get_winzip_path_from_toml():
    custom_settings = config_dict.get("CUSTOM")
    if not custom_settings:
        return get_default_winzip_path()
    custom_winzip_path = custom_settings.get("winzip_cli_path")
    if not custom_winzip_path:
        return get_default_winzip_path()
    return custom_winzip_path

# Function to ask for a file path
def ask_for_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        return file_path
    else:
        return None

def ask_for_winzip_cli_path(expected_path=""):
    messagebox.showinfo(
        "Error", 
        f"WinZip CLI was not found at the expected path.\n\n"
            + "A file selection dialogue will appear after you close this message box. You will then have two options.\n\n" \
            "1) If you know the path to `wzzip.exe` on your machine, select it, then hit 'Open'.\n\n" \
            "2) If you do NOT know the path to `wzzip.exe` on your machine, just hit 'Cancel'.\n\n" \
            f"The expected path is {expected_path}.\n\n" \
            f"You can view and edit the saved paths in the config file at {config_file_path}.\n\n" \
            )

    return ask_for_file()

# def ask_for_winzip_cli_path(expected_path=""):
#     # Create the main window
#     missing_path_root = tk.Tk()
#     missing_path_root.title("Error")

#     # Create a label
#     label = tk.Label(missing_path_root, text=f"WinZip CLI was not found at the expected path: {expected_path}.\nPlease specify the path to the winzip executable or abort the program.")
#     label.pack(padx=20, pady=20)

#     message_button = tk.Button(missing_path_root, text="Abort and close", command=missing_path_root.destroy)
#     message_button.pack()

#     file_button = tk.Button(missing_path_root, text="Select File", command=ask_for_file)
#     file_button.pack()

#     # Start the tkinter main loop
#     missing_path_root.mainloop()

def overwrite_toml(toml_file_path:Path, data:dict):
    with open(toml_file_path, 'w') as fp:
        toml.dump(data, fp)

def save_winzip_path(winzip_cli_path):
    config_dict["CUSTOM"] = {"winzip_cli_path": winzip_cli_path}
    overwrite_toml(config_file_path, config_dict)

def get_winzip_cli_path() -> str:
    winzip_cli_path = get_winzip_path_from_toml()

    if Path(winzip_cli_path).exists():
        return winzip_cli_path
    else:
        new_winzip_cli_path = ask_for_winzip_cli_path(winzip_cli_path)
        if new_winzip_cli_path:
            save_winzip_path(new_winzip_cli_path)
            return new_winzip_cli_path
        else:
            exit()

winzip_cli_path = get_winzip_cli_path()

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    messagebox.showinfo('running in a PyInstaller bundle')
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
        return None

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

def notify_zip_failed(explanation:Optional[str]=None):
    if not explanation:
        explanation = "Zip command did not exectute successfully."
    messagebox.showinfo("Zip didn't happen.", explanation)

def zip(source_paths:list[Path], secure_key=""):
    if not source_paths:
        notify_zip_failed("No source files were provided.\n\nTry drag and drop a file onto the Zippy shortcut icon.")
        return
    dest_path = get_output_path(source_paths)
    if dest_path is None:
        notify_zip_failed("Failed to get output path.")
        return
    
    print(f"source_path: {source_paths}")
    print(f"dest_path: {dest_path}")
    commands = [winzip_cli_path]
    if secure_key:
        commands.append(f"-s{secure_key}")

    commands += [dest_path] + source_paths

    completed_process = subprocess.run(commands, shell=True)

    # check completed process
    if completed_process.returncode == 0:
        return
    else:
        notify_zip_failed(f"Zip command did not exectute successfully.\n\n Error message: {completed_process.stderr}")
        return

# Create a function to handle the button click event
def submit_key(option, text_input, source_paths, tk_root):
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
    zip(source_paths, selected_text)
    tk_root.destroy()

def generate_passpharse(k_words:int=4):
    passpharse = []
    for i in range(k_words):
        passpharse.append(random.choice(words))
    return " ".join(passpharse)

def generate_password(length:int = 12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def run_zippy():
    # Function to update the text input based on the selected radio button
    def update_text_input():
        selected_option = radio_var.get()

        if selected_option == 1:
            input_var.set(generate_passpharse())
        elif selected_option == 2:
            input_var.set(generate_password())
        elif selected_option == 3:
            input_var.set("")

    try:
        source_paths = get_source_paths()
        # if __name__ == "__main__" and not source_paths:
        #     source_paths = [Path(r"C:\Users\Alexander.Oakley\OneDrive - Colonial First State\Desktop\words_pos.csv")]
        if not source_paths:
            messagebox.showinfo("Error", "No source files were provided.\n\nTry drag and drop a file onto the Zippy shortcut icon.")
            # exit()
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
        text_input.bind("<Return>", lambda event: submit_key(radio_var.get(), text_input, source_paths, root))

        # Create a button to trigger the dialogue
        dialogue_button = tk.Button(root, text="Submit and copy key to clipboard", command=lambda: submit_key(radio_var.get(), text_input, source_paths, root), font=("Arial", 10))
        dialogue_button.pack(pady=10)

        # Set the background color of the GUI
        root.configure(bg="#F0F0F0")

        # Start the main GUI loop
        root.mainloop()

        # input("Press Enter to continue...")
    except Exception as e:
        print(e)
        # input("Press Enter to continue...")

run_zippy()