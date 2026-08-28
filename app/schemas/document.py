from pydantic import BaseModel


class DocumentCreate(BaseModel):
    document_number: str
    document_type: str
    baunit_id: int
    document_date: str | None = None
    issuing_authority: str | None = None
    status: str = "VALID"
    description: str | None = None


class DocumentResponse(BaseModel):
    id: int
    document_number: str
    document_type: str
    baunit_id: int
    document_date: str | None
    issuing_authority: str | None
    status: str
    description: str | None

    class Config:
        from_attributes = True