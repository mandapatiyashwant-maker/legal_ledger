from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.spatial_unit import SpatialUnit
from app.schemas.spatial_unit import (
    SpatialUnitCreate,
    SpatialUnitResponse
)


router = APIRouter(
    prefix="/spatial-units",
    tags=["Spatial Units"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Allowed parent-child spatial hierarchy
# --------------------------------------------------

ALLOWED_PARENT_TYPES = {
    "PARCEL": {None},
    "BUILDING": {"PARCEL"},
    "FLOOR": {"BUILDING"},
    "APARTMENT": {"FLOOR"},
    "COMMERCIAL_UNIT": {"FLOOR"},
    "PARKING": {"FLOOR", "BUILDING"},
    "BASEMENT": {"BUILDING"},
    "UTILITY": {"BUILDING", "FLOOR", "PARCEL"},
    "AIR_RIGHT": {"PARCEL", "BUILDING"},
    "COMMON_AREA": {"BUILDING", "FLOOR"},
    "OTHER_3D_SPACE": {
        "PARCEL",
        "BUILDING",
        "FLOOR"
    }
}


@router.post(
    "/",
    response_model=SpatialUnitResponse
)
def create_spatial_unit(
    spatial_unit: SpatialUnitCreate,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # Validate parent spatial unit
    # --------------------------------------------------

    parent = None

    if spatial_unit.parent_spatial_unit_id is not None:

        parent = db.query(SpatialUnit).filter(
            SpatialUnit.id ==
            spatial_unit.parent_spatial_unit_id
        ).first()

        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent spatial unit not found"
            )

        allowed_parents = ALLOWED_PARENT_TYPES.get(
            spatial_unit.unit_type,
            set()
        )

        if parent.unit_type not in allowed_parents:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid hierarchy: "
                    f"{spatial_unit.unit_type} "
                    f"cannot have "
                    f"{parent.unit_type} as parent"
                )
            )

    # --------------------------------------------------
    # Prevent self-parenting
    # --------------------------------------------------

    if (
        spatial_unit.parent_spatial_unit_id is not None
        and spatial_unit.ulpin_3d
    ):

        existing = db.query(SpatialUnit).filter(
            SpatialUnit.ulpin_3d ==
            spatial_unit.ulpin_3d
        ).first()

        if existing and (
            existing.id ==
            spatial_unit.parent_spatial_unit_id
        ):

            raise HTTPException(
                status_code=400,
                detail="A spatial unit cannot be its own parent"
            )

    # --------------------------------------------------
    # Create Spatial Unit
    # --------------------------------------------------

    new_spatial_unit = SpatialUnit(

        ulpin_3d=spatial_unit.ulpin_3d,

        parent_ulpin=spatial_unit.parent_ulpin,

        parent_spatial_unit_id=(
            spatial_unit.parent_spatial_unit_id
        ),

        building_id=spatial_unit.building_id,

        source_building_id=(
            spatial_unit.source_building_id
        ),

        unit_type=spatial_unit.unit_type,

        floor_number=spatial_unit.floor_number,

        z_min=spatial_unit.z_min,

        z_max=spatial_unit.z_max,

        area_2d=spatial_unit.area_2d,

        volume_3d=spatial_unit.volume_3d,

        geometry_version=(
            spatial_unit.geometry_version
        ),

        geometry_hash=(
            spatial_unit.geometry_hash
        ),

        geometry_source=(
            spatial_unit.geometry_source
        ),

        segmentation_method=(
            spatial_unit.segmentation_method
        ),

        confidence=(
            spatial_unit.confidence
        ),

        validation_status=(
            spatial_unit.validation_status
        ),

        effective_from=(
            spatial_unit.effective_from
        ),

        effective_to=(
            spatial_unit.effective_to
        ),

        status=spatial_unit.status
    )

    db.add(new_spatial_unit)
    db.commit()
    db.refresh(new_spatial_unit)

    return new_spatial_unit


# --------------------------------------------------
# Get all spatial units
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[SpatialUnitResponse]
)
def get_spatial_units(
    db: Session = Depends(get_db)
):

    return db.query(SpatialUnit).all()