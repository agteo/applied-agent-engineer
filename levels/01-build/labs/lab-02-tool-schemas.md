# Lab 2: Tool Schemas

## Objective

Turn informal tool calls into validated tool calls.

## Build

Add schemas for three tools:

1. `calculate_reimbursement`
2. `lookup_receipt`
3. `search_policy`

Each schema should define required fields, optional fields, allowed values, and error behavior.

## Example Schema

```json
{
  "name": "lookup_receipt",
  "description": "Look up a receipt by employee id, merchant, date, or amount.",
  "input_schema": {
    "type": "object",
    "properties": {
      "employee_id": { "type": "string" },
      "merchant": { "type": "string" },
      "date": { "type": "string", "format": "date" },
      "amount": { "type": "number" }
    },
    "required": ["employee_id"]
  }
}
```

## Failure Cases

Create tests for invalid tool arguments:

- missing required field
- wrong type
- unknown enum value
- ambiguous lookup

## Deliverable

Submit:

- tool schema definitions
- validation code
- passing and failing test examples
- traces showing how validation errors are returned to the agent

## Checks

The lab passes if invalid tool arguments do not execute the tool and the agent receives a clear validation error.

