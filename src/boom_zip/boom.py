import argparse
from operator import is_
import subprocess
import os
from pathlib import Path

def uniquify(path:Path, counter:int=1):
    """
    If the path exists, append a number to it to make it unique.
    """
    if not path.exists():
        return path
    if path.is_file():
        path = path.with_name(path.stem + "(" +str(counter) + ")" + path.suffix)
        return uniquify(path, counter+1)
    if path.is_dir():
        path = path + "(" +str(counter) + ")"
        return uniquify(path, counter+1)
    return path

def infer_dest_path_from_source(source_path:Path):
    """
    If the source is a file, return a path to a file with the same name in the same folder.
    If the source is a folder, return a path to a file with the same name in the parent folder.
    """
    if source_path.is_file():
        return uniquify(source_path.with_suffix('.zip'))
    if source_path.is_dir():
        return uniquify(source_path.parent / (source_path.name + '.zip'))

WINZIP_PATH = r"c:\program files\winzip\wzzip"
TO_ZIP = r'C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\scratch\output\test_zip.zip'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", help="input file or folder")
    # parser.add_argument("-p", "--password", help="password for zip file")
    args = parser.parse_args()
    source_path = Path(args.source_path)
    # print(args.password)
    dest_path = uniquify(infer_dest_path_from_source(source_path))
    print(f"source_path: {source_path}")
    print(f"dest_path: {dest_path}")
    zip(source_path, dest_path)


def zip(source_path, dest_path):
        subprocess.run([
        WINZIP_PATH, dest_path, source_path
    ], shell=True)


main()
input("Press Enter to continue...")
# take input file or folder as argument

# pass that argument to the zip function

# ask for password or generate one

# zip function will create a zip file with the same name as the input file or folder