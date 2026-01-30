from app.classes.GitObject import GitObject

class Blob(GitObject):
    def __init__(self, content: bytes):
        super().__init__("Blob", content)


# a blob is nothing more than some bytes











