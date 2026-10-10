"""Explicit shape boundary before domain conversion/effects, not permission.

Provider fields may expand (ignore extras); owned client updates forbid extras,
not trust their sender. Validation runs through constructors/model_validate;
model_construct, unvalidated model_copy updates or direct object manipulation
can bypass it. Assignment validation does not make impossible states impossible.
Set request/resource limits and redact errors before logging separately.
"""

from __future__ import annotations

import math

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RawPlayerRecord(BaseModel):
    """Provider strings normalized; unknown fields intentionally ignored."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)

    id: str
    name: str
    position: str
    salary: str = ""

    @field_validator("id")
    @classmethod
    def id_must_be_numeric_string(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("player record missing id")
        if not stripped.isascii() or not stripped.isdigit():
            raise ValueError("player id must be an unsigned ASCII decimal")
        return stripped

    @field_validator("name", "position")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field must not be blank")
        return value.strip()

    @field_validator("salary")
    @classmethod
    def salary_must_be_numeric_if_present(cls, value: str) -> str:
        stripped = value.strip()
        if stripped and not _is_numeric(stripped):
            raise ValueError("salary must be a finite number when present")
        return stripped


def _is_numeric(value: str) -> bool:
    try:
        return math.isfinite(float(value))
    except ValueError:
        return False


class InternalPlayerUpdate(BaseModel):
    """Owned client shape; unknown/blank/invalid IDs rejected, not authorization."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, validate_assignment=True)

    player_id: str = Field(min_length=1, pattern=r"^[0-9]+$")
    new_position: str = Field(min_length=1)
