# All git objects are identifiable by a 40 character SHA1 hash.
import hashlib
import zlib

class GitObject:

    # type: blob, commit, tree
    def __init__(self, obj_type: str, content: bytes):
        self.type = obj_type
        self.content = content
        self.hash = self.compute_hash()
         



    def serialize(self) -> bytes:

        length = str(len(self.content)).encode()
        # we need evrything in bytes before we can serialize it
        to_be_compressed = self.type.encode() + " ".encode() + length + b"\0"  + self.content

        return to_be_compressed



    def compress(self) -> bytes:
        return zlib.compress(self.serialize())



    # we only call deserialize to deserialize a hash into its contents, so there is no instance of it when we call it so it needs to be a class method
    @classmethod
    def deserialize(cls, compressed: bytes):
        # initially it was <type> <length> + "\0" + <content>

        initial = zlib.decompress(compressed) # still bytes, just decompressed

        null_idx = initial.find(b"\0") # find seperator


        content = initial[null_idx + 1:]# everything after the null idx is content


        length_type = initial[:null_idx] # everything up to the null_idx


        space_idx = length_type.find(b" ")


        obj_type = length_type[:space_idx]

        return obj_type.decode(), content


    def compute_hash(self) -> str:
        return hashlib.sha1(self.serialize()).hexdigest()








