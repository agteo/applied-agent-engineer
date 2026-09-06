# Acme Model Improvement Decision Memo

## Decision

fix_tools_and_retrieval_before_training

## Evidence

- Level 2 benchmark success_rate: 0.890
- release threshold: 0.720
- benchmark gate passed: true
- Level 4 cleaned rows: 152
- SFT export train/dev rows: 78/47
- SFT rejected rows: 27
- tool or retrieval failure labels: 49
- model failure labels: 13

## Rationale

The benchmark clears the release gate, and the dominant annotated failures are tool or retrieval related. Use the SFT export for Track 5B rehearsal, but do not claim model improvement until tool behavior is fixed and a heldout benchmark comparison improves.

## Next Experiment

Improve receipt lookup arguments and rerun the Level 2 benchmark before any LoRA run.

## Adoption Gate

Adopt a trained or local model only if heldout benchmark success improves without increasing unsafe submission failures.
