from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.database import Base


class RRR(Base):
    __tablename__ = "rrrs"

    id = Column(Integer, primary_key=True, index=True)

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

    rrr_type = Column(String, nullable=False)

    share = Column(Integer, nullable=True)

    start_date = Column(Date, nullable=True)

    end_date = Column(Date, nullable=True)

    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    description = Column(String, nullable=True)