# Lesson 6: Splits and Contamination

## Core Idea

A split is a promise about what a number means. When you report held-out
accuracy, you are promising that the model never saw those examples during
training, and that the number therefore estimates performance on work it has
not done before.

Contamination is that promise being broken, usually by accident and almost
always silently. Nothing crashes. No test goes red. The score goes *up*, which
is the worst possible symptom, because it looks like the thing you were hoping
for. A contaminated benchmark does not tell you your model is good; it tells
you your model has a good memory, and you cannot distinguish the two after the
fact.

The reason this is hard is a genuine conflict of interest built into the work.
The examples most valuable for training are the ones where the agent currently
fails — that is where the learning signal is. Those are also the examples that
constitute your measurement of failure. Every correction you write from a
failing benchmark task is simultaneously the best training data you have and a
piece of your test set.

You cannot resolve that by being careful. You resolve it with a rule enforced
in code, applied before anyone is tempted. This repo has two such rules, and
this lesson traces one contaminated example through both of them.

## Three Splits, And What Each One Promises

| Split | Promise | Used for |
| --- | --- | --- |
| `train` | the model may see this | fitting |
| `dev` | seen often, by you, not the model | prompt and adapter iteration |
| `heldout` | seen once, at the end | the number you report |

The distinction that matters most is between `dev` and `heldout`. Dev is
allowed to be contaminated by *you* — you look at it constantly, you tune
against it, and its score drifts upward for reasons that have nothing to do
with the model getting better. That is fine, provided you never quote it.
Heldout exists to be quotable, and every look costs a little of its value.

In this repo, `python3 -m datasets.strongbench` produces:

```text
train    78
dev      47
heldout  27
```

## Rule One: Corrections Never Reach Train

Read `choose_split` in
[`datasets/strongbench/__init__.py`](../../../datasets/strongbench/__init__.py):

```python
def choose_split(row, index):
    if row["source_type"] == "failure_correction":
        return "dev" if index % 2 else "heldout"
    if row["source_type"] == "level1_trace":
        return "dev" if index % 5 == 0 else "train"
    bucket = int(hashlib.sha256(row["example_id"].encode("utf-8")).hexdigest(), 16) % 10
    if bucket < 7:
        return "train"
    if bucket < 9:
        return "dev"
    return "heldout"
```

The first branch is the whole contamination defence. A row whose
`source_type` is `failure_correction` — meaning it was written from a task the
agent got wrong on the Level 2 benchmark — **has no path to `train`.** Not "is
usually kept out of train". Cannot reach it. Check the actual distribution:

| source_type | train | dev | heldout |
| --- | ---: | ---: | ---: |
| `failure_correction` | **0** | 15 | 15 |
| `level1_trace` | 17 | 5 | 0 |
| `synthetic_gap_target` | 61 | 27 | 12 |

Two details in that function are worth stealing.

**Synthetic rows are split by a hash of their content, not at random.** The
same example lands in the same split on every machine and every run. This
sounds like a reproducibility nicety and is actually a second contamination
defence: if splits were random, a disappointing heldout score could be quietly
improved by re-running the build until the assignment flattered you. Content
hashing removes that option.

**The rule is stated in the metrics the build emits**, so it survives contact
with people who never read `choose_split`:

```json
"heldout_protection": "Benchmark-derived failure corrections are assigned only to dev or heldout splits."
```

## Rule Two: Heldout Never Reaches Training Data

A split assignment is only a label. Something has to enforce it at the point of
use. In [`model_improvement/strongbench/__init__.py`](../../../model_improvement/strongbench/__init__.py):

```python
def sft_rejection_reason(row):
    if row.get("split") == "heldout":
        return "heldout_reserved_for_evaluation"
```

Every rejected row is logged rather than dropped silently, to
`sft-rejected.jsonl`:

```json
{"reason": "heldout_reserved_for_evaluation",
 "source_example_id": "correction-scripted-current-bench-029",
 "split": "heldout"}
```

There are **27 rows in that file, and 27 rows in the heldout split.** They are
the same 27. The SFT export refuses the entire heldout set, and says so on
every row.

Logging the refusals matters more than it looks. A filter that silently drops
rows is indistinguishable from a filter with a bug. A filter that writes down
what it refused and why can be audited by counting lines.

## Following One Example Through Four Levels

The lesson is easier to hold as a single path. Take `bench-029`:

```text
Level 2   bench-029 fails the benchmark
          "total_reimbursable: expected 75.00, got 108.00"
                    |
Level 3   a correction example is written from that failure
          example_id: correction-scripted-current-bench-029
                    |
Level 4   source_type = failure_correction, so choose_split()
          sends it to heldout — train was never reachable
                    |
Level 5   sft_rejection_reason() rejects it from the SFT export
          reason: heldout_reserved_for_evaluation
```

