"""Boundary-validation pattern for external input: 3rd-party API responses,
CSV ingestion, request bodies.

Mirrors templates/go/schema/example.go and templates/typescript/schemas/
example.ts — same role, Pydantic v2 as the validation layer (the Python
analogue of Zod). Unlike the Go overlay's hand-written Validate() (chosen
there specifically to avoid struct-tag reflection an LLM can hallucinate),
Pydantic's field/model validators are the idiomatic and battle-tested choice
in Python — the risk Go avoids by hand-writing does not apply the same way
here, since Pydantic's validation surface is itself schema-driven and
type-checked by mypy through the pydantic mypy plugin.

RULE: never pass a raw external value (a request body, a CSV cell, an API
response) into business logic. Parse it into a Raw* model, let Pydantic
validate it at construction time (validation is not optional — a Pydantic
model cannot exist in an invalid state), and only then convert into a
domain type.

UNKNOWN-FIELD POLICY — strict for input you control, lenient for input you
don't (identical doctrine to the Go/TS overlays' schema templates):
  - EXTERNAL, 3rd-party input (an API/feed you do NOT own): TOLERATE unknown
    fields — model_config = ConfigDict(extra="ignore"). Such providers add
    fields without versioning; rejecting them turns a benign upstream
    addition into an outage. Correctness comes from field validators
    asserting the fields you depend on, not from forbidding fields you
    ignore.
  - INTERNAL, trusted input (your own client/frontend, your own services):
    be STRICT — model_config = ConfigDict(extra="forbid"). There an unknown
    field is a bug on your side and should fail loudly (equivalent to the
    Go overlay's dec.DisallowUnknownFields() and Zod's .strict()).

RawPlayerRecord below models a 3rd-party API (external), so it is lenient.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class RawPlayerRecord(BaseModel):
    """Shape of one player record as it arrives from a 3rd-party API.

    Salary arrives as a string in the source feed (providers commonly encode
    numbers as strings) — parse it, don't assume the wire type matches the
    domain type.
    """

    model_config = ConfigDict(extra="ignore")  # external: tolerate unknown fields

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
        if not stripped.isdigit():
            raise ValueError(f"player id {value!r} is not numeric")
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
            raise ValueError(f"salary {value!r} is not numeric")
        return stripped


def _is_numeric(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


class InternalPlayerUpdate(BaseModel):
    """Shape of a player-update request from OUR OWN frontend/service.

    Internal + trusted → strict: an unknown field here is a bug on our side
    (a client sending a stale/typo'd field) and should fail loudly rather
    than being silently dropped.
    """

    model_config = ConfigDict(extra="forbid")  # internal: reject unknown fields

    player_id: str
    new_position: str
