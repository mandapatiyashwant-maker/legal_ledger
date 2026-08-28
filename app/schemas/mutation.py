from pydantic import BaseModel
from typing import Literal


MutationState = Literal[
    "SUBMITTED",
    "UNDER_REVIEW",
    "APPROVED",
    "REJECTED",
    "REGISTERED",
    "SUPERSEDED"
]


class MutationCreate(BaseModel):
    baunit_id: int
    old_party_id: int
    new_party_id: int
    document_id: int | None = None
    reason: str


class MutationResponse(BaseModel):
    id: int
    baunit_id: int
    old_party_id: int
    new_party_id: int
    document_id: int | None
    state: MutationState
    reason: str
    rejection_reason: str | None

    class Config:
        from_attributes = True