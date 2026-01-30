<!--markdownlint-disable-->


# Git Objects

Git objects consist of

- blobs
- commits
- trees
- one last thing


every git object can be serialized into

<type> + " " <length> + "\0" + <content>

of course all of these are in byte format


git then stores these objects inits objects directory in their compressed format

They are compressed with zlib


Git stores them in the object directory using the first 2 digits of their hash as the initial folder, and the remaining 38 digits as the file name


The hash is calculated by the SHA1 of the serialized file


# Blobs



