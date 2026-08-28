from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.spatial_unit import SpatialUnit
from app.models.baunit import BAUnit
from app.models.rrr import RRR
from app.models.party import Party
from app.models.document import Document
from app.models.mutation import Mutation
from app.models.mutation_history import MutationHistory


router = APIRouter(
    prefix="/legal-summary",
    tags=["Legal Summary"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/{ulpin_3d}")
def get_legal_summary(
    ulpin_3d: str,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # 1. Find Spatial Unit using 3D-ULPIN
    # --------------------------------------------------

    spatial_unit = db.query(SpatialUnit).filter(
        SpatialUnit.ulpin_3d == ulpin_3d
    ).first()

    if not spatial_unit:
        raise HTTPException(
            status_code=404,
            detail="3D-ULPIN not found"
        )


    # --------------------------------------------------
    # 2. Find BAUnit connected to Spatial Unit
    # --------------------------------------------------

    baunit = db.query(BAUnit).filter(
        BAUnit.spatial_unit_id == spatial_unit.id
    ).first()

    if not baunit:
        raise HTTPException(
            status_code=404,
            detail="BAUnit not found"
        )


    # --------------------------------------------------
    # 3. Get ACTIVE RRR records
    # --------------------------------------------------

    rrr_records = db.query(RRR).filter(
        RRR.spatial_unit_id == spatial_unit.id,
        RRR.status == "ACTIVE"
    ).all()

    active_rights = []
    restrictions = []
    responsibilities = []


    for rrr in rrr_records:

        # Find party associated with RRR
        party = db.query(Party).filter(
            Party.id == rrr.party_id
        ).first()

        party_name = party.name if party else "Unknown"


        record = {
            "rrr_id": rrr.id,
            "party_id": rrr.party_id,
            "party_name": party_name,
            "rrr_type": rrr.rrr_type,
            "share": rrr.share,
            "start_date": rrr.start_date,
            "end_date": rrr.end_date,
            "description": rrr.description
        }


        # -------------------------------
        # Rights
        # -------------------------------

        if rrr.rrr_type in [
            "OWNERSHIP",
            "LEASE",
            "ACCESS_RIGHT",
            "AIR_RIGHT"
        ]:

            active_rights.append(record)


        # -------------------------------
        # Restrictions
        # -------------------------------

        elif rrr.rrr_type in [
            "MORTGAGE",
            "HERITAGE_RESTRICTION",
            "HEIGHT_RESTRICTION",
            "COURT_DISPUTE"
        ]:

            restrictions.append(record)


        # -------------------------------
        # Responsibilities
        # -------------------------------

        elif rrr.rrr_type in [
            "MAINTENANCE",
            "PROPERTY_TAX",
            "UTILITY_ACCESS"
        ]:

            responsibilities.append(record)


    # --------------------------------------------------
    # 4. Get Documents belonging to BAUnit
    # --------------------------------------------------

    documents = db.query(Document).filter(
        Document.baunit_id == baunit.id
    ).all()

    document_records = []


    for document in documents:

        document_records.append({
            "id": document.id,
            "document_number": document.document_number,
            "document_type": document.document_type,
            "document_date": document.document_date,
            "issuing_authority": document.issuing_authority,
            "status": document.status,
            "description": document.description
        })


    # --------------------------------------------------
    # 5. Get Mutations for this BAUnit
    # --------------------------------------------------

    mutations = db.query(Mutation).filter(
        Mutation.baunit_id == baunit.id
    ).all()

    mutation_records = []


    for mutation in mutations:

        # Get mutation history
        history = db.query(MutationHistory).filter(
            MutationHistory.mutation_id == mutation.id
        ).order_by(
            MutationHistory.changed_at
        ).all()

        history_records = []


        for entry in history:

            history_records.append({
                "old_state": entry.old_state,
                "new_state": entry.new_state,
                "changed_by": entry.changed_by,
                "reason": entry.reason,
                "changed_at": entry.changed_at
            })


        mutation_records.append({
            "mutation_id": mutation.id,
            "old_party_id": mutation.old_party_id,
            "new_party_id": mutation.new_party_id,
            "document_id": mutation.document_id,
            "state": mutation.state,
            "reason": mutation.reason,
            "rejection_reason": mutation.rejection_reason,
            "history": history_records
        })


    # --------------------------------------------------
    # 6. Return Complete Legal Summary
    # --------------------------------------------------

    return {

        # 3D property identifier
        "ulpin_3d": spatial_unit.ulpin_3d,


        # Spatial information from Group 3
        "spatial_unit": {
            "id": spatial_unit.id,
            "unit_type": spatial_unit.unit_type,
            "geometry_version": spatial_unit.geometry_version,
            "geometry_hash": spatial_unit.geometry_hash,
            "conflict_status": spatial_unit.conflict_status,
            "effective_time": spatial_unit.effective_time
        },


        # Legal/administrative unit
        "baunit": {
            "id": baunit.id,
            "baunit_number": baunit.baunit_number,
            "status": baunit.status
        },


        # Active legal rights
        "active_rights": active_rights,


        # Active restrictions
        "restrictions": restrictions,


        # Active responsibilities
        "responsibilities": responsibilities,


        # Supporting documents
        "documents": document_records,


        # Mutation and audit history
        "mutations": mutation_records
    }