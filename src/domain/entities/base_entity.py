""" Module srс.domain.entities """

from dataclasses import dataclass


@dataclass
class BaseEntity:
    id: int
