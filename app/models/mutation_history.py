from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class MutationHistory(Base):
    __tablename__ = "mutation_history"

    id = Column(Integer, primary_key=True, index=True)

    mutation_id = Column(
        Integer,
        ForeignKey("mutations.id"),
        nullable=False
    )

    old_state = Column(
        String,
        nullable=True
    )

    new_state = Column(
        String,
        nullable=False
    )

    changed_by = Column(
        String,
        nullable=False
    )

    reason = Column(
        String,
        nullable=True
    )

    changed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )