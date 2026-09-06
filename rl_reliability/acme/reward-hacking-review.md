# Reward Hacking Review

## Observed Risk

The weak submitter policy produced 120 unsafe submission failures. That is the clearest exploit target: chasing terminal actions without respecting actor and approval constraints.

## Exploits And Mitigations

| Exploit | Detection | Mitigation |
| --- | --- | --- |
| Submit every draft | unsafe submission failure count | Keep `unauthorized_submission` penalty and Level 2 unsafe slice gate |
| Ask approval for everything | approval overuse count | Score approval correctness, not approval presence |
| Skip receipt lookup but write right-looking totals | required records checked | Require receipt ids in observations |
| Optimize final-answer shape only | state draft and submission checks | Reward state verifiers before answer format |
| Memorize fixture ids | heldout task success | Keep heldout simulator tasks and Level 2 benchmark regression check |
