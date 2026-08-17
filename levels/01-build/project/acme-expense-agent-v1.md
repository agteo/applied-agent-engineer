# Project: Acme Expense Agent v1

## Objective

Build the first version of the canonical course agent.

The agent helps employees reason about expense reimbursement using policy search, receipt lookup, calculation, and approval gating.

## Required Capabilities

The agent must:

1. Answer expense-policy questions using retrieved policy snippets.
2. Look up simulated receipt records.
3. Calculate reimbursable totals.
4. Identify missing information.
5. Identify expenses that require manager approval.
6. Ask for human approval before preparing an action with external or financial consequences.
7. Return a structured final answer.
8. Save traces for every run.

## Required Tools

### `search_policy`

Find relevant policy sections.

### `lookup_receipt`

Retrieve simulated receipt records.

### `calculate_reimbursement`

Calculate totals, limits, and non-reimbursable amounts.

### `request_human_approval`

Ask whether the agent is allowed to prepare or submit a recommendation.

In Level 1, this may be a simulated local function.

## Final Answer Contract

The final answer should follow this shape:

```json
{
  "summary": "Short human-readable answer.",
  "reimbursable_items": [
    {
      "description": "Airport parking",
      "amount": 47.0,
      "policy_source_ids": ["policy-travel-002"]
    }
  ],
  "non_reimbursable_items": [],
  "missing_information": [],
  "approvals_required": [
    {
      "approval_type": "manager",
      "reason": "Missing hotel receipt"
    }
  ],
  "total_reimbursable": 47.0,
  "confidence": "medium",
  "next_action": "Ask manager to approve exception for missing hotel receipt."
}
```

## Example Tasks

Use these tasks while developing:

1. "I spent $47 on airport parking and $68 on dinner during a customer trip. What can I reimburse?"
2. "I lost my hotel receipt for a $214 stay. Can I still submit it?"
3. "Find the receipt for my Denver dinner last Thursday and tell me whether it is within policy."
4. "Prepare a reimbursement recommendation for my trip with parking, dinner, and hotel expenses."
5. "Can you submit this reimbursement for me?"

## Constraints

- Do not connect to real financial systems.
- Do not use real employee data.
- Do not submit real reimbursements.
- Do not let the model execute arbitrary code.
- Do not continue beyond the maximum step count.

## Evaluation Preview

Level 2 will evaluate this project on:

- task success
- policy citation accuracy
- tool-call correctness
- structured output validity
- cost
- latency
- failure rate

## Submission Checklist

- [ ] Agent runs locally.
- [ ] At least three tools are implemented.
- [ ] Tool arguments are validated.
- [ ] Final answers follow the contract.
- [ ] Policy citations are included.
- [ ] Human approval is used for risky actions.
- [ ] At least 20 traces are saved.
- [ ] Known limitations are documented.

