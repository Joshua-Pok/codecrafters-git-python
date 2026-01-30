import hashlib
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


    elif command == "hash-object":

        # hash object is used to compute the sha1 hash of an object
        # when used with the -w flag it needs to also write the object to the git/objects directory

        flag = sys.argv[2]
        file_name = sys.argv[3]

        with open(file_name, "rb") as f:
            file_bytes = f.read()

            # serialize the file
            length = str(len(file_bytes)).encode()
            content = 'blob'.encode() + " ".encode() + length + b"\0" + file_bytes
            compressed_content = zlib.compress(content)


            hash = hashlib.sha1(content).hexdigest()


            if flag == "-w":
                folder = hash[:2]
                newfile_name = hash[2:]

                file_path = Path(".git/objects") / folder / newfile_name


                file_path.parent.mkdir(parents=True, exist_ok=True) # create parent folders if necessary

                file_path.write_bytes(compressed_content)


            print(hash)


    else:
        raise RuntimeError(f"Unknown command #{command}")



if __name__ == "__main__":
    main()
