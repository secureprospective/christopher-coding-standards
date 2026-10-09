"""Shipped shape oracles and a synthetic effect boundary; not auth/persistence."""

import pytest
from pydantic import ValidationError

from schema.example import InternalPlayerUpdate, RawPlayerRecord


def test_valid_provider_normalization_and_unknown_fields() -> None:
    rec = RawPlayerRecord.model_validate(
        {"id": " 0099 ", "name": " Chris ", "position": " QB ", "salary": " 1.5 ", "new": True}
    )
    assert (rec.id, rec.name, rec.position, rec.salary) == ("0099", "Chris", "QB", "1.5")
    assert "new" not in rec.model_dump()
    assert RawPlayerRecord(id="0", name="Chris", position="QB").salary == ""


@pytest.mark.parametrize("field", ["id", "name", "position"])
@pytest.mark.parametrize("value", ["", " ", None, 42, True])
def test_invalid_required_field(field: str, value: object) -> None:
    data: dict[str, object] = {"id": "99", "name": "Chris", "position": "QB"}
    data[field] = value
    with pytest.raises(ValidationError):
        RawPlayerRecord.model_validate(data)


@pytest.mark.parametrize("value", ["-99", "+99", "９９", "²", "9x", "1 2"])
def test_invalid_numeric_id(value: str) -> None:
    with pytest.raises(ValidationError):
        RawPlayerRecord(id=value, name="Chris", position="QB")


@pytest.mark.parametrize("salary", ["NaN", "Inf", "-Infinity", "1e999", "bad"])
def test_invalid_salary(salary: str) -> None:
    with pytest.raises(ValidationError):
        RawPlayerRecord(id="99", name="Chris", position="QB", salary=salary)


@pytest.mark.parametrize("salary", ["", " ", "-1", "1e3", "1.5"])
def test_valid_salary(salary: str) -> None:
    rec = RawPlayerRecord(id="99", name="Chris", position="QB", salary=salary)
    assert rec.salary == salary.strip()


def test_owned_update_policy_and_json() -> None:
    update = InternalPlayerUpdate.model_validate_json('{"player_id":" 99 ","new_position":" QB "}')
    assert (update.player_id, update.new_position) == ("99", "QB")
    assert InternalPlayerUpdate.model_validate(update.model_dump()) == update
    for bad in [
        '{"player_id":"99","new_position":"QB","extra":true}',
        '{"player_id":"-99","new_position":"QB"}',
        '{"player_id":"99","new_position":" "}',
        "null",
        '{"player_id":"99","new_position":"QB"}{}',
    ]:
        with pytest.raises(ValidationError):
            InternalPlayerUpdate.model_validate_json(bad)


def test_assignment_and_documented_bypass() -> None:
    rec = RawPlayerRecord(id="99", name="Chris", position="QB")
    rec.name = " New "
    assert rec.name == "New"
    with pytest.raises(ValidationError):
        rec.id = "-99"
    assert rec.id == "99"
    # These documented APIs do not run validation. Never mistake them for boundary validation.
    bypass = RawPlayerRecord.model_construct(id="invalid", name="Chris", position="QB")
    assert bypass.id == "invalid"
    copied = rec.model_copy(update={"id": "invalid"})
    assert copied.id == "invalid"


def test_synthetic_caller_rejects_before_effect() -> None:
    accepted: list[str] = []

    def receive(payload: object) -> None:
        try:
            raw = RawPlayerRecord.model_validate(payload)
        except ValidationError:
            return
        accepted.append(raw.id)

    for bad in [None, {"id": "-99", "name": "Chris", "position": "QB"}]:
        receive(bad)
    assert accepted == []
    receive({"id": " 99 ", "name": "Chris", "position": "QB"})
    assert accepted == ["99"]
