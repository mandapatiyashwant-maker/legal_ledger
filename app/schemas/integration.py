from datetime import datetime

from pydantic import BaseModel, Field


class SpatialUnitRegistrationRequest(BaseModel):

    ulpin3d: str = Field(
        min_length=1
    )

    parent_ulpin: str | None = None

    unit_type: str

    building_id: str | None = None

    source_building_id: str | None = None

    floor_number: int | None = None

    z_min: float | None = None

    z_max: float | None = None

    area_2d: float | None = None

    volume_3d: float | None = None

    geometry_version: int

    geometry_hash: str | None = None

    geometry_source: str | None = None

    segmentation_method: str | None = None

    confidence: str | None = None

    validation_status: str

    effective_from: datetime | None = None

    effective_to: datetime | None = None


class SpatialUnitRegistrationResponse(BaseModel):

    id: int

    ulpin3d: str

    parent_ulpin: str | None

    unit_type: str

    building_id: str | None

    source_building_id: str | None

    floor_number: int | None

    geometry_version: int

    geometry_hash: str | None

    validation_status: str | None

    status: str

    message: str

    class Config:
        from_attributes = True