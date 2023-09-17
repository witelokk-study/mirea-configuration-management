import json
from collections import defaultdict
from os import path
from hashlib import md5


class HashesManager:
    def __init__(self, dir_name: str):
        self._dir_name = dir_name
        self._path = path.join(dir_name, ".minimake_hashes")
        self._dict: dict[str, str | None] = defaultdict(lambda: None)
        self.load()

    def load(self):
        try:
            with open(self._path) as f:
                self._dict.update(json.load(f))
        except FileNotFoundError:
            pass

    def is_file_updated(self, relative_path: str):
        full_path = path.realpath(path.join(self._dir_name, relative_path))
        # try:
        with open(full_path, "rb") as f:
            current_hash = md5(f.read()).hexdigest()
        return self._dict[relative_path] != current_hash

    def get_hash(self, relative_path: str) -> str | None:
        return self._dict[relative_path]

    def update_hash(self, relative_path: str) -> None:
        full_path = path.realpath(path.join(self._dir_name, relative_path))
        try:
            with open(full_path, "rb") as f:
                self._dict[relative_path] = md5(f.read()).hexdigest()
        except FileNotFoundError as e:
            if relative_path in self._dict:
                self._dict.pop(relative_path)
            raise e

    def write(self):
        with open(self._path, "w") as f:
            json.dump(self._dict, f)
