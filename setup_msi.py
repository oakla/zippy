import sys
from cx_Freeze import setup, Executable

# ------------------------------------------------------------------
# py build_msi.py bdist_msi
# ------------------------------------------------------------------

DISPLAY_NAME='CFS-Zippy'
DESCRIPTION="Quickly zip and encrypt files and/or folders"
AUTHOR="Alexander Oakley"
SCRIPT_NAME="cfs_zippy"
WORDS_FILE="src/eff.org_files_2016_07_18_eff_large_wordlist.txt"
ICON_PATH=r"assets/icon.ico"

base = "Win32GUI" if sys.platform == "win32" else None

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     DISPLAY_NAME,                  # Name that will be show on the link
     "TARGETDIR",              # Component_
     f"[TARGETDIR]{SCRIPT_NAME}.exe",# Target exe to exexute
     None,                     # Arguments
     DESCRIPTION,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]


msi_data = {
    "Shortcut": shortcut_table,
    }

bdist_msi_options = {
    "summary_data": {
        "author": AUTHOR,
        "comments": DESCRIPTION
    },
    "install_icon": ICON_PATH,
    "upgrade_code": "{12345678-0987-1234-0987-123456789098}",
    "data": msi_data
}

build_exe_options = {
    'replace_paths': [("*", "")],
    "excludes": [],
    # 'includes': ["pystray", "PIL", "os", "threading", "json", "datetime", "requests", "numpy", "io", "base64", "tkinter", "shutil", "sys", "swinlnk", "time"],
    "include_files": ["assets/icon.ico", WORDS_FILE]
}

executables = [
        Executable(
            script=f"src/{SCRIPT_NAME}.py",
            copyright="Copyright (C) 2023 CFS Autobots",
            base=base,
            icon=ICON_PATH,
        )
    ]
#
# shortcut_name = "MyTime",
# shortcut_dir = "DesktopFolder",

setup(
    name="cfs_zippy",
    version="1.0.1",
    description="Submit current activity for reporting purposes",
    author=AUTHOR,
    url="http://autobots.avanteos.com.au/",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    })