"""
This module is the default starting point of your package after installation.

Feel free to delete the contents of this file and start from scratch.
"""

import sys
# importlib_resources is a backport of importlib.resources which provides
# the newest features of importlib.resources to older Python versions.

# You could just use importlib_resources regardless of the Python version.
# Go ahead and change it, but remember to update the dependencies list.
if sys.version_info >= (3, 10):
    from importlib.resources import files
else: 
    from importlib_resources import files


#* Below is a demonstration of accessing datafiles at runtime.
# Read text from a file
example_text = files('pkgname.data_files').joinpath('example.txt').read_text()
print(example_text)

# Read binary data from a file
import json
example_map = json.loads(files('pkgname').joinpath('example2.json').read_bytes())
print(f"Hello {example_map['Hello']} from json file\n")

example_path = files('pkgname').joinpath('another_data_file.html')
print(f"html file path is {example_path}")

# In some cases you may need to make changes to the config files and/or
# use a MANIFEST.in file to include additional files.
# https://setuptools.pypa.io/en/latest/userguide/datafiles.html#data-files-support 