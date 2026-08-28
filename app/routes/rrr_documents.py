from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.rrr import RRR
from app.models.document import Document
from app.models.rrr_document import RRRDocument
from app.schemas.rrr_document import (
    RRRDocumentCreate,
    RRRDocumentResponse
)


router = APIRouter(
    prefix="/rrr-documents",
    tags=["RRR Documents"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=RRRDocumentResponse)
def link_document_to_rrr(
    link: RRRDocumentCreate,
    db: Session = Depends(get_db)
):

    rrr = db.query(RRR).filter(
        RRR.id == link.rrr_id
    ).first()

    if not rrr:
        raise HTTPException(
            status_code=404,
            detail="RRR not found"
        )

    document = db.query(Document).filter(
        Document.id == link.document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    existing = db.query(RRRDocument).filter(
        RRRDocument.rrr_id == link.rrr_id,
        RRRDocument.document_id == link.document_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Document is already linked to this RRR"
        )

    new_link = RRRDocument(
        rrr_id=link.rrr_id,
        document_id=link.document_id
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return new_link


@router.get("/", response_model=list[RRRDocumentResponse])
def get_rrr_documents(db: Session = Depends(get_db)):
    return db.query(RRRDocument).all()