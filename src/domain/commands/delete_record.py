from dataclasses import dataclass

from src.domain.commands.command import Command


@dataclass
class DeleteRecord(Command):
    id_: int
