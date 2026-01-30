import sys
import os
from pathlib import Path
import zlib

from app.classes.GitObject import GitObject


def main():
    print("Logs from your program will appear here!", file=sys.stderr)


    command = sys.argv[1] #returns list of arguments
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":

        # cat file is used to view the type of an object, it's size and its content
        # cat file takes 2 arguments, a flag and its hash
        # we need to find the blob in our objects directory

        flag = sys.argv[2]
        hash = sys.argv[3]

        folder = hash[:2] # folder is the first 2 digits of the hash

        file_name = hash[2:] #everything else is the file name


        file_path = Path(".git/objects") / folder / file_name

        with open(file_path, "rb") as f: # rb stands for read binary, returns data as bytes instead of string
            compressed_bytes = f.read()

            _, content = GitObject.deserialize(compressed_bytes)

            sys.stdout.buffer.write(content)

    else:
        raise RuntimeError(f"Unknown command #{command}")



if __name__ == "__main__":
    main()
