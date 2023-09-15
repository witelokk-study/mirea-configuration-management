from dataclasses import dataclass


@dataclass
class Rule:
    target: str
    prerequisites: list[str]
    commands: list[str]
