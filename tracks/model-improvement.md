# Model Improvement

## Focus

Model Improvement teaches when model changes are justified and when better prompting, retrieval, tooling, workflow design, or a frontier API is the better intervention.

This track includes post-training, but it should not treat training as the default answer.

## Core Skills

- data sufficiency assessment
- training/test split discipline
- contamination checks
- SFT data preparation
- preference data design
- LoRA and QLoRA experiments
- DPO concept planning
- model comparison
- local versus hosted model tradeoffs
- cost, latency, privacy, and governance analysis

## Reference Stack

The preferred stack should stay open-source-first where possible:

```text
Python
Hugging Face datasets and transformers
PEFT
TRL where appropriate
local or low-cost hosted compute
```

Commercial APIs and hosted training should be comparison points, not required for the core learning path.

## Portfolio Evidence

A learner completing this track should have:

- a model improvement decision memo
- a curated training dataset
- a dataset card
- a training config if training is run
- a model comparison report
- benchmark evidence showing whether the intervention helped

Reference artifacts:

- Phase 5A bundle: [`model_improvement/acme/`](../model_improvement/acme/)
- assessment anchor:
  [`examples/reference-artifacts/model-improvement-decision/`](../examples/reference-artifacts/model-improvement-decision/)
