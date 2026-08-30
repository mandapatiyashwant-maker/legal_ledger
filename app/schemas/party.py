from pydantic import BaseModel


class PartyCreate(BaseModel):

    name: str

    party_type: str

    is_demo_record: bool = True

    demo_reference: str | None = None


class PartyResponse(BaseModel):

    id: int

    name: str

    party_type: str

    is_demo_record: bool

    demo_reference: str | None

    class Config:
        from_attributes = True