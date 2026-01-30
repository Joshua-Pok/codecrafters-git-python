import hashlib
import sys
import os
from pathlib import Path
import zlib

from app.classes.GitObject import GitObject
from typing import Dict, Any, Tuple, List
from app.classes.Index import IndexFile

from app.classes.Tree import TreeEntry
from app.classes.Tree import Tree


def write_object(obj: GitObject) -> str:
    oid = obj.hash

    obj_path = Path(".git") / "objects" / oid[:2] / oid[2:]

    obj_path.parent.mkdir(parents=True, exist_ok=True)

    obj_path.write_bytes(obj.compress())

    return oid


def write_tree_from_index(index: IndexFile) -> str:

    root: Dict[str, Any] = {}

    for entry in index["entries"]:
        path = entry["path"]
        oid = entry["oid"]

        parts = path.split("/") # returns a list of parts

        curr = root

        for part in parts[:-1]: # for all elements except the last, these are all guranteed to be folders
            if part not in curr:
                curr[part] = {} # create the trie like structure
            curr = curr[part]
        curr[parts[-1]] = oid # set the value of the file to be its hash


    def write_node(node: Dict[str, Any]) -> str: # walk the trie from  bottom up and build the git tree object
        entries: List[TreeEntry] = [] # where we build the entries

        for name, value in node.items():
            if isinstance(value, dict): #if it is the folder
                child_tree_oid = write_node(value) # recursively build the tree for this folder
                entries.append(TreeEntry(mode='40000',name=name, oid=child_tree_oid))
            else:
                entries.append(TreeEntry(mode='100644', name=name, oid=value))

        tree_obj = Tree(entries)
        return write_object(tree_obj)


    return write_node(root)

def parseTreeContent(content: bytes) -> List[Tuple[str, str, str]]:
    entries: List[Tuple[str, str, str]] = []
    i = 0

    while i < len(content):
        space_idx = content.find(b" ", i)
        if space_idx == -1:
            raise ValueError("Corrupt tree: could not find space")
        mode = content[i:space_idx].decode("utf-8")
        null_idx = content.find(b"\0",space_idx + 1)
        name = content[space_idx + 1: null_idx].decode("utf-8")


        oid_start = null_idx + 1
        oid_end = oid_start + 20


        if oid_end > len(content):
            raise ValueError("Corrupt Tree: Incomplete OID")

        oid_hex = content[oid_start: oid_end].hex()
        entries.append((mode, name, oid_hex))
        i = oid_end


    return entries






def main():
    print("Logs from your program will appear here!", file=sys.stderr)


    command = sys.argv[1] #returns list of arguments
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        with open(".git/index", "wb") as f:
            pass
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


    elif command == "ls-tree":
        flag = sys.argv[2]
        hash = sys.argv[3]


        if flag == "--name-only":

            tree_path = Path(".git/objects") / hash[:2] / hash[2:]

            compressed_bytes = tree_path.read_bytes()

            obj_type, content = GitObject.deserialize(compressed_bytes)


            if obj_type != "tree":
                raise ValueError(f"{hash} is not a tree")

            entries = parseTreeContent(content)

            for _, name, _ in sorted(entries, key=lambda t: t[1]):
                print(name)

        else:
            pass # not implemented yet


    else:
        raise RuntimeError(f"Unknown command #{command}")



if __name__ == "__main__":
    main()
