from datetime import datetime
from typing import Literal

from pydantic import BaseModel


MutationState = Literal[
    "DRAFT",
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

    state: MutationState = "DRAFT"

    reason: str

    valid_from: datetime | None = None

    valid_to: datetime | None = None


class MutationResponse(BaseModel):
    id: int

    baunit_id: int

    old_party_id: int

    new_party_id: int

    document_id: int | None

    state: MutationState

    reason: str | None

    rejection_reason: str | None

    valid_from: datetime | None

    valid_to: datetime | None

    recorded_at: datetime

    class Config:
        from_attributes = True