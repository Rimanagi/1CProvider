from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TypicalDefect(BaseModel):
    guid: UUID = Field(validation_alias="GUIDTypicalDefect")
    code: str = Field(validation_alias="Code")
    name: str = Field(validation_alias="TypicalDefect")


class DefectCause(BaseModel):
    guid: UUID = Field(validation_alias="GUIDTitle")
    code: str = Field(validation_alias="Code")
    name: str = Field(validation_alias="TheCauseOfTheDefect")


class RepairFacility(BaseModel):
    guid: UUID = Field(validation_alias="GUIDRepairObject")
    code: str = Field(validation_alias="CodeRepairObject")
    name: str = Field(validation_alias="RepairObject")
    parent_guid: UUID | None = Field(default=None, validation_alias="GUIDParent")
    parent_code: str | None = Field(default=None, validation_alias="CodeParent")
    parent_name: str | None = Field(default=None, validation_alias="Parent")

    @field_validator("parent_guid", "parent_code", "parent_name", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        return value or None


class Defect(BaseModel):
    defect_type_id: UUID
    defect_reason_id: UUID
    equipment_id: UUID
    server_defect_id: str
    detected_at: datetime
    comment: str


class Walker(BaseModel):
    person_number: str
    full_name: str


class DefectUsers(BaseModel):
    walker: Walker


class Transfer(BaseModel):
    idempotency_id: str
    transferred_at: datetime
    payload_sha256: Annotated[str, Field(pattern=r"^[a-fA-F0-9]{64}$")]


class IdentifiedDefect(BaseModel):
    defect: Defect
    users: DefectUsers
    transfer: Transfer
