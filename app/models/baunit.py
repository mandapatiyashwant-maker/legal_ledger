from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class BAUnit(Base):
    __tablename__ = "ba_units"

    id = Column(Integer, primary_key=True, index=True)

    baunit_number = Column(
        String,
        unique=True,
        nullable=False
    )

    spatial_unit_id = Column(
        Integer,
        ForeignKey("spatial_units.id"),
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    description = Column(
        String,
        nullable=True
    )