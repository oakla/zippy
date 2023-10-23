from zippy import Zippy
from pathlib import Path

source_paths=[
    r"C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\.gitignore"
]

Zippy([Path(x) for x in source_paths]).run()