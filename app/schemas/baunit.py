from pydantic import BaseModel


class BAUnitCreate(BaseModel):
    baunit_number: str
    spatial_unit_id: int
    status: str = "ACTIVE"
    description: str | None = None


class BAUnitResponse(BaseModel):
    id: int
    baunit_number: str
    spatial_unit_id: int
    status: str
    description: str | None

    class Config:
        from_attributes = True