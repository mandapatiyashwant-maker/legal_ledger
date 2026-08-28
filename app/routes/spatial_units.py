from fastapi import APIRouter, Depends
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


@router.post("/", response_model=SpatialUnitResponse)
def create_spatial_unit(
    spatial_unit: SpatialUnitCreate,
    db: Session = Depends(get_db)
):
    new_spatial_unit = SpatialUnit(
        ulpin_3d=spatial_unit.ulpin_3d,
        unit_type=spatial_unit.unit_type,
        geometry_version=spatial_unit.geometry_version,
        geometry_hash=spatial_unit.geometry_hash,
        conflict_status=spatial_unit.conflict_status,
        effective_time=spatial_unit.effective_time
    )

    db.add(new_spatial_unit)
    db.commit()
    db.refresh(new_spatial_unit)

    return new_spatial_unit


@router.get("/", response_model=list[SpatialUnitResponse])
def get_spatial_units(db: Session = Depends(get_db)):
    return db.query(SpatialUnit).all()