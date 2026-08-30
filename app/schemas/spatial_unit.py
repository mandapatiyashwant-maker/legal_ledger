from datetime import datetime

from pydantic import BaseModel, field_validator


ALLOWED_UNIT_TYPES = {
    "PARCEL",
    "BUILDING",
    "FLOOR",
    "APARTMENT",
    "COMMERCIAL_UNIT",
    "PARKING",
    "BASEMENT",
    "UTILITY",
    "AIR_RIGHT",
    "COMMON_AREA",
    "OTHER_3D_SPACE",
}


ALLOWED_CONFIDENCE_LEVELS = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


ALLOWED_VALIDATION_STATUSES = {
    "PENDING_VERIFICATION",
    "VALID",
    "VERIFIED",
    "INVALID",
}


ALLOWED_SEGMENTATION_METHODS = {
    "derived_from_storey_count",
    "surveyed",
    "bim",
    "floor_plan",
    "manual",
    "other",
}


class SpatialUnitCreate(BaseModel):

    ulpin_3d: str

    parent_ulpin: str | None = None

    parent_spatial_unit_id: int | None = None

    building_id: str | None = None

    source_building_id: str | None = None

    unit_type: str

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

    validation_status: str | None = None

    effective_from: datetime | None = None

    effective_to: datetime | None = None

    status: str = "ACTIVE"

    @field_validator("unit_type")
    @classmethod
    def validate_unit_type(cls, value):

        value = value.upper()

        if value not in ALLOWED_UNIT_TYPES:
            raise ValueError(
                f"Invalid unit_type. "
                f"Allowed values: {sorted(ALLOWED_UNIT_TYPES)}"
            )

        return value

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value):

        if value is None:
            return value

        value = value.upper()

        if value not in ALLOWED_CONFIDENCE_LEVELS:
            raise ValueError(
                f"Invalid confidence. "
                f"Allowed values: "
                f"{sorted(ALLOWED_CONFIDENCE_LEVELS)}"
            )

        return value

    @field_validator("validation_status")
    @classmethod
    def validate_validation_status(cls, value):

        if value is None:
            return value

        value = value.upper()

        if value not in ALLOWED_VALIDATION_STATUSES:
            raise ValueError(
                f"Invalid validation_status. "
                f"Allowed values: "
                f"{sorted(ALLOWED_VALIDATION_STATUSES)}"
            )

        return value

    @field_validator("segmentation_method")
    @classmethod
    def validate_segmentation_method(cls, value):

        if value is None:
            return value

        if value not in ALLOWED_SEGMENTATION_METHODS:
            raise ValueError(
                f"Invalid segmentation_method. "
                f"Allowed values: "
                f"{sorted(ALLOWED_SEGMENTATION_METHODS)}"
            )

        return value


class SpatialUnitResponse(BaseModel):

    id: int

    ulpin_3d: str

    parent_ulpin: str | None

    parent_spatial_unit_id: int | None

    building_id: str | None

    source_building_id: str | None

    unit_type: str

    floor_number: int | None

    z_min: float | None

    z_max: float | None

    area_2d: float | None

    volume_3d: float | None

    geometry_version: int

    geometry_hash: str | None

    geometry_source: str | None

    segmentation_method: str | None

    confidence: str | None

    validation_status: str | None

    effective_from: datetime | None

    effective_to: datetime | None

    status: str

    created_at: datetime | None

    updated_at: datetime | None

    class Config:
        from_attributes = True