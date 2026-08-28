from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.rrr import RRR
from app.models.party import Party
from app.models.spatial_unit import SpatialUnit
from app.schemas.rrr import RRRCreate, RRRResponse


router = APIRouter(
    prefix="/rrr",
    tags=["RRR"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=RRRResponse)
def create_rrr(
    rrr: RRRCreate,
    db: Session = Depends(get_db)
):

    party = db.query(Party).filter(
        Party.id == rrr.party_id
    ).first()

    if not party:
        raise HTTPException(
            status_code=404,
            detail="Party not found"
        )

    spatial_unit = db.query(SpatialUnit).filter(
        SpatialUnit.id == rrr.spatial_unit_id
    ).first()

    if not spatial_unit:
        raise HTTPException(
            status_code=404,
            detail="Spatial unit not found"
        )

    new_rrr = RRR(
        party_id=rrr.party_id,
        spatial_unit_id=rrr.spatial_unit_id,
        rrr_type=rrr.rrr_type,
        share=rrr.share,
        start_date=rrr.start_date,
        end_date=rrr.end_date,
        status=rrr.status,
        description=rrr.description
    )

    db.add(new_rrr)
    db.commit()
    db.refresh(new_rrr)

    return new_rrr


@router.get("/", response_model=list[RRRResponse])
def get_rrrs(db: Session = Depends(get_db)):
    return db.query(RRR).all()