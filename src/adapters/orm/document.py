from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import func
from src.adapters.orm import mapper_registry


@mapper_registry.mapped_as_dataclass
class Document:
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    created_date: Mapped[date] = mapped_column(
        insert_default=func.current_date(),
        default=None,
    )
