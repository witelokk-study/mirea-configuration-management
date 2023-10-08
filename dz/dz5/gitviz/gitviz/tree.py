from __future__ import annotations
from dataclasses import dataclass

from .blob import Blob


@dataclass
class TreeEntry:
    mode: int
    name: str
    blob_or_tree_object_name: str


@dataclass
class Tree:
    object_name: str
    entries: list[TreeEntry]

