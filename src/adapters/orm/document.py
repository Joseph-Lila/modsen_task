""" Module srс.adapters.orm """

from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Document:
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        autoincrement=True,
    )
    text: Mapped[str]
    rubrics: Mapped[List["Rubric"]] = relationship(
        default_factory=list,
        backref="rubrics",
        secondary="document_rubrics",
    )
    created_date: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        default=None,
    )
