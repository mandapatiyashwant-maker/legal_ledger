from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document import Document
from app.models.baunit import BAUnit
from app.schemas.document import DocumentCreate, DocumentResponse


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    baunit = db.query(BAUnit).filter(
        BAUnit.id == document.baunit_id
    ).first()

    if not baunit:
        raise HTTPException(
            status_code=404,
            detail="BAUnit not found"
        )

    existing = db.query(Document).filter(
        Document.document_number == document.document_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Document number already exists"
        )

    new_document = Document(
        document_number=document.document_number,
        document_type=document.document_type,
        baunit_id=document.baunit_id,
        document_date=document.document_date,
        issuing_authority=document.issuing_authority,
        status=document.status,
        description=document.description
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


@router.get("/", response_model=list[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()