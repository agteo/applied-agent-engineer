# Lesson 2: Failure Taxonomies

## Core Idea

A benchmark tells you thirty tasks failed. A taxonomy tells you there are four
things to fix.

That compression is the entire value, and it is worth stating as a test:
**a label earns its place when it changes what you would do next.** If two
failures carry different labels but you would take the same action for both,
the distinction is decorative. If two failures share a label but need different
fixes, the label is too coarse. Everything else about taxonomy design — how many
categories, what to call them, how to nest them — follows from that one
question.

This is why "bad answer" and "hallucination" are not labels. They describe how
a failure felt to read. An engineer holding thirty rows labelled "bad answer"
has learned nothing they did not know from the pass rate.

The second property that matters is agreement. A taxonomy applied inconsistently
produces counts that mean nothing, and counts are what you use to prioritise. If
two reviewers label the same trace differently, the number next to each category
is noise, and you will spend your effort on whichever category happened to
attract the most generous labeller.

## The Taxonomy This Repo Uses

`python3 -m evals.operations` emits
[`evals/operations/strongbench/taxonomy.md`](../../../evals/operations/strongbench/taxonomy.md):

```text
EVALUATION.expected_answer_wrong   The expected answer may be wrong or underspecified.
MODEL.instruction_following        The answer ignores a required boundary such as employee-only submission.
MODEL.reasoning                    Wrong arithmetic, category interpretation, or policy application.
RETRIEVAL.citation                 The answer omitted an expected policy source.
TOOLS.arguments                    A tool was called with arguments too broad, too narrow, or malformed.
TOOLS.interpretation               The agent saw the tool result but reported the wrong conclusion.
TOOLS.selection                    A required tool was not called.
```

Three structural choices are worth copying.

**Labels are namespaced by where the fix lives.** `TOOLS.*` failures are fixed
in the harness or the tool schemas. `MODEL.*` failures are fixed in the prompt,
the data, or the model. `RETRIEVAL.*` is fixed in the search layer. The prefix
answers "whose bug is this?" before anyone reads the description.

**`TOOLS.selection`, `TOOLS.arguments` and `TOOLS.interpretation` are three
labels, not one.** They correspond to three genuinely different repairs: the
agent did not call the tool; it called it wrongly; or it called it correctly and
misread the result. Collapsing them into `TOOLS.*` would produce a big bucket
you cannot act on.

**`EVALUATION.expected_answer_wrong` exists.** A taxonomy that cannot express
"the benchmark is wrong" will force every such case into a model-blaming
category, and you will chase agent bugs that are actually task bugs. Give your
reviewers somewhere honest to put it.

## Labels Are Not Exclusive

A trace can carry several. Across the 30 annotated failures:

| Label | Count |
| --- | ---: |
| `RETRIEVAL.citation` | 20 |
| `TOOLS.selection` | 19 |
| `MODEL.reasoning` | 9 |
| `TOOLS.arguments` | 7 |
| `MODEL.instruction_following` | 4 |
| `TOOLS.interpretation` | 3 |

Those sum to 62 across 30 rows, because a single failure usually has more than
one thing wrong with it. Forcing one label per failure would mean discarding
most of what the reviewer noticed.

## The Compression, Measured

