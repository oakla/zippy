"""
- Substitute the package name in the files that have the placeholder name $src-template.
- Remove comments from pyproject.toml 
- Delete the files 
    - setup.cfg
    - MANIFEST.in
    - pyproject-uncommented.toml
    - src/$src-template/data_files/example.txt
    - src/$src-template/another_data_file.html
    - src/$src-template/example2.json
"""
import os
from sys import argv

DEFAULT_PACKAGE_NAME = 'my_package'

if len(argv) > 1:
    package_name = argv[1]
else:
    package_name = input('Enter package name: ')
    if not package_name:
        package_name = DEFAULT_PACKAGE_NAME

FILES_TO_DELETE = [
    'setup.cfg',
    'MANIFEST.in',
    'pyproject-uncommented.toml',
    fr"src\{package_name}\data_files\example.txt",
    fr"src\{package_name}\another_data_file.html",
    fr"src\{package_name}\example2.json",
]

DIRS_TO_DELETE = [
    f'src\\{package_name}\\data_files',
]

def clean_pyproject_toml():
    with open('pyproject-uncommented.toml', 'r') as f:
        content = f.read()
    os.remove('pyproject-uncommented.toml')
    with open('pyproject.toml', 'w') as f:
        f.write(content)
    replace_place_holder_name_in_file('pyproject.toml', package_name)

def rename_top_level_module_folder():
    # rename directory
    os.rename('src/$src-template', f'src/{package_name}')

def replace_place_holder_name_in_file(file_name, new_string):
    with open(file_name, 'r') as f:
        content = f.read()
    content = content.replace('$src-template', new_string)
    with open(file_name, 'w') as f:
        f.write(content)

with open('README.md', 'w') as f:
    f.write(f'# {package_name}\n')

clean_pyproject_toml()
rename_top_level_module_folder()

for file_name in FILES_TO_DELETE:
    os.remove(file_name)

for dir_name in DIRS_TO_DELETE:
    # Check if dir is empyt
    dir_contents = os.listdir(dir_name)
    if not dir_contents:
        os.rmdir(dir_name)

# delete this file (the file you're looking at right now)
os.remove('clean.py')