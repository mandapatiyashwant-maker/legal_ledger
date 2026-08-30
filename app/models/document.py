from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_number = Column(
        String,
        unique=True,
        nullable=False
    )

    document_type = Column(
        String,
        nullable=False
    )

    baunit_id = Column(
        Integer,
        ForeignKey("ba_units.id"),
        nullable=False
    )

    document_date = Column(
        String,
        nullable=True
    )

    issuing_authority = Column(
        String,
        nullable=True
    )

    file_reference = Column(
        String,
        nullable=True
    )

    content_hash = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="VALID"
    )

    description = Column(
        String,
        nullable=True
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