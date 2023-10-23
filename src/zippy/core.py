"""take input file or folder as argument
ask for password or generate one
zip input file or folder to a pre-defined location"""

from logging import config
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import string
from typing import Optional, Union
import pyperclip
import os
from pathlib import Path
import sys
from zippy.settings import Settings
from zippy.path_management import uniquify


class Zippy:

    def __init__(
            self, 
            source_paths:list[Path],
            ):
        self.source_paths = source_paths

        with open(Settings.words_file_path, 'r') as fp:
            self.phrase_phrase_words = [x.split('\t')[1] for x in fp.read().splitlines() if len(x) > 1]

        if not self.check_winzip_cli_path_exists():
            self.show_error_message(
                f'The WinZip CLI executbale was not found at the expected path: {Settings.winzip_cli_path}.\n\n' \
                f'You can view and edit the expected path in the config file at {Settings.config_file_path}.\n\n' \
                f'Note that the WinZip CLI executbale is distinct from the WinZip GUI executable which is usually called "WZZIP.EXE"')


    def check_winzip_cli_path_exists(self):
        return Path(Settings.winzip_cli_path).exists()


    def show_error_message(self, message:str):
        messagebox.showinfo("Error", message)

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        messagebox.showinfo('running in a PyInstaller bundle')
        print(f"sys._MEIPASS: {sys._MEIPASS}") # type: ignore
    else:
        # print('running in a normal Python process')
        ...


    def get_output_path(self, source_paths:list[Path], to_desktop:bool=True):
        """
        Two options:
        - Send to desktop (default)
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

    def notify_zip_failed(self,explanation:Optional[str]=None):
        if not explanation:
            explanation = "Zip command did not exectute successfully."
        messagebox.showinfo("Zip didn't happen.", explanation)

    def make_zip_file(self,source_paths:list[Path], secure_key=""):
        if not source_paths:
            self.notify_zip_failed("No source files were provided.\n\nTry drag and drop a file onto the Zippy shortcut icon.")
            return
        dest_path = self.get_output_path(source_paths)
        if dest_path is None:
            self.notify_zip_failed("Failed to get output path.")
            return
        
        print(f"source_path: {source_paths}")
        print(f"dest_path: {dest_path}")
        commands = [Settings.winzip_cli_path]
        if secure_key:
            secure_key = '"' + secure_key + '"'
            commands.append(f"-s{secure_key}")
            commands.append("-yc") # Use AES Encryption

        commands += [dest_path] + source_paths

        completed_process = subprocess.run(commands, shell=True)

        # check completed process
        if completed_process.returncode == 0:
            return
        else:
            self.notify_zip_failed(f"Zip command did not exectute successfully.\n\n Error message: {completed_process.stderr}")
            return

    # Create a function to handle the button click event
    def submit_key(self, option, text_input, source_paths, tk_root):
        # if option == 1:
        #     zip_with_key(text_input.get())
        # elif option == 2:
        #     zip_with_key(text_input.get())
        # elif option == 3:
        #     zip_with_key(text_input.get())
        # else:
        #     print("No option selected")
        secure_key = text_input.get()
        illegal_characters = "\"'\\/"
        for char in illegal_characters:
            if char in secure_key:
                messagebox.showinfo(
                    "Error", 
                    f"The secure key cannot contain the following characters: {illegal_characters}\n\n" \
                        f"Try again.")
                exit()
            
        pyperclip.copy(secure_key)
        self.make_zip_file(source_paths, secure_key)
        tk_root.destroy()

    def generate_passpharse(self, k_words:int=4):
        passpharse = []
        for i in range(k_words):
            passpharse.append(random.choice(self.phrase_phrase_words))
        return " ".join(passpharse)

    def generate_password(self, length:int = 12):
        special_characters = "!@#$%^&*()_+?"
        
        characters = string.ascii_letters + string.digits + special_characters
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    def run(self):
        # Function to update the text input based on the selected radio button
        def update_text_input():
            selected_option = radio_var.get()

            if selected_option == 1:
                input_var.set(self.generate_passpharse())
            elif selected_option == 2:
                input_var.set(self.generate_password())
            elif selected_option == 3:
                input_var.set("")

        try:
            # if __name__ == "__main__" and not source_paths:
            #     source_paths = [Path(r"C:\Users\Alexander.Oakley\OneDrive - Colonial First State\Desktop\words_pos.csv")]
            if not self.source_paths:
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
            input_var.set(self.generate_passpharse())
            text_input = tk.Entry(root, textvariable=input_var, font=("Arial", 10), width=50)
            text_input.pack()

            # Bind the <FocusIn> event to the text_input widget
            text_input.bind("<FocusIn>", lambda event: radio_var.set(3))

            # Bind the <Return> event to the text_input widget
            text_input.bind("<Return>", lambda event: self.submit_key(radio_var.get(), text_input, self.source_paths, root))

            # Create a button to trigger the dialogue
            dialogue_button = tk.Button(root, text="Submit and copy key to clipboard", command=lambda: self.submit_key(radio_var.get(), text_input, self.source_paths, root), font=("Arial", 10))
            dialogue_button.pack(pady=10)

            # Set the background color of the GUI
            root.configure(bg="#F0F0F0")

            # Start the main GUI loop
            root.mainloop()

            # input("Press Enter to continue...")
        except Exception as e:
            print(e)
            # input("Press Enter to continue...")

