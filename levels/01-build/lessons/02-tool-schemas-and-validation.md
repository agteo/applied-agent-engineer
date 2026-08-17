# Lesson 2: Tool Schemas and Validation

## Core Idea

Tools are contracts. The agent should never execute vague, malformed, or unsafe tool calls.

The model may propose a tool call, but the harness decides whether that call is valid.

## Tool Contract

Every tool should define:

- name
- purpose
- input schema
- output shape
- possible errors
- permission level

## Validation Responsibilities

The harness should validate:

- required fields
- field types
- enum values
- date formats
- numeric ranges
- unknown fields
- permissions

## Example

```json
{
  "name": "calculate_reimbursement",
  "input_schema": {
    "type": "object",
    "properties": {
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "category": {
              "type": "string",
              "enum": ["meal", "travel", "lodging", "parking", "other"]
            },
            "amount": { "type": "number", "minimum": 0 }
          },
          "required": ["category", "amount"]
        }
      }
    },
    "required": ["items"]
  }
}
```

## Design Rule

Validation errors should become observations. They should not crash the whole run unless the error is unrecoverable.

## Checkpoint

You are ready to move on when invalid tool arguments are rejected before execution and the agent can recover from the validation message.

