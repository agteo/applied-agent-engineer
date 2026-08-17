# Lesson 3: Deterministic Graders

## Core Idea

Use code when correctness can be checked with code.

Deterministic graders are cheaper, faster, and easier to debug than model-based judges.

## Good Uses

Use deterministic graders for:

- JSON schema validity
- required field presence
- numeric totals
- expected policy source ids
- approval required vs not required
- tool called vs not called
- tool argument shape
- max latency
- max cost

## Example Grades

```json
{
  "task_id": "expense-042",
  "grades": {
    "valid_json": true,
    "correct_total": true,
    "required_approval_identified": false,
    "policy_sources_present": true
  }
}
```

## Common Mistakes

- Grading prose with brittle string matching.
- Requiring exact wording when meaning matters.
- Treating partial correctness as all-or-nothing.
- Ignoring tool traces.
- Failing closed without useful error messages.

## Checkpoint

You are ready to move on when your benchmark has deterministic graders for all fields with objective expected answers.

