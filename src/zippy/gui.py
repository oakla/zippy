import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
import string
import random
import pyperclip
from typing import Optional
import logging
from zippy.settings import Settings
from zippy import path_management

logger = logging.getLogger(__name__)


class ListFrame(tk.Frame):

    def __init__(self, parent, list_prelude: str = "") -> None:
        super().__init__(parent, width=400)

        label_prelude = tk.Label(self, text=list_prelude)
        label_prelude.grid(column=0, row=0, sticky=tk.W, padx=3, pady=5, columnspan=2)

        self.current_row_index = 1

    def add_list_item(self, text, bullet_point="\u2022", bullet_width=5):

        label_bullet = tk.Label(self, text=f"{bullet_point}  ", width=bullet_width, justify=tk.RIGHT, anchor=tk.E)
        label_bullet.grid(column=0, row=self.current_row_index, sticky=tk.NE,)

        label_item_text = tk.Label(self, text=text, wraplength=500, justify=tk.LEFT)
        label_item_text.grid(column=1, row=self.current_row_index, sticky=tk.NW)

        self.current_row_index += 1


class NotebookSectionFrame(tk.Frame):

    def __init__(
        self,
        parent=None,
        heading: str = "",
        list_prelude: str = "",
        list_items: list[tuple[str, str]] = Optional[None],  # type: ignore
    ) -> None:

        super().__init__(master=parent)

        label_heading = tk.Label(self, text=heading)
        label_heading["font"] = "TkHeadingFont"
        label_heading.grid(column=0, row=0, padx=5, pady=10)

        frame_list = ListFrame(self, list_prelude=list_prelude)
        frame_list.grid(column=0, row=2, padx=15, pady=15)

        for instruction_item in list_items:
            frame_list.add_list_item(
                text=instruction_item[1], bullet_point=instruction_item[0], 
            )


class AboutSectionFrame(tk.Frame):

    def __init__(
        self,
        parent=None,
    ) -> None:
        about_heading_text = "📜 About Zippy"

        about_items_prelude = ""

        about_items = [
            (
                "What is Zippy:",
                "Zippy is a utility to help quickly zip and encrypt files and/or folders.",
            ),
            (
                "Version:",
                "1.2.0",
            ),
            (   
                "Project Source Code:",
                "https://github.com/CFSCo-Automation/Zippy"
            ),
            (
                "Author:",
                "Alex Oakley",
            ),
        ]

        super().__init__(
            master=parent,
        )

        label_heading = tk.Label(self, text=about_heading_text)
        label_heading["font"] = "TkHeadingFont"
        label_heading.grid(column=0, row=0, padx=5, pady=10)

        frame_list = ListFrame(self, list_prelude=about_items_prelude)
        frame_list.grid(column=0, row=2, padx=15, pady=15)

        for instruction_item in about_items:
            frame_list.add_list_item(
                text=instruction_item[1], bullet_point=instruction_item[0], bullet_width=20
            )


class InstructionsSectionFrame(NotebookSectionFrame):

    def __init__(
        self,
        parent=None,
    ) -> None:

        instructions_heading_text = "📜 How to use Zippy"

        instructions_items_prelude = "Steps: "

        instructions_items = [
            ("1.", "Drag and drop a file or folder onto the icon on your desktop."),
            (
                "2.",
                "(Optional) Click 'Generate password' to generate a random password.",
            ),
            ("3.", "Edit the password as required."),
            (
                "4.",
                "Click 'Submit' to zip your files and encrypt them. You will find the new zip file on your desktop.",
            ),
            ("5.", "The password you chose will be copied to your clipboard."),
        ]

        super().__init__(
            parent=parent,
            heading=instructions_heading_text,
            list_prelude=instructions_items_prelude,
            list_items=instructions_items,
        )


class GuidelinesFrame(NotebookSectionFrame):

    def __init__(self, parent=None) -> None:

        guidlines_heading_text = "📜 CFS Password Guidelines"

        guidelines_prelude = "Passwords should ideally:"

        guideline_items = [
            ("📏", "be a minimum of 14 characters long,"),
            ("🎲", "be generated randomly,"),
            ("📕", "not use dictionary words,"),
            ("🔤", "contain upper case, lower case, numbers and special characters."),
        ]

        super().__init__(
            parent=parent,
            heading=guidlines_heading_text,
            list_prelude=guidelines_prelude,
            list_items=guideline_items,
        )


class PasswordChoiceFrame(tk.Frame):

    def __init__(self, parent=None) -> None:
        
        super().__init__(parent)

        label_warning = tk.Label(
            self,
            text="",
            fg="red",
        )
        label_warning.grid(column=0, row=3)
        self.warning_contents = tk.StringVar()
        self.warning_contents.set("")
        label_warning["textvariable"] = self.warning_contents

        self.secure_key = tk.StringVar()
        self.secure_key.trace_add("write", self.update_password_warning)

        # Text Entry
        self.entry_password = ttk.Entry(
            self,
            width=60,
            textvariable=self.secure_key,
            font=("Segoe UI", 12),
        )
        self.entry_password.grid(
            column=0,
            row=2,
            # sticky=(tk.W, tk.E), # type: ignore
            padx=3,
            pady=5,
        )

        # Generate Random Password
        button_generate_random = ttk.Button(
            master=self,
            text="Generate password",
            command=self.update_with_random_password,
        )
        button_generate_random.grid(
            column=0,
            row=4,
            # sticky=tk.W
            pady=3,
        )

        # Generate Random Passphrase
        if Settings.best_practice():
            button_generate_passphrase = ttk.Button(
                master=self,
                text="Generate passphrase",
                command=self.update_with_random_passphrase,
            )
            button_generate_passphrase.grid(
                column=0,
                row=5,
                # sticky=tk.W
                pady=3,
            )

        self.generate_random_password()

    def update_password_warning(self, *args):
        if self.is_secure_key_valid():
            self.warning_contents.set("")
        else:
            self.warning_contents.set("Password must be at least 8 characters long.")


    def is_secure_key_valid(self):
        current_secure_key_text = self.secure_key.get()
        if len(current_secure_key_text) < 8:
            return False
        return True


    def update_with_random_password(self):
        secure_key = self.generate_random_password()
        self.secure_key.set(secure_key)


    def update_with_random_passphrase(self):
        secure_key = self.generate_passphrase()
        self.secure_key.set(secure_key)


    def generate_random_password(self, length: int = 14):
        special_characters = "!@#$%^&*()_+?"

        characters = string.ascii_letters + string.digits + special_characters
        password = "".join(random.choice(characters) for _ in range(length))
        return password


    def get_phrase_word_list(self):
        try:
            logger.debug(
                f"Attempting to open and read words file ({path_management.words_file_path})."
            )
            with open(path_management.words_file_path, "r") as fp:
                phrase_words = [
                    x.split("\t")[1] for x in fp.read().splitlines() if len(x) > 1
                ]
        except Exception as e:
            logger.critical(
                f"Error while opening 'word file' expected at {path_management.words_file_path}: {e}"
            )

        return phrase_words


    def generate_passphrase(self, k_words=5):
        self.phrase_words = self.get_phrase_word_list()
        passpharse = []
        for _ in range(k_words):
            passpharse.append(random.choice(self.phrase_words))
        return " ".join(passpharse)


    def get_secure_key(self):
        return self.secure_key.get()


class ZippyGui:

    def __init__(self):

        self.secure_key = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Zippy")
        # root.geometry("400x400")

        tk_default_font = font.nametofont("TkDefaultFont")
        config_dict = Settings.load_setting_dict()
        tk_default_font.config(**config_dict["default_font"])

        tk_heading_font = font.nametofont("TkHeadingFont")
        tk_heading_font.config(**config_dict["heading_font"])

        # Create a notebook to hold the frames
        notebook = ttk.Notebook(self.root, padding="3 3 12 12", style="TNotebook")
        notebook.grid(column=0, row=0)
        notebook.enable_traversal()

        # Add the frames to the notebook
        notebook.add(GuidelinesFrame(), text="Guidelines")
        notebook.add(InstructionsSectionFrame(), text="Instructions")
        notebook.add(AboutSectionFrame(), text="About")

        style = ttk.Style()
        style.configure(
            "TNotebook.Tab",
            # background="#808080",
            # foreground="blue",
            padding=3,
        )

        self.password_choice_frame = PasswordChoiceFrame(
            # padding="3 3 12 12"
        )
        self.password_choice_frame.grid(column=0, row=1)

        # Submit Button
        button_submit = ttk.Button(master=self.root, text="Submit", command=self.submit_secure_key)  # type: ignore
        button_submit.grid(column=0, row=5, sticky=tk.E, padx=6, pady=6)

        self.root.mainloop()


    def create_instrutions_frame(self) -> tk.Frame:
        instructions_frame = tk.Frame()

        return instructions_frame

    def submit_secure_key(self):
        if not self.password_choice_frame.is_secure_key_valid():
            self.password_choice_frame.update_password_warning()
            return

        secure_key = self.password_choice_frame.get_secure_key()
        # if self.is_common_password(secure_key):
        #     self.show_common_password_warning()
        self.close_zippy_gui(secure_key)


    # def show_common_password_warning(self):
    #     messagebox.Message(
    #         master=self.root,
    #         text="Password Warning",
    #         message="Consider choosing a different password",
    #         details="Your password is included in a list of the 100,000 most commonly used passwords, and therefore is easily crackable.",
    #         icon=messagebox.WARNING,
    #     )

    def close_zippy_gui(self, secure_key) -> None:
        pyperclip.copy(secure_key)
        self.secure_key = secure_key
        self.root.destroy()


    def is_common_password(self, secure_key):
        with open(path_management.common_passwords_file_path, "r") as fp:
            bad_passwords = [x.strip() for x in fp.readlines()]
        return secure_key in bad_passwords


if __name__ == "__main__":
    gui = ZippyGui()
    print(gui.secure_key)
