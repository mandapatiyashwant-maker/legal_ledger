from pydantic import BaseModel


class PartyCreate(BaseModel):
    name: str
    party_type: str


class PartyResponse(BaseModel):
    id: int
    name: str
    party_type: str

    class Config:
        from_attributes = True