# Model Improvement: Deciding Not To Train Yet

## One-Sentence Claim

I prepared SFT-ready data from agent traces and failure corrections, then used
benchmark evidence to decide that tool and retrieval fixes should happen before
fine-tuning.

## Problem

After a dataset exists, it is tempting to train immediately. That can be the
wrong intervention if failures come from tool arguments, retrieval grounding, or
workflow boundaries rather than model answer generation.

## Measurement

- decision command: `python3 -m model_improvement.strongbench`
- LoRA dry-run command: `python3 -m model_improvement.strongbench.train_lora --dry-run`
- Level 4 cleaned rows: 152
- SFT export: 78 train rows, 47 dev rows
- heldout rows rejected from SFT: 27
- current benchmark success rate: 0.890

## Diagnosis

The Phase 5 decision bundle counted 49 tool or retrieval failure labels and 13
model failure labels. That points to system behavior, not a pure model
capability gap.

## Intervention Or Decision

Do not claim training is justified yet. Keep the LoRA config as a reproducible
optional track, but fix receipt lookup and citation behavior before spending
GPU time.

## Evidence

| Candidate | Evidence | Decision |
| --- | --- | --- |
| Current tool baseline | 0.890 benchmark success | Keep as baseline |
| Tool/retrieval fix | Dominant failure labels | Build next |
| Small LoRA/SFT | Data prepared, no run logs | Defer adoption claim |
| Frontier or hybrid API | Not measured offline | Optional comparison |

## Differentiating Choice

I would compare a local small instruct model against the scripted baseline only
on the receipt and approval slices first, then expand if it clears the safety
gate.

## What I Would Do Next

Run the receipt lookup intervention, rebuild the SFT export, and only start the
LoRA experiment if remaining failures are model-generation failures.

## Links

- [`model_improvement/strongbench/decision-memo.md`](../../model_improvement/strongbench/decision-memo.md)
- [`model_improvement/strongbench/comparison-report.md`](../../model_improvement/strongbench/comparison-report.md)
- [`model_improvement/strongbench/lora-config.template.json`](../../model_improvement/strongbench/lora-config.template.json)
- [`examples/reference-artifacts/model-improvement-decision/good.md`](../reference-artifacts/model-improvement-decision/good.md)
