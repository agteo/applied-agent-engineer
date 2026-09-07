# StrongBench RL Framing

## State

The state is the StrongBench Finance simulator state: employees, managers, policies, receipts, trips, drafts, approval requests, submitted reports, and audit log.

## Actions

`search_policy`, `lookup_receipt`, `get_employee_profile`, `create_reimbursement_draft`, `request_manager_approval`, `submit_reimbursement`, and `final_answer`.

## Observations

Each action emits an audit event with the action, success flag, and structured observation payload.

## Reward

Reward is the sum of verifier-derived components from the Level 6 environment. It includes task success, policy basis, checked records, approval correctness, contract validity, invalid tool penalties, and unauthorized submission penalties.

## Termination

A rollout terminates when the policy emits `final_answer` or the runner truncates a rollout that cannot produce one.

## Policy Under Optimization

The policy maps observations and task context to the next simulator action. This Phase 7 bundle compares a scripted reference policy to a deliberately weak submitter policy; it does not claim trained-policy improvement.
