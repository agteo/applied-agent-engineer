# StrongBench Finance Simulator Verifier Report

- tasks: 120 (120 distinct)
- rollouts: 120
- tool_count: 7
- verifier_types: deterministic, state, constraint, model_based

## Policy comparison

| Policy | Success rate | Average reward | Distinct rewards |
| --- | ---: | ---: | ---: |
| scripted_reference | 1.000 | 1.900 | 1 |
| reward_hacker | 0.000 | -0.815 | 4 |

The reward-hacking probe is caught on 120 of 120 rollouts (1.000).

A reference policy passing every task only means the contract is coherent. The probe row is
the one that shows the verifiers discriminate. Level 7 should add learned policies before
making any reward-learning claim.
