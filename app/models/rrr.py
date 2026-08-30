from sqlalchemy import Column, Integer, String, ForeignKey, Date


from app.database import Base


class RRR(Base):
    __tablename__ = "rrrs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    party_id = Column(
        Integer,
        ForeignKey("parties.id"),
        nullable=False
    )

    spatial_unit_id = Column(
        Integer,
        ForeignKey("spatial_units.id"),
        nullable=False
    )

    # Legal relationship type
    rrr_type = Column(
        String,
        nullable=False
    )

    # More specific legal classification
    subtype = Column(
        String,
        nullable=True
    )

    # Ownership / legal share
    share = Column(
        Integer,
        nullable=True
    )

    # Legal validity period
    start_date = Column(
        Date,
        nullable=True
    )

    end_date = Column(
        Date,
        nullable=True
    )

    # Supporting legal document
    source_document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=True
    )

    # Legal record state
    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    # Priority of the legal relationship
    priority = Column(
        Integer,
        nullable=True
    )

    # Additional information
    notes = Column(
        String,
        nullable=True
    )

    # Existing description retained for compatibility
    description = Column(
        String,
        nullable=True
    )