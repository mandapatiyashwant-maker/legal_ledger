from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.mutation import Mutation
from app.models.baunit import BAUnit
from app.models.party import Party
from app.models.document import Document
from app.schemas.mutation import MutationCreate, MutationResponse
from app.models.rrr import RRR
from app.models.mutation_history import MutationHistory


router = APIRouter(
    prefix="/mutations",
    tags=["Mutations"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MutationResponse)
def create_mutation(
    mutation: MutationCreate,
    db: Session = Depends(get_db)
):

    baunit = db.query(BAUnit).filter(
        BAUnit.id == mutation.baunit_id
    ).first()

    if not baunit:
        raise HTTPException(
            status_code=404,
            detail="BAUnit not found"
        )

    old_party = db.query(Party).filter(
        Party.id == mutation.old_party_id
    ).first()

    if not old_party:
        raise HTTPException(
            status_code=404,
            detail="Old party not found"
        )

    new_party = db.query(Party).filter(
        Party.id == mutation.new_party_id
    ).first()

    if not new_party:
        raise HTTPException(
            status_code=404,
            detail="New party not found"
        )

    if mutation.document_id is not None:

        document = db.query(Document).filter(
            Document.id == mutation.document_id
        ).first()

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

    if mutation.old_party_id == mutation.new_party_id:
        raise HTTPException(
            status_code=400,
            detail="Old and new party cannot be the same"
        )

    new_mutation = Mutation(
        baunit_id=mutation.baunit_id,
        old_party_id=mutation.old_party_id,
        new_party_id=mutation.new_party_id,
        document_id=mutation.document_id,
        state="SUBMITTED",
        reason=mutation.reason
    )

    db.add(new_mutation)
    db.commit()
    db.refresh(new_mutation)

    return new_mutation


@router.get("/", response_model=list[MutationResponse])
def get_mutations(db: Session = Depends(get_db)):
    return db.query(Mutation).all()
@router.patch("/{mutation_id}/state")
def update_mutation_state(
    mutation_id: int,
    new_state: str,
    changed_by: str = "Demo Officer",
    reason: str | None = None,
    db: Session = Depends(get_db)
):
    mutation = db.query(Mutation).filter(
        Mutation.id == mutation_id
    ).first()

    if not mutation:
        raise HTTPException(
            status_code=404,
            detail="Mutation not found"
        )

    allowed_transitions = {
        "SUBMITTED": ["UNDER_REVIEW", "REJECTED"],
        "UNDER_REVIEW": ["APPROVED", "REJECTED"],
        "APPROVED": ["REGISTERED"],
        "REJECTED": [],
        "REGISTERED": ["SUPERSEDED"],
        "SUPERSEDED": []
    }

    current_state = mutation.state

    if new_state not in allowed_transitions.get(
        current_state, []
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition: {current_state} -> {new_state}"
        )

    # Save state history
    history = MutationHistory(
    mutation_id=mutation.id,
    old_state=current_state,
    new_state=new_state,
    changed_by=changed_by,
    reason=reason or f"State changed from {current_state} to {new_state}"
)

    db.add(history)

    # Ownership transfer when mutation is registered
    if new_state == "REGISTERED":

        baunit = db.query(BAUnit).filter(
        BAUnit.id == mutation.baunit_id
    ).first()

    if not baunit:
        raise HTTPException(
            status_code=404,
            detail="BAUnit not found"
        )

    # Find the active ownership of this property
    active_ownerships = db.query(RRR).filter(
        RRR.spatial_unit_id == baunit.spatial_unit_id,
        RRR.rrr_type == "OWNERSHIP",
        RRR.status == "ACTIVE"
    ).all()

    # The old party must have an active ownership
    old_ownership = None

    for ownership in active_ownerships:
        if ownership.party_id == mutation.old_party_id:
            old_ownership = ownership
            break

    if not old_ownership:
        raise HTTPException(
            status_code=400,
            detail="Old party is not an active owner of this property"
        )

    # Prevent the new party from already being an active owner
    for ownership in active_ownerships:
        if ownership.party_id == mutation.new_party_id:
            raise HTTPException(
                status_code=400,
                detail="New party already has active ownership"
            )

    # Preserve old ownership as history
    old_ownership.status = "SUPERSEDED"

    # Create new active ownership
    new_ownership = RRR(
        party_id=mutation.new_party_id,
        spatial_unit_id=baunit.spatial_unit_id,
        rrr_type="OWNERSHIP",
        share=old_ownership.share,
        start_date=None,
        end_date=None,
        status="ACTIVE",
        description=(
            f"Ownership transferred from "
            f"party {mutation.old_party_id}"
        )
    )

    db.add(new_ownership)

    mutation.state = new_state
    if new_state == "REJECTED":
        mutation.rejection_reason = reason or "Mutation rejected"

    db.commit()
    db.refresh(mutation)

    return mutation