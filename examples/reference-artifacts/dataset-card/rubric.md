# Dataset Card Rubric

## High

A high-quality dataset card lets another engineer decide whether the dataset is
usable for the stated purpose.

Required anchors:

- Intended use and explicit non-use.
- Source counts and source types.
- Schema or contract reference.
- Cleaning rules and rejected-row summary.
- Split policy and contamination controls.
- Known limitations.

Example: [`good.md`](good.md) earns high because it gives row counts, rejection
reasons, split behavior, and a clear synthetic-data limitation.

## Medium

A medium card lists sources and intended use but omits one or more of counts,
rejection evidence, split rules, or contamination controls.

## Low

A low card says the dataset exists and is cleaned without enough evidence for a
reviewer to trust or reproduce it.

Example: [`weak.md`](weak.md) is low because it claims likely improvement while
omitting the evidence needed to support that claim.
