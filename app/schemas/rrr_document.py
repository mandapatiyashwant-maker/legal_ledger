from pydantic import BaseModel


class RRRDocumentCreate(BaseModel):
    rrr_id: int
    document_id: int


class RRRDocumentResponse(BaseModel):
    id: int
    rrr_id: int
    document_id: int

    class Config:
        from_attributes = True