Here is the payoff, from
[`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl):

```text
30  annotated failures
 7  distinct label combinations
 5  distinct hypotheses
 4  distinct recommended interventions
```

Thirty failures collapse to four actions. And the mapping is clean — **every
one of the seven label combinations maps to exactly one intervention.** That is
the property to check in your own taxonomy: if a label combination maps to two
different fixes, the labels are not carrying enough information yet.

The largest group shows what this buys:

```json
{"config": "weak-no-tool",
 "taxonomy_labels": ["RETRIEVAL.citation", "TOOLS.selection"],
 "hypothesis": "The model is answering from the prompt without using the
                evidence-producing tools required by policy.",
 "recommended_intervention": "Tighten prompt/tool policy and fail CI when
                required evidence tools are skipped."}
```

Nineteen of the thirty rows are that exact shape. Without labels they are
nineteen separate mysteries. With labels they are one sentence — *this agent
config does not call its tools* — and one fix that closes all nineteen at once.

Note also the `config` field. Eleven failures come from `scripted-current` and
nineteen from `weak-no-tool`. Recording which configuration produced a failure
is what lets you say a category belongs to one build rather than to the agent in
general.

## From Label To Action

The bundle carries three fields per row, and they are deliberately separate:

| Field | Question it answers | Changes when |
| --- | --- | --- |
| `taxonomy_labels` | what kind of failure is this? | the taxonomy is revised |
| `hypothesis` | why do we think it happened? | someone investigates |
| `recommended_intervention` | what should we do? | the fix is decided |

Keeping them apart matters because they have different lifetimes and different
authors. A label is applied by a reviewer in a minute. A hypothesis survives
until someone disproves it. An intervention is a commitment of engineering time.
Collapsing them into one "notes" field loses the ability to re-derive the second
two when the first changes.

## Common Failure Modes

- **Labels that describe the symptom.** "Wrong total" is the grader's job. The
  label should say why the total was wrong.
- **Labels nobody can act on.** If no intervention follows, delete the label.
- **One label per failure, enforced.** Most real failures have several causes;
  forcing a choice discards the reviewer's actual finding.
- **Mixing cause with severity.** `critical` is not a sibling of
  `TOOLS.selection`. Severity is a separate axis.
- **No category for "the benchmark is wrong."** Every taxonomy needs an escape
  hatch, or reviewers will file eval bugs as model bugs.
- **Counting labels without recording the config.** A category that belongs to
  one build looks like a property of the agent.
- **Never measuring agreement.** Two reviewers, twenty traces, compare. If they
  disagree often, your counts are noise and your priorities are arbitrary.

## Exercise

Open [`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl)
and [`taxonomy.md`](../../../evals/operations/strongbench/taxonomy.md).

1. Nineteen of the thirty rows share one hypothesis and one intervention. What
   do their `taxonomy_labels` and `config` have in common, and what single change
   would close all nineteen?
2. The label counts sum to 62 across 30 rows. Is that a labelling error? What
   would it imply if the sum were exactly 30?
3. `EVALUATION.expected_answer_wrong` is defined in the taxonomy and used by no
   row in this bundle. Argue for keeping it anyway, then say what you would
   conclude if it were suddenly applied to twelve rows.

Check your answer:

```text
1. All nineteen carry ["RETRIEVAL.citation", "TOOLS.selection"] and all nineteen
   come from config "weak-no-tool" — an agent configuration that answers from
   the prompt without calling the evidence tools. The intervention is one
   change: tighten the prompt/tool policy and fail CI when required evidence
   tools are skipped. Nineteen failures, one fix, because the labels grouped
   them.

2. Not an error. Labels are not exclusive, so a single failure can be both a
   citation omission and a tool-selection failure — which is exactly what those
   nineteen rows are. A sum of exactly 30 would mean one label per row, which
   for real agent failures almost always means reviewers were forced to choose
   and their other observations were thrown away.

3. Keep it because a taxonomy with no way to say "the expected answer is wrong"
   pushes benchmark bugs into model-blaming categories, and the team then
   debugs an agent that is behaving correctly. Zero uses is the healthy state.
   If it were suddenly applied to twelve rows, the finding is about the
   benchmark, not the agent: stop tuning and go audit the task expectations
   before any of the other counts can be trusted.
```

Then pick five rows and label them yourself before reading the
`taxonomy_labels` field. Compare. Where you disagree, decide whether the
taxonomy needs a clearer definition or you need a closer read — that argument is
the calibration this lesson's Checkpoint asks for.

## Checkpoint

You are ready to move on when every label in your taxonomy maps to an
intervention, no label describes a symptom, and you and one other person have
labelled the same traces and compared.

## Reading

- [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
  — read how the label counts turn into a prioritised list. That ordering is the
  decision the taxonomy exists to support; if your labels cannot produce one,
  they are not finished.
- [tau2-bench](https://github.com/sierra-research/tau2-bench) — its per-task
  failure analysis classifies by cause rather than symptom. Read it when you are
  deciding your own category boundaries, and compare its splits against the
  `TOOLS.*` three used here.
