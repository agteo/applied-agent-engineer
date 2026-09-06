# Eval Report Rubric

## High

A high-quality eval report makes a release decision and defends it with
benchmark evidence.

Required anchors:

- Names the benchmark task set and command.
- Reports overall success, per-tag success, safety behavior, cost or latency,
  and judge calibration.
- Quotes or summarizes specific failed task ids.
- Separates benchmark failures from suspected agent, tool, retrieval, or grader
  causes.
- Recommends an intervention order.

Example: [`good.md`](good.md) earns high because it cites the 89/100 result,
the 3/10 receipt lookup slice, and the specific room-service and approval
failures before recommending fixes.

## Medium

A medium report includes the main metrics and a plausible recommendation, but
does not fully connect failures to trace evidence or interventions.

Typical gaps:

- Per-tag numbers are missing.
- Failure labels are too broad.
- The release recommendation is present but not tied to the threshold.

## Low

A low-quality report gives a vibe instead of a defensible release decision.

Example: [`weak.md`](weak.md) is low because it says the agent did well without
naming the pass rate, threshold, failed tags, or safety risk. It recommends
shipping despite missing the evidence a reviewer needs.

