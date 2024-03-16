"""take input file or folder as argument
ask for password or generate one
zip input file or folder to a pre-defined location"""

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
from zippy import path_management
import logging
from zippy import gui

logger = logging.getLogger(__name__)


class Zippy:

    def __init__(
        self,
    ):

        self.ensure_winzip_cli_path_exists()

    def ensure_winzip_cli_path_exists(self):
        if not Path(Settings.winzip_cli_path()).exists():
            logger.error(f"WinZip CLI executable was not found.")
            # Might be wise to use PyZip instead of WinZip
            self.show_error_message(
                f"The WinZip CLI executbale was not found at the expected path: {path_management.config_file_path}.\n\n"
                f"You can view and edit the expected path in the config file at {path_management.config_file_path}.\n\n"
                f'Note that the WinZip CLI executbale is distinct from the WinZip GUI executable which is usually called "WZZIP.EXE"'
            )

    def show_error_message(self, message: str):
        messagebox.showinfo("Error", message)

    def get_destination_path(
        self,
        source_paths: list[Path],
        dest_path_parent: Optional[Path] = None,
        to_desktop: bool = True,
    ) -> Union[Path, None]:
        """
        Two options:
        - Send to desktop (default)
        - Send to the parent folder
        """
        logger.debug(f"Determining output path")
        if to_desktop:
            logger.debug(f"Program config indicates output should go to Desktop")
            output_path_parent = Path(
                os.path.join(
                    os.path.join(os.environ["USERPROFILE"]),
                    "OneDrive - Colonial First State",
                    "Desktop",
                )
            )
        elif dest_path_parent is not None:
            output_path_parent = dest_path_parent
        else:
            output_path_parent = source_paths[0].parent

        if len(source_paths) > 1:
            output_file_name = "zip_file"
        elif len(source_paths) == 1:
            output_file_name = source_paths[0].name
        else:
            print("Something went wrong. No source files were provided.")
            return None

        logger.info(f"output parent will be {output_path_parent}")
        return path_management.uniquify(
            (output_path_parent / output_file_name).with_suffix(".zip")
        )

    def notify_zip_failed(self, explanation: Optional[str] = None):
        if not explanation:
            explanation = "Zip command did not exectute successfully."
        messagebox.showinfo("Zip didn't happen.", explanation)

    def run(
        self,
        source_paths: list[Path],
        dest_path_parent: Optional[Path] = None,
        to_desktop: bool = True,
    ):

        dest_path_parent = self.get_destination_path(
            source_paths, to_desktop=to_desktop, dest_path_parent=dest_path_parent
        )
        logger.info(f"Zip output will be written to {dest_path_parent}")
        if not to_desktop and dest_path_parent is None:
            logger.warning(f"Zip output path came back as None.")
            self.notify_zip_failed("Failed to get output path.")
            return

        password_selection_gui = gui.ZippyGui()
        secure_key = password_selection_gui.secure_key
        # print(secure_key)
        if secure_key is None:
            self.notify_zip_failed("No password was submitted.")
            return
        if len(secure_key) < 8:
            self.notify_zip_failed("Password must be at least 8 characters long.")
            return
        
        self.make_zip_file(source_paths, secure_key, dest_path_parent)

    def make_zip_file(
        self, source_paths: list[Path], secure_key="", dest_path: Optional[Path] = None
    ):

        if not source_paths:
            self.notify_zip_failed(
                "No source files were provided.\n\nTry drag and drop a file onto the Zippy shortcut icon."
            )
            return
        logging.debug(f"Source paths to be zipped are {source_paths}")

        logger.info(f"{secure_key=}")
        logger.info(f"{source_paths=}")
        logger.info(f"{dest_path=}")
        commands = [Settings.winzip_cli_path()] + [dest_path]
        if secure_key:
            escaped_secure_key = self.add_escapes_for_special_characters(secure_key)
            logger.info(f"{escaped_secure_key=}")
            commands.append(f"-s{escaped_secure_key}")
            commands.append("-yc")  # Use AES Encryption

        commands += source_paths

        logger.debug(f"Calling `subprocess.run(...) with: {commands}")
        completed_process = subprocess.run(
            commands, shell=True, capture_output=True, text=True
        )

        returncode = completed_process.returncode
        stdout = completed_process.stdout
        stderr = completed_process.stderr

        logger.debug("subprocess complete.")

        # check completed process
        if completed_process.returncode == 0:
            logger.debug(f"returncode == `{returncode=}`")
            logger.debug(f"stdout == `{stdout=}`")
            logger.debug(f"stderr == `{stderr=}`")
            return
        else:
            logger.critical(f"subprocess completed with returncode NOT equal to 0")
            logger.critical(f"{returncode=}")
            logger.critical(f"{stderr=}")
            logger.critical(f"{stdout=}")
            self.notify_zip_failed(
                f"Zip command did not exectute successfully.\n\n Error message: {completed_process.stdout}"
            )
            return


    def add_escapes_for_special_characters(self, unescaped_string:str) -> str:
        
        windows_reservered_characters = [    
            "^", # The '^' must be first so that other escapes don't get escaped
            "&", 
            "|", 
            # "(", 
            # ")", 
            "<", 
            ">", 
        ]
        windows_escape_character = "^"

        escaped_string = unescaped_string
        for c in windows_reservered_characters:
            escaped_string = escaped_string.replace(c, windows_escape_character + c)

        return escaped_string