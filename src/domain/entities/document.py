""" Module srс.domain.entities """

from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Document:
    id: int
    text: str
    created_date: date
    rubrics: List[str]
