from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base


class SpatialUnit(Base):
    __tablename__ = "spatial_units"

    id = Column(Integer, primary_key=True, index=True)

    # 3D spatial identity
    ulpin_3d = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    parent_ulpin = Column(
        String,
        nullable=True
    )

    # Spatial hierarchy
    parent_spatial_unit_id = Column(
        Integer,
        ForeignKey("spatial_units.id"),
        nullable=True
    )

    building_id = Column(
        String,
        nullable=True
    )

    source_building_id = Column(
        String,
        nullable=True
    )

    # Type of spatial unit
    unit_type = Column(
        String,
        nullable=False
    )

    floor_number = Column(
        Integer,
        nullable=True
    )

    # 3D spatial metadata
    z_min = Column(
        Float,
        nullable=True
    )

    z_max = Column(
        Float,
        nullable=True
    )

    area_2d = Column(
        Float,
        nullable=True
    )

    volume_3d = Column(
        Float,
        nullable=True
    )

    geometry_version = Column(
        Integer,
        nullable=False
    )

    geometry_hash = Column(
        String,
        nullable=True
    )

    geometry_source = Column(
        String,
        nullable=True
    )

    # Segmentation / verification information
    segmentation_method = Column(
        String,
        nullable=True
    )

    confidence = Column(
        String,
        nullable=True
    )

    validation_status = Column(
        String,
        nullable=True
    )

    # Temporal validity
    effective_from = Column(
        DateTime,
        nullable=True
    )

    effective_to = Column(
        DateTime,
        nullable=True
    )

    # Record status
    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime,
        nullable=True
    )

    updated_at = Column(
        DateTime,
        nullable=True
    )