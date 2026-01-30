# Structure of a commit
# commit <size>\0tree <tree_sha>
# parent <parent_sha>
# author <name> <<email>> <timestamp> <timezone>
# committer <name> <<email>> <timestamp> <timezone>
# <empty line>
# <commit message>

# Commit needs to know what branch it is on, what parent commit is


from app.classes.GitObject import GitObject
from typing import List
import time

class Commit(GitObject):
    def __init__ (self, tree_hash: str, parent_hash: List[str], author: str, committer: str, message: str, timestamp: int):
        # parent_hash is a list of strings because a commit can have multiple parents (eg: merge commits)
        self.tree_hash = tree_hash
        self.parent_hashes = parent_hash
        self.author = author
        self.committer = committer 
        self.timestamp = timestamp or time.time()
        self.message = message
        content = self.serialize_commit()
        super().__init__('commit', content)


    def serialize_commit(self): #serializes commit in the structure stated above

        lines = [f"tree {self.tree_hash}"]
        for parent in self.parent_hashes:
            lines.append(f"parent {parent}")

        lines.append(f"author {self.author} {self.timestamp} + 0000")
        lines.append(f"committer {self.committer} {self.timestamp} + 0000")
        lines.append("")
        lines.append(self.message)


        return "\n".join(lines).encode()


    @classmethod
    def deserialize_commit(cls, content: bytes) -> Commit:
        lines = content.decode().split("\n") # get back original string


        tree_hash = None
        parent_hashes = []
        author = None
        committer = None
        message_start = 0


        for i, line in enumerate(lines, start=1): # for each line
            if line.startswith("tree "):
                tree_hash = line[5:]
            elif line.startswith("parent "):
                parent_hashes.append(line[7:])
            elif line.startswith("author "):
                author_parts = line[7:].rsplit(" ", 2) # returns a list of words using a delimiter
                author = author_parts[0]
                timestamp = int(author_parts[1])
            elif line.startswith("committer "):
                committer_parts = line[10:].rsplit(" ", 2)
                committer = committer_parts[0]

            elif line == "":
                message_start = i + 1
                break


        message = "\n".join(lines[message_start:])

            # if i == 1: #commit line
            #     null_idx = line.find(b"\0")
            #     commit_portion = line[:null_idx]
            #     tree_portion = line[null_idx + 1:]
            #
            #
            #     commit = commit_portion.split()[1] #split by whitesspace take the second value
            #     tree = tree_portion.split()[1]
            #
            # if i == 2:
            #     parent_hash = line.split()[1]
            #
            #
            # if i == 3:
            #     author = line.split()[1]
            #     timestamp = line.split()[2]
            #
            #
            # if i == 4:
            #     commiter = line.split()[1]
            #
            # if i == 5:
            #     message = line
            #

        commit_obj = cls(tree_hash, parent_hashes, author, committer, message, timestamp)


        return commit_obj







        
