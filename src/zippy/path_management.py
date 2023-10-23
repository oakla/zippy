from pathlib import Path

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
    


# ====================================
# None of the below are used right now
from tkinter import filedialog, messagebox
from zippy.settings import Settings
# Function to ask for a file path
def ask_for_file(self):
    file_path = filedialog.askopenfilename()
    if file_path:
        return file_path
    else:
        return None

def ask_for_winzip_cli_path(self, expected_path=""):
    messagebox.showinfo(
        "Error", 
        f"WinZip CLI was not found at the expected path.\n\n"
            + "A file selection dialogue will appear after you close this message box. You will then have two options.\n\n" \
            "1) If you know the path to `wzzip.exe` on your machine, select it, then hit 'Open'.\n\n" \
            "2) If you do NOT know the path to `wzzip.exe` on your machine, just hit 'Cancel'.\n\n" \
            f"The expected path is {expected_path}.\n\n" \
            f"You can view and edit the saved paths in the config file at {Settings.config_file_path}.\n\n" \
            )

    return self.ask_for_file()

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