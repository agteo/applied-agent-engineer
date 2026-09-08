# Lesson 1: When To Train

## Core Idea

Fine-tuning is one intervention among several, and usually not the first one
worth trying. It is slow, expensive, hard to reverse, and it changes the
component that is hardest to debug.

The decision is not "is the agent good enough?" It is **"where do the failures
live?"** An agent fails for reasons that live in different places — the tools,
the retrieval layer, the prompt, the model's own judgment — and training only
moves the last one. Pointing a training run at a tool bug produces a model that
has memorised its way around a broken tool, at considerable cost, while the tool
stays broken.

This is answerable with counting rather than opinion, provided Level 3 did its
job. If your failures are labelled by where the fix lives, you already have the
number that decides this. This lesson is about reading it.

The honest version of the question: *what would have to be true for training to
be the right call, and is it?*

## Count The Labels By Where The Fix Lives

The Level 3 taxonomy namespaces every label by its owner: `TOOLS.*`,
`RETRIEVAL.*`, `MODEL.*`. Summing the 30 annotated failures gives:

| Where the fix lives | Labels |
| --- | ---: |
| `TOOLS.selection` | 19 |
| `RETRIEVAL.citation` | 20 |
| `TOOLS.arguments` | 7 |
| `TOOLS.interpretation` | 3 |
| **Tools and retrieval — total** | **49** |
| `MODEL.reasoning` | 9 |
| `MODEL.instruction_following` | 4 |
| **Model — total** | **13** |

`python3 -m model_improvement.strongbench` computes exactly this and writes it to
[`decision.json`](../../../model_improvement/strongbench/decision.json):

```json
{"tool_or_retrieval_failure_labels": 49,
 "model_failure_labels": 13,
 "decision": "fix_tools_and_retrieval_before_training",
 "next_experiment": "Improve receipt lookup arguments and rerun the Level 2
                     benchmark before any LoRA run."}
```

Nearly four times as many failures live outside the model as inside it. A
training run would leave 49 of 62 labels untouched and cost a GPU budget to do
it. The decision is not close, and — this is the point — it did not require
judgment. It required a taxonomy applied consistently and then summed.

## The Trap This Avoids

Training is seductive precisely when it is wrong. A model fine-tuned on
corrections derived from tool failures will get better at the benchmark, because
it learns to produce the right final answers despite the broken tool. The score
moves. The demo improves.

What has actually happened is that the model has memorised compensations for a
defect nobody fixed. The tool is still wrong, so every new task family hits it
again, and the model's compensations do not transfer. You have bought a
benchmark improvement and paid for it in generalisation.

The tell is always the same: **the intervention does not match the diagnosis.**
When a fix works for reasons other than the ones you claimed, it will stop
working somewhere you cannot predict.

## Interventions, In Cost Order

[`intervention-matrix.json`](../../../model_improvement/strongbench/intervention-matrix.json)
records four options, each with the evidence that justifies its status and the
measurement that would confirm it:

| Intervention | Status | Confirmed by |
| --- | --- | --- |
| `tool_and_retrieval_fix` | **recommended_next** | receipt_lookup and citation slices improve on the Level 2 benchmark |
| `prompt_revision` | use_as_low_cost_control | no regression below threshold, fewer approval-boundary failures |
| `small_lora_sft` | **defer_until_tool_plateau** | heldout improvement plus unchanged or better unsafe-submission rate |
| `frontier_api_or_hybrid` | compare_if_quality_gap_remains | quality lift justifies cost, latency, privacy, vendor tradeoffs |

Two things about this table are worth adopting.

**Every row names its success measure in advance.** Deciding what would count as
success *before* running the experiment is what stops a disappointing result
from being reinterpreted afterwards. If you cannot write the success measure,
you are not ready to run the intervention.

**`small_lora_sft` is deferred, not rejected.** The status is
`defer_until_tool_plateau` — train when tool fixes stop paying, not never. The
condition is stated so a future reader knows when the answer changes. A matrix
that only says no is a matrix nobody revisits.

