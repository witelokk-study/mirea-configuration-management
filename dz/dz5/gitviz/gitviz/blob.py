from dataclasses import dataclass


@dataclass
class Blob:
    object_name: str
    data: bytes
    size: int
