from dataclasses import dataclass
from typing import List

from src.domain.entities import Document
from src.domain.events.event import Event


@dataclass
class GotFirst20RecordsByMatch(Event):
    documents: List[Document]
