from zippy import Zippy
from pathlib import Path
from zippy import path_management
import logging


source_paths=[
    r"test\inputs\a file with spaces.txt"
]

outpath_parent = path_management.uniquify(Path(r"test\outputs\output"))
outpath_parent.mkdir()

Zippy().run([Path(x) for x in source_paths], outpath_parent, to_desktop=False, )