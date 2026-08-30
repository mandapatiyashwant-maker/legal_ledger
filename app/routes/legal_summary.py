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
    tags=["Legal Summary"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def build_legal_summary(
    ulpin_3d: str,
    db: Session
):

    # --------------------------------------------------
    # 1. Find Spatial Unit
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
    # 2. Find BAUnit
    # --------------------------------------------------

    baunit = db.query(BAUnit).filter(
        BAUnit.spatial_unit_id == spatial_unit.id
    ).first()


    # --------------------------------------------------
    # 3. Get active RRR records
    # --------------------------------------------------

    rrr_records = db.query(RRR).filter(
        RRR.spatial_unit_id == spatial_unit.id,
        RRR.status == "ACTIVE"
    ).all()

    active_rights = []
    restrictions = []
    responsibilities = []


    for rrr in rrr_records:

        party = db.query(Party).filter(
            Party.id == rrr.party_id
        ).first()

        party_name = (
            party.name
            if party
            else "Unknown"
        )


        record = {
            "rrr_id": rrr.id,
            "party_id": rrr.party_id,
            "party_name": party_name,

            "rrr_type": rrr.rrr_type,
            "subtype": rrr.subtype,

            "share": rrr.share,

            "start_date": rrr.start_date,
            "end_date": rrr.end_date,

            "source_document_id": (
                rrr.source_document_id
            ),

            "status": rrr.status,

            "priority": rrr.priority,

            "notes": rrr.notes,

            "description": rrr.description
        }


        if rrr.rrr_type in [
            "OWNERSHIP",
            "LEASE",
            "ACCESS_RIGHT",
            "AIR_RIGHT"
        ]:
            active_rights.append(record)


        elif rrr.rrr_type in [
            "MORTGAGE",
            "HERITAGE_RESTRICTION",
            "HEIGHT_RESTRICTION",
            "COURT_DISPUTE"
        ]:
            restrictions.append(record)


        elif rrr.rrr_type in [
            "MAINTENANCE",
            "PROPERTY_TAX",
            "UTILITY_ACCESS"
        ]:
            responsibilities.append(record)


    # --------------------------------------------------
    # 4. Documents
    # --------------------------------------------------

    document_records = []

    if baunit:

        documents = db.query(Document).filter(
            Document.baunit_id == baunit.id
        ).all()


        for document in documents:

            document_records.append({

                "id": document.id,

                "document_number": (
                    document.document_number
                ),

                "document_type": (
                    document.document_type
                ),

                "document_date": (
                    document.document_date
                ),

                "issuing_authority": (
                    document.issuing_authority
                ),

                "file_reference": (
                    document.file_reference
                ),

                "content_hash": (
                    document.content_hash
                ),

                "status": document.status,

                "description": (
                    document.description
                ),

                "is_demo_record": (
                    document.is_demo_record
                ),

                "demo_reference": (
                    document.demo_reference
                )
            })


    # --------------------------------------------------
    # 5. Mutations + history
    # --------------------------------------------------

    mutation_records = []

    if baunit:

        mutations = db.query(Mutation).filter(
            Mutation.baunit_id == baunit.id
        ).all()


        for mutation in mutations:

            history = db.query(
                MutationHistory
            ).filter(
                MutationHistory.mutation_id ==
                mutation.id
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

                "old_party_id": (
                    mutation.old_party_id
                ),

                "new_party_id": (
                    mutation.new_party_id
                ),

                "document_id": (
                    mutation.document_id
                ),

                "state": mutation.state,

                "reason": mutation.reason,

                "rejection_reason": (
                    mutation.rejection_reason
                ),

                "valid_from": (
                    mutation.valid_from
                ),

                "valid_to": (
                    mutation.valid_to
                ),

                "recorded_at": (
                    mutation.recorded_at
                ),

                "history": history_records
            })


    # --------------------------------------------------
    # 6. Spatial hierarchy
    # --------------------------------------------------

    parent_information = None

    if spatial_unit.parent_spatial_unit_id:

        parent_unit = db.query(
            SpatialUnit
        ).filter(
            SpatialUnit.id ==
            spatial_unit.parent_spatial_unit_id
        ).first()


        if parent_unit:

            parent_information = {

                "id": parent_unit.id,

                "ulpin_3d": (
                    parent_unit.ulpin_3d
                ),

                "unit_type": (
                    parent_unit.unit_type
                ),

                "building_id": (
                    parent_unit.building_id
                ),

                "floor_number": (
                    parent_unit.floor_number
                )
            }


    # --------------------------------------------------
    # 7. Final legal summary
    # --------------------------------------------------

    return {

        "ulpin_3d": spatial_unit.ulpin_3d,

        "spatial_unit": {

            "id": spatial_unit.id,

            "ulpin_3d": (
                spatial_unit.ulpin_3d
            ),

            "parent_ulpin": (
                spatial_unit.parent_ulpin
            ),

            "parent_spatial_unit_id": (
                spatial_unit.parent_spatial_unit_id
            ),

            "parent": parent_information,

            "unit_type": (
                spatial_unit.unit_type
            ),

            "building_id": (
                spatial_unit.building_id
            ),

            "source_building_id": (
                spatial_unit.source_building_id
            ),

            "floor_number": (
                spatial_unit.floor_number
            ),

            "z_min": spatial_unit.z_min,

            "z_max": spatial_unit.z_max,

            "area_2d": spatial_unit.area_2d,

            "volume_3d": (
                spatial_unit.volume_3d
            ),

            "geometry_version": (
                spatial_unit.geometry_version
            ),

            "geometry_hash": (
                spatial_unit.geometry_hash
            ),

            "geometry_source": (
                spatial_unit.geometry_source
            ),

            "segmentation_method": (
                spatial_unit.segmentation_method
            ),

            "confidence": (
                spatial_unit.confidence
            ),

            "validation_status": (
                spatial_unit.validation_status
            ),

            "effective_from": (
                spatial_unit.effective_from
            ),

            "effective_to": (
                spatial_unit.effective_to
            ),

            "status": spatial_unit.status
        },


        "baunit": (

            {
                "id": baunit.id,

                "baunit_number": (
                    baunit.baunit_number
                ),

                "status": baunit.status
            }

            if baunit
            else None
        ),


        "active_rights": active_rights,

        "restrictions": restrictions,

        "responsibilities": responsibilities,

        "documents": document_records,

        "mutations": mutation_records,

        "current_status": (
            spatial_unit.status
        )
    }


# ==================================================
# OLD ENDPOINT — KEPT FOR COMPATIBILITY
# ==================================================

@router.get(
    "/legal-summary/{ulpin_3d}"
)
def get_legal_summary(
    ulpin_3d: str,
    db: Session = Depends(get_db)
):

    return build_legal_summary(
        ulpin_3d,
        db
    )


# ==================================================
# NEW GROUP 3 → GROUP 4 ENDPOINT
# ==================================================

@router.get(
    "/legal/properties/{ulpin3d}/summary"
)
def get_property_legal_summary(
    ulpin3d: str,
    db: Session = Depends(get_db)
):

    return build_legal_summary(
        ulpin3d,
        db
    )