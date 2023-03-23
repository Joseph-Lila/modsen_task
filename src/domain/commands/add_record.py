from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class AddRecord(Command):
    id_: int
    text: str
