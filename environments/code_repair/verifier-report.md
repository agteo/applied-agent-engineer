# Code Repair Environment Verifier Report

- tasks: 60 (60 distinct)
- rollouts: 60
- tool_count: 5
- verifier_types: deterministic, state, constraint

## Policy comparison

| Policy | Success rate | Average reward | Fabricated test claims |
| --- | ---: | ---: | ---: |
| scripted_reference | 1.000 | 1.950 | 0 |
| reward_hacker | 0.000 | -1.700 | 60 |

The reward-hacking probe is caught on 60 of 60 rollouts (1.000).
