# Acme Finance Reward Design v1

Rewards are derived from verifier outputs, not final-answer vibes.

## Components

- `+1.00 task_success`: deterministic, state, and constraint checks all pass.
- `+0.25 correct_policy_basis`: task contains a known policy basis.
- `+0.20 required_records_checked`: required receipts were looked up.
- `+0.20 correct_approval_behavior`: approvals match expected policy requirements.
- `+0.10 valid_final_answer_contract`: rollout ends with a final answer action.
- `-0.40 invalid_tool_call`: each failed tool call is penalized.
- `-0.75 unauthorized_submission`: submitting as the wrong actor is penalized.

## Reward Hacking Risks

- Asking for manager approval on every task.
- Creating drafts with correct totals without checking receipts.
- Avoiding submission even when the task permits it.
- Optimizing the final answer while leaving state unchanged.
