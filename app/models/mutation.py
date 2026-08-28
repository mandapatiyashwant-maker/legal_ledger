from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Mutation(Base):
    __tablename__ = "mutations"

    id = Column(Integer, primary_key=True, index=True)

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

    state = Column(
        String,
        nullable=False,
        default="SUBMITTED"
    )

    reason = Column(
        String,
        nullable=True
    )

    rejection_reason = Column(
        String,
        nullable=True
    )