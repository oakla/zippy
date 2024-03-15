import tkinter as tk
from tkinter import font
from tkinter import ttk
import string
import random
import pyperclip
from typing import Optional


BEST_PRACTICE = False

DEFAULT_FONT = {}
# DEFAULT_FONT["family"] = "Arial"
DEFAULT_FONT["family"] = "Calibri"
# DEFAULT_FONT["family"] = "Segoe UI"
DEFAULT_FONT["size"] = 12

HEADING_FONT = {}
HEADING_FONT["family"] = "Calibri"
HEADING_FONT["size"] = 16
# HEADING_FONT['weight'] = "bold"
# HEADING_FONT['underline'] = 1


class ListFrame(tk.Frame):

    def __init__(self, parent, list_prelude: str = "") -> None:
        super().__init__(parent, width=400)
        
        label_prelude = tk.Label(self, text=list_prelude)
        label_prelude.grid(column=0, row=0, sticky=tk.W, padx=3, pady=5, columnspan=2)

        self.current_row_index = 1

    def add_list_item(self, text, bullet_point="\u2022"):

        label_bullet = tk.Label(self, text=f"{bullet_point}  ", width=5)
        label_bullet.grid(column=0, row=self.current_row_index, sticky=tk.NW)

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
        frame_list.grid(column=0, row=2, padx=15 , pady=15)

        for instruction_item in list_items:
            frame_list.add_list_item(
                text=instruction_item[1], bullet_point=instruction_item[0]
            )


class InstructionsSectionFrame(NotebookSectionFrame):

    def __init__(self, parent=None,) -> None:

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

        self.phrase_phrase_words = [
            "mainframe",
            "columnconfigure",
            "rowconfigure",
            "StringVar",
            "Button",
            "Label",
            "feet_entry",
            "root",
        ]

        self.secure_key = tk.StringVar()
        self.secure_key.trace_add("write", self.update_password_warning)
        # frame_guidelines = GuidelinesFrame(self)
        # frame_guidelines.grid(column=0, row=0)

        # Text Entry
        entry_password = ttk.Entry(
            self,
            width=60,
            textvariable=self.secure_key,
            font=("Arial", 12),
        )
        entry_password.grid(
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
        if BEST_PRACTICE:
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
        password = "".join(random.choice(characters) for i in range(length))
        return password

    def generate_passphrase(self, k_words=5):
        passpharse = []
        for _ in range(k_words):
            passpharse.append(random.choice(self.phrase_phrase_words))
        return " ".join(passpharse)

    def get_secure_key(self):
        return self.secure_key.get()


class ZippyGui:

    def __init__(self):

        self.secure_key = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Frame Scratch")
        # root.geometry("400x400")

        tk_default_font = font.nametofont("TkDefaultFont")
        tk_default_font.config(**DEFAULT_FONT)

        tk_heading_font = font.nametofont("TkHeadingFont")
        tk_heading_font.config(**HEADING_FONT)

        # Create a notebook to hold the frames
        notebook = ttk.Notebook(self.root, padding="3 3 12 12", style="TNotebook")
        notebook.grid(column=0, row=0)
        notebook.enable_traversal()

        # !
        # TODO: connect secure_key to clipboard and zip process path
        # TODO: connect destroy command to submit button
        # Add the frames to the notebook
        notebook.add(GuidelinesFrame(), text="Guidelines")
        notebook.add(InstructionsSectionFrame(), text="Instructions")
        notebook.add(self.create_about_frame(), text="About")

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

    def create_about_frame(self) -> tk.Frame:
        about_frame = tk.Frame()

        return about_frame

    def create_instrutions_frame(self) -> tk.Frame:
        instructions_frame = tk.Frame()

        return instructions_frame

    def submit_secure_key(self):
        if not self.password_choice_frame.is_secure_key_valid():
            return
        
        self.secure_key = self.password_choice_frame.get_secure_key()
        pyperclip.copy(self.secure_key)
        self.root.destroy()


if __name__ == "__main__":
    gui = ZippyGui()
    print(gui.secure_key)
