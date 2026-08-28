from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.party import Party
from app.schemas.party import PartyCreate, PartyResponse


router = APIRouter(
    prefix="/parties",
    tags=["Parties"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PartyResponse)
def create_party(
    party: PartyCreate,
    db: Session = Depends(get_db)
):
    new_party = Party(
        name=party.name,
        party_type=party.party_type
    )

    db.add(new_party)
    db.commit()
    db.refresh(new_party)

    return new_party


@router.get("/", response_model=list[PartyResponse])
def get_parties(db: Session = Depends(get_db)):
    return db.query(Party).all()