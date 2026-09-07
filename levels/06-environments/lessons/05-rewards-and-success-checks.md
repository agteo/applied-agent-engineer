# Lesson 5: Rewards and Success Checks

## Core Idea

Success checks decide whether the task was completed. Rewards shape what behavior is preferred.

## Success Checks

Use deterministic success checks when possible:

- correct reimbursable total
- required approval requested
- unsafe submission avoided
- policy citation included
- draft created with correct items

## Reward Design

Rewards can include:

- task completion
- correct tool use
- safe approval behavior
- concise interaction
- penalty for invalid actions
- penalty for unsafe side effects

## Warning

Reward design can create shortcuts. If the reward misses an important behavior, the agent may learn to exploit the gap.

## Common Failure Modes

- Rewarding final-answer format while state is wrong.
- Giving approval credit for approving everything.
- Using one opaque scalar with no component breakdown.

## Exercise

Name three reward components from the StrongBench simulator.

Check your answer:

```text
`task_success`, `required_records_checked`, `correct_approval_behavior`, `valid_final_answer_contract`, and penalties such as `unauthorized_submission`.
```

Use the StrongBench Finance rollout to confirm the answer against the environment simulator rather than relying on memory.

## Checkpoint

You are ready to move on when each reward component maps to a behavior you actually care about.
