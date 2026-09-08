# Lesson 3: Cleaning and Deduplication

## Core Idea

More data is not better data. A dataset's quality is set by its worst rows,
because those are the ones the model will learn from most confusingly, and no
amount of good data cancels a systematically wrong example.

Cleaning is therefore a deletion discipline, and it has one non-obvious
requirement: **a filter must record what it removed and why.** A cleaner that
silently drops rows is indistinguishable from a cleaner with a bug. Both produce
a smaller dataset that looks fine. Only one of them is working, and you cannot
tell which by looking at the output.

The second idea is that deduplication is not tidiness. A duplicate that lands in
two different splits is contamination, and it produces an evaluation number that
is quietly wrong rather than a crash. Dedup is a correctness control that happens
to look like housekeeping.

## Three Rejections, Three Different Bugs

`python3 -m datasets.strongbench` takes 155 raw rows to 152 cleaned, and writes
every removal to
[`rejected.jsonl`](../../../datasets/strongbench/rejected.jsonl):

```json
{"example_id": "cleaning-fixture-duplicate",            "reason": "duplicate_prompt_target",   "source_type": "level1_trace"}
{"example_id": "cleaning-fixture-missing-provenance",   "reason": "missing_provenance",        "source_type": "cleaning_fixture"}
{"example_id": "cleaning-fixture-invalid-target",       "reason": "invalid_target_contract",   "source_type": "cleaning_fixture"}
```

Three rows, three distinct reasons, and each is a different kind of problem:

| Reason | What is wrong | Why it must go |
| --- | --- | --- |
| `duplicate_prompt_target` | the same prompt and target appears twice | can land in two splits and contaminate the evaluation |
| `missing_provenance` | the row cannot say where it came from | unauditable; if it turns out to be wrong you cannot find its siblings |
| `invalid_target_contract` | the target does not match the answer schema | teaches the model a shape the harness will reject |

Note that the fixtures are named `cleaning-fixture-*`. They exist so that the
cleaner is **exercised on every build** rather than being a filter nobody has
seen fire. A cleaning stage that never rejects anything is a cleaning stage you
have not tested, and the cheapest fix is to plant one row per rule and assert
they are all caught.

The counts are published too, in
[`metrics.json`](../../../datasets/strongbench/metrics.json):

```json
{"raw_count": 155, "cleaned_count": 152, "rejected_count": 3,
 "rejection_reasons": {"duplicate_prompt_target": 1,
                       "invalid_target_contract": 1,
                       "missing_provenance": 1}}
```

`raw − rejected == cleaned` is an invariant worth asserting in a test. If those
three numbers ever stop reconciling, rows are being lost somewhere other than
the filter, and you will not find out any other way.

## Provenance Is A Filter Criterion, Not Metadata

`missing_provenance` being a rejection reason — rather than a warning — is the
strongest opinion in this pipeline, and it is the right one.

Provenance is what makes a dataset repairable. When a downstream evaluation
turns up a systematic error, the question is always "what else came from that
source?" A row that cannot answer it is not just unhelpful; it is a permanent
unknown that contaminates every future audit of the set. Keeping it costs more
than dropping it.

This is also why the pipeline records `source_type` on every surviving row —
`level1_trace`, `failure_correction`, `synthetic_gap_target`. That single field
is what lets Level 4 split by origin and Level 5 count failures by where the fix
lives. Cleaning is where it gets guaranteed.

## Deduplicate On Meaning, Not Bytes

The rule here is *prompt and target and source*, not exact-string equality on
the row. Two rows with different `example_id`s, different timestamps and
identical content are duplicates; byte comparison would keep both.

Choosing that key is the entire design decision, and it goes wrong in two
directions:

- **Too narrow** — dedup on the full row, and near-identical rows survive to be
  split apart, which is contamination.
- **Too broad** — dedup on the prompt alone, and you delete legitimate rows where
  the same question has different correct answers under different context.

