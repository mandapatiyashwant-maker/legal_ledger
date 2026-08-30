from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.spatial_unit import SpatialUnit
from app.schemas.integration import (
    SpatialUnitRegistrationRequest,
    SpatialUnitRegistrationResponse
)


router = APIRouter(
    prefix="/legal",
    tags=["Group 3 Integration"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/spatial-units/register",
    response_model=SpatialUnitRegistrationResponse,
    status_code=201
)
def register_spatial_unit(
    registration: SpatialUnitRegistrationRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # Check whether this 3D ULPIN already exists
    # --------------------------------------------------

    existing = db.query(SpatialUnit).filter(
        SpatialUnit.ulpin_3d == registration.ulpin3d
    ).first()

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Spatial unit with this ULPIN3D already exists"
        )


    # --------------------------------------------------
    # Validate parent spatial unit
    # --------------------------------------------------

    parent_spatial_unit = None

    if registration.parent_ulpin:

        parent_spatial_unit = db.query(
            SpatialUnit
        ).filter(
            SpatialUnit.ulpin_3d ==
            registration.parent_ulpin
        ).first()

        if not parent_spatial_unit:

            raise HTTPException(
                status_code=404,
                detail="Parent spatial unit not found"
            )


    # --------------------------------------------------
    # Create legal spatial-unit record
    #
    # NOTE:
    # No 3D geometry is stored here.
    # Only metadata/provenance is stored.
    # --------------------------------------------------

    new_spatial_unit = SpatialUnit(

        ulpin_3d=registration.ulpin3d,

        parent_ulpin=registration.parent_ulpin,

        parent_spatial_unit_id=(
            parent_spatial_unit.id
            if parent_spatial_unit
            else None
        ),

        building_id=registration.building_id,

        source_building_id=(
            registration.source_building_id
        ),

        unit_type=registration.unit_type,

        floor_number=registration.floor_number,

        z_min=registration.z_min,

        z_max=registration.z_max,

        area_2d=registration.area_2d,

        volume_3d=registration.volume_3d,

        geometry_version=(
            registration.geometry_version
        ),

        geometry_hash=registration.geometry_hash,

        geometry_source=(
            registration.geometry_source
        ),

        segmentation_method=(
            registration.segmentation_method
        ),

        confidence=registration.confidence,

        validation_status=(
            registration.validation_status
        ),

        effective_from=(
            registration.effective_from
        ),

        effective_to=(
            registration.effective_to
        ),

        status="ACTIVE"
    )


    db.add(new_spatial_unit)

    db.commit()

    db.refresh(new_spatial_unit)


    # --------------------------------------------------
    # Return integration response
    # --------------------------------------------------

    return {
        "id": new_spatial_unit.id,

        "ulpin3d": new_spatial_unit.ulpin_3d,

        "parent_ulpin": (
            new_spatial_unit.parent_ulpin
        ),

        "unit_type": (
            new_spatial_unit.unit_type
        ),

        "building_id": (
            new_spatial_unit.building_id
        ),

        "source_building_id": (
            new_spatial_unit.source_building_id
        ),

        "floor_number": (
            new_spatial_unit.floor_number
        ),

        "geometry_version": (
            new_spatial_unit.geometry_version
        ),

        "geometry_hash": (
            new_spatial_unit.geometry_hash
        ),

        "validation_status": (
            new_spatial_unit.validation_status
        ),

        "status": (
            new_spatial_unit.status
        ),

        "message": (
            "3D spatial unit successfully "
            "registered in Legal Ledger"
        )
    }