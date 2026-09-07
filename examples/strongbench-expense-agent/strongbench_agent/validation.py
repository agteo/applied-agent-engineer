"""A small JSON-Schema-shaped validator.

The course deliberately does not depend on `jsonschema` here. Learners should
see exactly what "validating a tool call" means: a handful of type checks, a
required-field check, and an error message the model can actually act on.

Supported keywords: type, properties, required, enum, items, minimum,
maximum, minItems, additionalProperties, format ("date" only).
"""

from __future__ import annotations

import datetime as _dt
from typing import Any

_TYPES: dict[str, type | tuple[type, ...]] = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "null": type(None),
}


class ValidationError(ValueError):
    """Raised when tool arguments or a final answer do not match a schema."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


def _check(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected = schema.get("type")
    if expected:
        py_type = _TYPES[expected]
        # bool is a subclass of int in Python; never let it pass as a number.
        if isinstance(value, bool) and expected in {"number", "integer"}:
            errors.append(f"{path}: expected {expected}, got boolean")
            return
        if not isinstance(value, py_type):
            errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
            return

    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(repr(v) for v in schema["enum"])
        errors.append(f"{path}: {value!r} is not one of [{allowed}]")

    if schema.get("format") == "date" and isinstance(value, str):
        try:
            _dt.date.fromisoformat(value)
        except ValueError:
            errors.append(f"{path}: expected an ISO date (YYYY-MM-DD), got {value!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} is below the minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} is above the maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} item(s)")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                _check(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for field in schema.get("required", []):
            if field not in value:
                errors.append(f"{path}.{field}: required field is missing")
        if schema.get("additionalProperties") is False:
            for field in value:
                if field not in properties:
                    known = ", ".join(sorted(properties)) or "none"
                    errors.append(f"{path}.{field}: unknown field (known fields: {known})")
        for field, sub_schema in properties.items():
            if field in value:
                _check(value[field], sub_schema, f"{path}.{field}", errors)


def validate(value: Any, schema: dict[str, Any], name: str = "arguments") -> Any:
    """Validate `value` against `schema`, returning it unchanged if it passes."""
    errors: list[str] = []
    _check(value, schema, name, errors)
    if errors:
        raise ValidationError(errors)
    return value
