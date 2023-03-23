""" Module srс.domain.entities """

from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.domain.entities.base_entity import BaseEntity


@dataclass
class Document(BaseEntity):
    text: str
    created_date: datetime
    rubrics: List[str]
