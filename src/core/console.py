from .core import Core
import sys

#TODO: This is temporary, we have to implement config system
def main():
    if len(sys.argv) < 2:
        print("\nNo prefix entered.\n\nExample:\nweBGP 111.222.333.0/24,222.111.333.0/24\n")
    else:
        prefixes = sys.argv[1].strip().split(",")
        Core(prefixes)