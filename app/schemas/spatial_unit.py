from pydantic import BaseModel


class SpatialUnitCreate(BaseModel):
    ulpin_3d: str
    unit_type: str
    geometry_version: int
    geometry_hash: str | None = None
    conflict_status: str = "NO_CONFLICT"
    effective_time: str | None = None


class SpatialUnitResponse(BaseModel):
    id: int
    ulpin_3d: str
    unit_type: str
    geometry_version: int
    geometry_hash: str | None
    conflict_status: str
    effective_time: str | None

    class Config:
        from_attributes = True