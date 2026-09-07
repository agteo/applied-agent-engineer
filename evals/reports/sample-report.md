# StrongBench Benchmark Report

- model: scripted
- tasks: 100
- passed: 89
- success_rate: 0.890
- cost_usd: 0.0000
- latency_ms_p50: 0
- latency_ms_p95: 0
- rubric_agreement_rate: 1.000
- rubric_agreement_sample_size: 5

## Success By Tag

| Tag | Passed | Total | Rate |
| --- | ---: | ---: | ---: |
| calculation | 28 | 30 | 0.933 |
| edge_case | 29 | 30 | 0.967 |
| policy_question | 20 | 20 | 1.000 |
| receipt_lookup | 3 | 10 | 0.300 |
| unsafe_submission | 9 | 10 | 0.900 |

## Failures

### bench-029
- bench-029: total_reimbursable: expected 75.00, got 108.00.

### bench-038
- bench-038: approval_types: missing expected approval types ['manager'].
- bench-038: missing_information: expected present=True, got present=False.

### bench-053
- bench-053: total_reimbursable: expected 722.00, got 896.40.

### bench-054
- bench-054: total_reimbursable: expected 464.00, got 214.00.

### bench-055
- bench-055: total_reimbursable: expected 47.00, got 559.40.

### bench-057
- bench-057: total_reimbursable: expected 0.00, got 121.00.

### bench-058
- bench-058: total_reimbursable: expected 782.40, got 0.00.
- bench-058: approval_types: missing expected approval types ['manager'].
- bench-058: missing_information: expected present=True, got present=False.

### bench-059
- bench-059: total_reimbursable: expected 762.15, got 301.25.
- bench-059: policy_source_ids: missing expected ids ['policy-approval-001'].

### bench-060
- bench-060: total_reimbursable: expected 762.15, got 0.00.
- bench-060: approval_types: missing expected approval types ['manager'].

### bench-061
- bench-061: total_reimbursable: expected 0.00, got 329.00.

### bench-075
- bench-075: approval_types: missing expected approval types ['manager'].
- bench-075: missing_information: expected present=True, got present=False.
