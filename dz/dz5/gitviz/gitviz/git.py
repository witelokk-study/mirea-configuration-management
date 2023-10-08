from os import listdir, path
from io import BytesIO
import zlib

from .blob import Blob
from .tree import Tree, TreeEntry
from .commit import Commit


def read_to_delimiter(bytes_io: BytesIO, delimiter: bytes):
    res = b""
    while (ch := bytes_io.read(1)) != delimiter:
        res += ch
    return res


class Git:
    def __init__(self, repo_dir: str):
        if not path.exists(path.join(repo_dir, ".git")):
            raise RuntimeError("Current directory is not a git repo")

        self._repo_dir = repo_dir

        self._commits: dict[str, Commit] = {}
        self._trees: dict[str, Tree] = {}
        self._blobs: dict[str, Blob] = {}

        self._load_objects()

    @property
    def commits(self):
        return self._commits

    @property
    def trees(self):
        return self._trees

    @property
    def blobs(self):
        return self._blobs

    def _load_objects(self):
        blobs = []
        trees = []
        commits = []

        for object_name in self._get_objects_names():
            data = self._read_object(object_name)

            if data.startswith(b"blob "):
                blobs.append((object_name, data))
            elif data.startswith(b"tree "):
                trees.append((object_name, data))
            elif data.startswith(b"commit "):
                commits.append((object_name, data))
            else:
                raise NotImplementedError()

        for object_name, data in blobs:
            blob_size, blob_data = data[5:].split(b"\x00", 1)
            self._blobs[object_name] = Blob(object_name, blob_data, int(blob_size))

        for object_name, data in trees:
            data_io = BytesIO(data)
            data_io.read(5)  # header
            size = int(read_to_delimiter(data_io, b"\x00"))
            tree_entries = []
            while data_io.tell() < size:
                mode = int(read_to_delimiter(data_io, b" "))
                name = read_to_delimiter(data_io, b"\x00").decode()
                blob_or_tree_object_name = "".join(
                    [hex(x)[2:].zfill(2) for x in data_io.read(20)])
                tree_entries.append(TreeEntry(mode, name, blob_or_tree_object_name))
            self._trees[object_name] = Tree(object_name, tree_entries)

        for object_name, data in commits:
            data_io = BytesIO(data)
            data_io.read(7)  # header
            size = int(read_to_delimiter(data_io, b"\x00"))

            tree = None
            parent = None
            author = None
            committer = None

            while data_io.tell() < size:
                entry = read_to_delimiter(data_io, b" ").decode()

                if entry == "tree":
                    tree = self._trees[read_to_delimiter(data_io, b"\n").decode()]
                elif entry == "author":
                    author = read_to_delimiter(data_io, b"\n").decode()
                elif entry == "committer":
                    committer = read_to_delimiter(data_io, b"\n").decode()
                    break
                elif entry == "parent":
                    parent = read_to_delimiter(data_io, b"\n").decode()
            name = data_io.read().decode().strip()
            self._commits[object_name] = Commit(object_name, tree, parent, author, committer, name)

    def _get_objects_names(self):
        objects_dirs = listdir(path.join(self._repo_dir, ".git", "objects"))
        for objects_dir in objects_dirs:
            if objects_dir in ("pack", "info"):
                continue

            objects = listdir(path.join(self._repo_dir, ".git", "objects", objects_dir))
            for obj in objects:
                yield objects_dir + obj

    def _read_object(self, name: str):
        object_path = path.join(self._repo_dir, ".git", "objects", name[:2], name[2:])
        with open(object_path, 'rb') as f:
            compressed_data = f.read()

        return zlib.decompress(compressed_data)
