from dataclasses import dataclass
from typing import List

from src.domain.events.event import Event


@dataclass
class GotFirst20RecordsByMatch(Event):
    document_ids: List[int]
