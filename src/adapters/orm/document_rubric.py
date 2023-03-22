""" Module srс.adapters.orm """

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class DocumentRubric:
    __tablename__ = 'document_rubrics'

    id: Mapped[int] = mapped_column(
        init=False,
        primary_key=True,
        autoincrement=True,
    )
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    rubric_id: Mapped[int] = mapped_column(ForeignKey("rubrics.id"))
