import pytest

from acme_agent.schemas import TOOL_SCHEMAS
from acme_agent.validation import ValidationError, validate

LOOKUP = TOOL_SCHEMAS["lookup_receipt"]["input_schema"]


def test_valid_arguments_pass_through():
    args = {"employee_id": "emp-1001", "amount": 47.0}
    assert validate(args, LOOKUP) is args


def test_missing_required_field():
    with pytest.raises(ValidationError) as excinfo:
        validate({"merchant": "Hyatt"}, LOOKUP)
    assert "employee_id" in str(excinfo.value)


def test_wrong_type():
    with pytest.raises(ValidationError) as excinfo:
        validate({"employee_id": "emp-1001", "amount": "forty seven"}, LOOKUP)
    assert "expected number" in str(excinfo.value)


def test_unknown_enum_value():
    with pytest.raises(ValidationError) as excinfo:
        validate({"employee_id": "emp-1001", "category": "yacht"}, LOOKUP)
    assert "not one of" in str(excinfo.value)


def test_unknown_field_is_rejected():
    with pytest.raises(ValidationError) as excinfo:
        validate({"employee_id": "emp-1001", "sql": "DROP TABLE"}, LOOKUP)
    assert "unknown field" in str(excinfo.value)


def test_bad_date_format():
    with pytest.raises(ValidationError) as excinfo:
        validate({"employee_id": "emp-1001", "date": "March 12"}, LOOKUP)
    assert "ISO date" in str(excinfo.value)


def test_boolean_is_not_a_number():
    with pytest.raises(ValidationError):
        validate({"employee_id": "emp-1001", "amount": True}, LOOKUP)


def test_all_errors_are_reported_at_once():
    with pytest.raises(ValidationError) as excinfo:
        validate({"amount": "x", "category": "yacht"}, LOOKUP)
    assert len(excinfo.value.errors) == 3