## Prepare The Data Anyway

The same build that says *do not train* still exports 78 train rows and 47 dev
rows, and still rejects 27 heldout rows. That is not a contradiction.

Preparing SFT data is cheap, and doing it surfaces problems while they are still
correctable — the split rules, the contamination guard, the target format. The
memo says to use the export for *rehearsal*. What it forbids is the claim:

```text
"Use the SFT export for Track 5B rehearsal, but do not claim model improvement
 until tool behavior is fixed and a heldout benchmark comparison improves."
```

Rehearsing the mechanics and asserting a result are different acts. Keep them
separate and you can be ready to train without being tempted to.

## The Adoption Gate

Written down before any training happens, in
[`decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md):

```text
Adopt a trained or local model only if heldout benchmark success improves
without increasing unsafe submission failures.
```

Note that it is a conjunction. Reward went up is not the gate; *heldout* success
improved **and** safety did not regress. A single-metric gate is one an
optimisation process will eventually satisfy in a way you did not intend, which
is the whole subject of Level 7.

## Common Failure Modes

- **Training because the score is disappointing.** The score does not say where
  the failure lives. The labels do.
- **Training on corrections derived from tool bugs.** Teaches the model to work
  around a defect that stays in the codebase.
- **No success measure written before the run.** Any outcome can then be read as
  progress.
- **A single-metric adoption gate.** Something will satisfy it without improving
  the system.
- **Deciding from the aggregate rather than the slices.** 89% hides a capability
  at 30%, and that capability is a tool problem.
- **Treating "defer" as "never".** Without a stated condition, nobody knows when
  to reconsider, so nobody does.

## Exercise

Open [`decision.json`](../../../model_improvement/strongbench/decision.json) and
[`intervention-matrix.json`](../../../model_improvement/strongbench/intervention-matrix.json).

1. `tool_or_retrieval_failure_labels` is 49 and `model_failure_labels` is 13,
   but there are only 30 annotated failures. Explain the arithmetic, and say
   which Level 3 property makes it work.
2. Suppose a LoRA run raised benchmark success from 0.89 to 0.94. Using the
   adoption gate, is that sufficient to adopt? What else must you check, and
   what would you suspect if the tool-related slices improved too?
3. `small_lora_sft` has status `defer_until_tool_plateau`. Write the concrete
   observation that would change it to `recommended_next`.

Check your answer:

```text
1. Labels are not exclusive — a single failure can carry several — so the 30
   rows produce 62 labels, split 49 tools/retrieval and 13 model. The property
   that makes it work is namespacing labels by where the fix lives: because
   every label starts with TOOLS., RETRIEVAL. or MODEL., summing by prefix is a
   valid answer to "where does the work go?".

2. Not sufficient. The gate is a conjunction: heldout success must improve AND
   unsafe submission failures must not increase, so you check the safety slice
   before adopting. If the tool-related slices also improved, be suspicious
   rather than pleased — training does not fix a tool. The likely explanation
   is that the model memorised compensations for the broken tool, which will
   not transfer to new task families and leaves the defect in place.

3. Something like: "tool_and_retrieval_fix has landed, receipt_lookup and
   citation slices have improved on the Level 2 benchmark, and the remaining
   annotated failures are majority MODEL.* labels." The plateau is the
   condition — when fixing tools stops moving the number, the residue is what
   training is for.
```

Then run `python3 -m model_improvement.strongbench` and read `decision-memo.md`
end to end. Every number in it is derived; find the one you would most want to
argue with, and check what it is computed from.

## Checkpoint

You are ready to move on when you can state where your failures live as a count
rather than an impression, name the intervention that count implies, and write
the measurement that would tell you it worked — before running it.

## Reading

- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — read it as a template for the memo you will have to write. Notice that every
  claim cites a number produced by a builder, which is what makes it reviewable
  by someone who disagrees with you.
- [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
  — the upstream input. The decision here is only as good as the labelling
  there, which is the argument for taking Level 3 seriously.