There is no universal key. Write down which fields define identity for *your*
data, and expect to defend it.

## What Cleaning Does Not Catch

Worth being explicit, so the stage is not over-trusted:

- **Wrong-but-well-formed targets.** A correction with a plausible schema and an
  incorrect total passes every filter here. Only review catches it.
- **Near-duplicates.** Paraphrases with the same meaning survive an exact-match
  key.
- **Systematic bias in a source.** If a generator is skewed, its rows are
  individually valid and collectively misleading. That is what the source-type
  metrics are for.
- **Contamination across splits.** Handled later, by split assignment — see
  Lesson 6.

## Common Failure Modes

- **Dropping rows without logging them.** A silent filter and a broken filter
  look identical from outside.
- **Treating missing provenance as a warning.** The row becomes a permanent
  unknown in every later audit.
- **Deduplicating on the whole row.** Timestamps and ids defeat it; the
  duplicates survive.
- **Deduplicating on the prompt alone.** Deletes legitimate rows with
  context-dependent answers.
- **Never testing the cleaner.** Plant a fixture per rule; otherwise you learn it
  was broken from the model's behaviour.
- **Not reconciling the counts.** If `raw − rejected != cleaned`, rows are
  vanishing somewhere you are not looking.
- **Believing clean means correct.** Every row here is well-formed. That is a
  much weaker claim than accurate.

## Exercise

Open [`rejected.jsonl`](../../../datasets/strongbench/rejected.jsonl) and
[`metrics.json`](../../../datasets/strongbench/metrics.json).

1. Every rejected row has `example_id` beginning `cleaning-fixture-`. What is
   that telling you about how this pipeline is tested, and what would you
   conclude if a build produced zero rejections?
2. `missing_provenance` is a rejection rather than a warning. Give the concrete
   scenario, six months later, where that choice pays for itself.
3. The dedup key is prompt + target + source, not the whole row. Describe a row
   pair that a whole-row key would wrongly keep, and one that a prompt-only key
   would wrongly delete.

Check your answer:

```text
1. The cleaner is exercised on every build by planted fixtures — one per rule —
   so each filter is known to fire rather than assumed to. Zero rejections
   would mean the fixtures had been removed or the filters had stopped
   matching; either way the cleaning stage is no longer tested, and a silent
   filter is indistinguishable from a broken one. Zero is a red flag here, not
   a clean bill of health.

2. A heldout evaluation shows a systematic error — say every row from one
   synthetic generator has the meal cap wrong. The repair is "find and fix
   every row from that source". Rows carrying source_type can be found in one
   query. A row admitted without provenance cannot be found at all, so it stays
   in the dataset, wrong, through every future rebuild. One unauditable row
   makes the whole set slightly untrustworthy forever.

3. Whole-row key wrongly keeps: two rows with identical prompt and target but
   different example_id or captured-at timestamp — genuine duplicates that can
   then be split across train and heldout. Prompt-only key wrongly deletes: the
   same question asked by two different employees where the correct total
   differs because their receipts differ — same prompt, different valid target,
   and both rows are needed.
```

Then add a fourth fixture that should be rejected for a reason not yet covered,
run `python3 -m datasets.strongbench`, and check whether it survives. If it does,
you have found a rule the cleaner is missing.

## Checkpoint

You are ready to move on when your cleaner logs every rejection with a reason,
its counts reconcile, each rule has a fixture proving it fires, and you can
state which fields define identity for your dedup key and why.

## Reading

- [`datasets/strongbench/schema.json`](../../../datasets/strongbench/schema.json)
  — the contract `invalid_target_contract` is checked against. Read it before
  writing your own cleaner; most cleaning rules are a schema you have not
  written down yet.
- [`datasets/strongbench/dataset-card.md`](../../../datasets/strongbench/dataset-card.md)
  — its Cleaning and Limitations sections state what the filters do and do not
  guarantee. Publishing both is what stops a reader assuming clean means correct.
