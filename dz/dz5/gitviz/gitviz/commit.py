from __future__ import annotations
from dataclasses import dataclass

from .blob import Blob
from .tree import Tree


@dataclass
class Commit:
    object_name: str
    tree: Tree
    parent: Commit
    author: str
    committer: str
    name: str

