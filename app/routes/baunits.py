from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.baunit import BAUnit
from app.models.spatial_unit import SpatialUnit
from app.schemas.baunit import BAUnitCreate, BAUnitResponse


router = APIRouter(
    prefix="/baunits",
    tags=["BAUnits"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BAUnitResponse)
def create_baunit(
    baunit: BAUnitCreate,
    db: Session = Depends(get_db)
):
    spatial_unit = db.query(SpatialUnit).filter(
        SpatialUnit.id == baunit.spatial_unit_id
    ).first()

    if not spatial_unit:
        raise HTTPException(
            status_code=404,
            detail="Spatial unit not found"
        )

    existing = db.query(BAUnit).filter(
        BAUnit.baunit_number == baunit.baunit_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="BAUnit number already exists"
        )

    new_baunit = BAUnit(
        baunit_number=baunit.baunit_number,
        spatial_unit_id=baunit.spatial_unit_id,
        status=baunit.status,
        description=baunit.description
    )

    db.add(new_baunit)
    db.commit()
    db.refresh(new_baunit)

    return new_baunit


@router.get("/", response_model=list[BAUnitResponse])
def get_baunits(db: Session = Depends(get_db)):
    return db.query(BAUnit).all()