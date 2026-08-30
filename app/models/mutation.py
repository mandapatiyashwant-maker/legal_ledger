from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Mutation(Base):
    __tablename__ = "mutations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    baunit_id = Column(
        Integer,
        ForeignKey("ba_units.id"),
        nullable=False
    )

    old_party_id = Column(
        Integer,
        ForeignKey("parties.id"),
        nullable=False
    )

    new_party_id = Column(
        Integer,
        ForeignKey("parties.id"),
        nullable=False
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=True
    )

    # Mutation workflow state
    state = Column(
        String,
        nullable=False,
        default="DRAFT"
    )

    reason = Column(
        String,
        nullable=True
    )

    rejection_reason = Column(
        String,
        nullable=True
    )

    # Legal validity period
    valid_from = Column(
        DateTime,
        nullable=True
    )

    valid_to = Column(
        DateTime,
        nullable=True
    )

    # When the mutation was recorded by the system
    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )