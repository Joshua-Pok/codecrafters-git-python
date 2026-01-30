# Git Index: Staging area or where stuff goes when we git add .


# Index stores a list of entries in a key value format
# path : indexfile


from typing import TypedDict, List
from pathlib import Path
import json


class IndexEntry(TypedDict):
    path: str
    oid: str

class IndexFile(TypedDict):
    version: int
    entries: List[IndexEntry]


INDEX_PATH = Path(".git") / "index"


def read_index() -> IndexFile:

    if not INDEX_PATH.exists():
        return {"version": 1, "entries": []} # if index does not exist we return an empty index


    raw_index = INDEX_PATH.read_text(encoding="utf-8").strip() # returns json string


    data = json.loads(raw_index) # json.loads() converts a json formatted string into a python object


    return data



def write_index(file: IndexFile) -> None:
    # json.dumps() serializes a python object into a json formatted string

    raw_index = json.dumps(file)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    INDEX_PATH.write_bytes(raw_index.encode())


    



