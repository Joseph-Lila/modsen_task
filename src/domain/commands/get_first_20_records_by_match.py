from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class GetFirst20RecordsByMatch(Command):
    text: str
