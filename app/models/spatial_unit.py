from sqlalchemy import Column, Integer, String
from app.database import Base


class SpatialUnit(Base):
    __tablename__ = "spatial_units"

    id = Column(Integer, primary_key=True, index=True)

    ulpin_3d = Column(
        String,
        unique=True,
        nullable=False
    )

    unit_type = Column(
        String,
        nullable=False
    )

    geometry_version = Column(
        Integer,
        nullable=False
    )

    geometry_hash = Column(
        String,
        nullable=True
    )

    conflict_status = Column(
        String,
        nullable=False,
        default="NO_CONFLICT"
    )

    effective_time = Column(
        String,
        nullable=True
    )