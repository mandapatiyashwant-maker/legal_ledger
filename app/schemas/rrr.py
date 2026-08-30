from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


RRRType = Literal[
    "OWNERSHIP",
    "LEASE",
    "ACCESS_RIGHT",
    "AIR_RIGHT",
    "MORTGAGE",
    "HERITAGE_RESTRICTION",
    "HEIGHT_RESTRICTION",
    "COURT_DISPUTE",
    "MAINTENANCE",
    "PROPERTY_TAX",
    "UTILITY_ACCESS"
]


RRRStatus = Literal[
    "ACTIVE",
    "EXPIRED",
    "CANCELLED",
    "PENDING"
]


class RRRCreate(BaseModel):

    party_id: int

    spatial_unit_id: int

    rrr_type: RRRType

    subtype: str | None = None

    share: int | None = Field(
        default=None,
        ge=0,
        le=100
    )

    start_date: date | None = None

    end_date: date | None = None

    source_document_id: int | None = None

    status: RRRStatus = "ACTIVE"

    priority: int | None = Field(
        default=None,
        ge=0
    )

    notes: str | None = None

    description: str | None = None


class RRRResponse(BaseModel):

    id: int

    party_id: int

    spatial_unit_id: int

    rrr_type: RRRType

    subtype: str | None

    share: int | None

    start_date: date | None

    end_date: date | None

    source_document_id: int | None

    status: RRRStatus

    priority: int | None

    notes: str | None

    description: str | None

    class Config:
        from_attributes = True