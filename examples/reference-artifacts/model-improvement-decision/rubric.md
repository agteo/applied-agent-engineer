# Model Improvement Decision Rubric

## High

A high-quality decision memo chooses an intervention and rules out alternatives
using benchmark, trace, and dataset evidence.

Required anchors:

- States the decision clearly.
- Names current benchmark performance.
- Links failure modes to likely intervention types.
- Explains why training is or is not justified.
- Defines the next measurement.

Example: [`good.md`](good.md) earns high because it uses the 89/100 result and
the failure taxonomy to choose tool fixes before fine-tuning.

## Medium

A medium memo makes a plausible intervention choice but gives incomplete
evidence or a weak success criterion.

## Low

A low memo chooses training because training is available.

Example: [`weak.md`](weak.md) is low because it assumes the dataset proves a
fine-tune is warranted and does not name a benchmark gate.
