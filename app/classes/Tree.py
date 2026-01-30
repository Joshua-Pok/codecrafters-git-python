from app.classes.GitObject import GitObject
from typing import List
from dataclasses import dataclass


# Index is flat, there is no sense of structure.
# Tree class gives it the structure


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    name: str
    oid: str


class Tree(GitObject):
    def __init__ (self, entries: List[TreeEntry]):
        self.entries = entries
        content = self._build_content(entries)
        super().__init__('tree', content)


    @staticmethod
    def _build_content(entries: List[TreeEntry]) -> bytes:
        entries_sorted = sorted(entries, key=lambda e: e.name)

        out = b""
        for e in entries_sorted:
            out += f"{e.mode} {e.name}".encode() + b"\0" + bytes.fromhex(e.oid)

        return out


# A tree has multiple "entries". Each entry includes a SHA-1 Hash that points to a blob or tree object.

# Each entry also has the name of the file/directory

# each entry also has the mode (or permissions) or the file/directory

# A tree is a snapshot of the current directory at the time of commit. It simply lists the hashes of files and subtrees in the directory


# A tree's content is just all its entries stuc together

# b"100644 README.md\0" + <20 raw bytes of blob hash>
# b"40000 src\0"       + <20 raw bytes of tree hash>

# join all together and thats the content for the tree


