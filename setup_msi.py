import sys
from cx_Freeze import setup, Executable
import toml
import os

# ------------------------------------------------------------------
# python setup_msi.py bdist_msi
# ------------------------------------------------------------------

# Build management
DIST_OUTPUT_DIR = "dist"
PYTHON_PROJECT_CONFIG_FILE = r"pyproject.toml"

MAIN_SCRIPT_NAME = "__main__"

# Inputs
PACKAGE_DIR="src/zippy"
SCRIPT_TO_EXECUTE = f'{PACKAGE_DIR}/{MAIN_SCRIPT_NAME}.py'
WORDS_FILE=f"{PACKAGE_DIR}/eff.org_files_2016_07_18_eff_large_wordlist.txt"
COMMON_PASSWORDS_FILE=f"{PACKAGE_DIR}/src/zippy/top-100000-common-passwords.txt"
CONFIG_FILE_PATH=f"{PACKAGE_DIR}/settings.toml"

# Outputs
DISPLAY_NAME='Zippy'
DESCRIPTION="Quickly zip and encrypt files and/or folders"
AUTHOR="Alexander Oakley"
INSTALLER_NAME="zippy"
ICON_PATH=r"assets\Cog-Logo.ico"


def get_version():
    with open(PYTHON_PROJECT_CONFIG_FILE) as f:
        pyproject_toml = toml.load(f)
    return pyproject_toml['project']['version']


def does_version_distribution_exist():
    version:str = get_version()
    return os.path.exists(f'{DIST_OUTPUT_DIR}/{INSTALLER_NAME}-{version}-win64.msi')


def block_if_version_distribution_exists():
    if does_version_distribution_exist():
        raise Exception(
            f"Version distribution already exists." \
            f"Either (1) increment the version number in {PYTHON_PROJECT_CONFIG_FILE}." \
            f"Or (2) delete the existing version distribution {get_version()}." \
            )

block_if_version_distribution_exists()

base = "Win32GUI" if sys.platform == "win32" else None

shortcut_table = [
    ("DesktopShortcut",                 # Shortcut
     "DesktopFolder",                   # Directory_
     DISPLAY_NAME,                      # Name that will be show on the link
     "TARGETDIR",                       # Component_
     f"[TARGETDIR]{MAIN_SCRIPT_NAME}.exe",   # Target exe to exexute
     None,                              # Arguments
     DESCRIPTION,                       # Description
     None,                              # Hotkey
     None,                              # Icon
     None,                              # IconIndex
     None,                              # ShowCmd
     'TARGETDIR'                        # WkDir
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
    "upgrade_code": "{009e6dd7-961b-4c53-bb3c-131508142c8e}",
    "data": msi_data
}

build_exe_options = {
    'replace_paths': [("*", "")],
    "excludes": [ # Any modules that are in your environment that you don't want to include.
        "tomlkit",
        "numpy",
        "pyinstaller",
        "setuptools"
    ],
    'includes': [
        'zippy',
    #   "pystray", "PIL", "os", "threading", 
    #   "json", "datetime", "requests", "numpy", 
    #   "io", "base64", "tkinter", "shutil", "sys", 
    #   "swinlnk", "time"
    ],
    "include_files": [
        # ICON_PATH, 
        # WORDS_FILE, 
        # CONFIG_FILE_PATH
    ],
}

# input("Creating executable settings(?) object")
executables = [
        Executable(
            script=SCRIPT_TO_EXECUTE,
            copyright="Copyright (C) 2023 CFS Autobots",
            base=base,
            icon=ICON_PATH,
        )
    ]
#
# shortcut_name = "MyTime",
# shortcut_dir = "DesktopFolder",

# input("About to call `setup(...)`")
setup(
    # name="cfs_zippy",
    # version="1.0.1",
    # description="Quickly zip and encrypt files and/or folders",
    # author=AUTHOR,
    url="http://autobots.avanteos.com.au/",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    })