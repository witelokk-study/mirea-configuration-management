from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CpioEntry:
    ino: int
    mode: int
    uid: int
    gid: int
    nlink: int
    mtime: int
    devmajor: int
    devminor: int
    rdevmajor: int
    rdevminor: int
    check: int

    path: str
    data: bytes
