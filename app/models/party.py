from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Party(Base):
    __tablename__ = "parties"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    party_type = Column(
        String,
        nullable=False
    )

    is_demo_record = Column(
        Boolean,
        nullable=False,
        default=True
    )

    demo_reference = Column(
        String,
        nullable=True
    )