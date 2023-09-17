from dataclasses import dataclass


@dataclass
class Rule:
    target: str
    dependencies: list[str]
    commands: list[str]
