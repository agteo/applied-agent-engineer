# StrongBench Model Comparison Report

## Current Evidence

- scripted baseline success_rate: 0.890
- release threshold: 0.720
- benchmark passed: true
- SFT train/dev rows: 78/47

## Comparison Table

| Candidate | Evidence Status | Decision |
| --- | --- | --- |
| Current scripted/tool baseline | Measured on 100 tasks | Keep as baseline gate |
| Tool and retrieval fixes | Supported by Phase 3 failure labels | Build next |
| Small LoRA/SFT adapter | Data prepared, no training run yet | Defer adoption claim |
| Frontier or hybrid API | Not measured in offline course path | Optional comparison |

## Recommendation

The benchmark clears the release gate, and the dominant annotated failures are tool or retrieval related. Use the SFT export for Track 5B rehearsal, but do not claim model improvement until tool behavior is fixed and a heldout benchmark comparison improves.
