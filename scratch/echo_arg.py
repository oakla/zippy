import sys
input("Press Enter to continue...")
try:
    print(sys.argv[1])
except IndexError:
    print("Usage: python3 echo_arg.py <arg1> <arg2> ...")
    # sys.exit(1)

input("Press Enter to continue...")