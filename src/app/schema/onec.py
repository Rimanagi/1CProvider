from uuid import UUID

from pydantic import BaseModel, Field


class TypicalDefect(BaseModel):
    guid: UUID = Field(validation_alias="GUIDTypicalDefect")
    code: str = Field(validation_alias="Code")
    name: str = Field(validation_alias="TypicalDefect")


class DefectCause(BaseModel):
    guid: UUID = Field(validation_alias="GUIDTitle")
    code: str = Field(validation_alias="Code")
    name: str = Field(validation_alias="TheCauseOfTheDefect")