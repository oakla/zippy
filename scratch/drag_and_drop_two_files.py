import argparse
from ast import parse


parser = argparse.ArgumentParser()
parser.add_argument("source_path", nargs='+', help="input file or folder")
args = parser.parse_args()

print(f"{type(args.source_path)=}")
print(f"{args.source_path=}")


input("Press Enter to continue...")