Fifteen of the 27 heldout rows are corrections like this one, and six of them
trace back to tasks that currently fail: `bench-029`, `bench-053`, `bench-055`,
`bench-058`, `bench-060`, `bench-075`.

Now notice what the discipline costs. Those six are the most informative
examples in the entire dataset — they are precisely the agent's known
weaknesses, written up with correct answers. Every one is refused from
training. That is not waste; it is the price of being able to say afterwards
whether anything improved. **If you train on your failures, you can no longer
measure whether you fixed them.**

## Contamination That Splits Do Not Catch

Split assignment protects against one leak. These are not covered by it:

- **Duplicates across splits.** The same prompt and target appearing in both
  train and heldout is contamination even when the labels differ. This repo
  removes them at the cleaning stage — see the `duplicate_prompt_target` row in
  [`datasets/strongbench/rejected.jsonl`](../../../datasets/strongbench/rejected.jsonl).
- **Expected answers inside prompts.** A synthetic generator handed the answer
  key produces training rows that teach recall, not reasoning.
- **Tuning repeatedly against heldout.** No individual run is contamination.
  Fifty runs and picking the best is, and it leaves no trace in any file.
- **Reusing benchmark fixtures for synthetic generation.** The policies and
  receipts are shared, so a generator seeded from benchmark tasks can
  reconstruct them without ever copying a row.

## Common Failure Modes

- **Training on heldout benchmark answers.** The score improves and means
  nothing. The most expensive mistake on this list, and the quietest.
- **Assigning splits randomly.** Re-running until the number improves is then
  available, and it will eventually be taken.
- **Choosing splits after seeing results.** A split decided post hoc is a
  selection of the data that flatters you.
- **Filtering silently.** A drop with no log is indistinguishable from a bug.
- **Quoting the dev score.** Dev is contaminated by design — by you, on
  purpose, every time you iterate.
- **Treating the benchmark as reusable.** Level 2 is a release gate. Each time
  you tune against it, it becomes slightly less of one.

## Exercise

Open [`datasets/strongbench/cleaned.jsonl`](../../../datasets/strongbench/cleaned.jsonl),
[`model_improvement/strongbench/sft-rejected.jsonl`](../../../model_improvement/strongbench/sft-rejected.jsonl)
and `choose_split` in the Level 4 builder.

1. How many `failure_correction` rows are in `train`, and is that a coincidence
   of this dataset or a property of the code? Point to the line that decides it.
2. `sft-rejected.jsonl` has 27 rows and the heldout split has 27 rows. Is that
   a coincidence? What would it mean if the rejection log had 26?
3. Suppose you changed `choose_split` so `failure_correction` rows could land in
   `train`. Nothing would crash and every test would still pass. Name the
   specific number that would become meaningless, and say who would notice.

Check your answer:

```text
1. Zero, and it is a property of the code. The first branch of choose_split
   returns "dev" or "heldout" for every failure_correction row; train is not
   reachable from that branch. The distribution (0 / 15 / 15) is a consequence,
   not a coincidence, and it would stay zero if the dataset tripled.

2. Not a coincidence. sft_rejection_reason rejects every row whose split is
   "heldout", so the rejection log must contain exactly the heldout set. If it
   held 26, one heldout row reached the SFT export — a contaminated training
   set, and the discrepancy in those two counts is the only visible symptom.
   That equality is worth asserting in a test.

3. The heldout benchmark comparison in the Level 5 decision memo — the number
   that decides whether a trained model is adopted. It would rise because the
   model had memorised corrections written from the very tasks it is being
   scored on. Nobody would notice from inside the repo: no test fails, no
   builder errors, and the metric moves in the direction everyone wants. It
   surfaces only in production, as a model that scored well and does not work.
```

Then run `python3 -m datasets.strongbench` twice and diff `heldout.jsonl`
against itself. It should be byte-identical, because splits come from a content
hash. Convince yourself why a random split would make every number in this
lesson unauditable.

## Checkpoint

You are ready to move on when every example in your dataset carries a split,
the rule that assigns it lives in code rather than in a convention, your
training export logs what it refused, and you can name one contamination route
your splits do not close.

## Reading

- [`datasets/strongbench/dataset-card.md`](../../../datasets/strongbench/dataset-card.md)
  — read the splits section before you publish a dataset. The card states the
  heldout protection in prose so a reader can check the claim against the code,
  which is the point of writing it down twice.
- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — read the adoption gate. It is the number rule two exists to protect, and
  seeing what depends on the split is what makes the discipline feel worth it.
