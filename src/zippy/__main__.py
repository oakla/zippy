from zippy.core import Zippy
import argparse
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def get_source_paths():
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument("source_paths", nargs='*', help="input file or folder")
        args = parser.parse_args()
        source_paths = [Path(arg) for arg in args.source_paths]
    except Exception as e:
        logger.critical(f"Error while reading initial program input: {e}")
        exit()
    return source_paths

Zippy(
    source_paths=get_source_paths()
    ).run()