from dataclasses import dataclass
from typing import Any


@dataclass
class Variable:
    name: str
    value: Any
