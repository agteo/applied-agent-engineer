# Lesson 2: Schemas and Formats

## Core Idea

A dataset schema is not paperwork. It is the contract that decides what a row is
allowed to be, and every rule you leave out becomes a class of bad row you will
discover later from a model's behaviour.

The useful way to design one is to ask what breaks without each field. Not "what
would be nice to record" — that produces a schema of thirty optional fields
nobody fills — but **which downstream step fails, and how loudly, if this is
missing.** A field whose absence causes nothing to fail is a field that will
drift out of use.

The second idea is that format choices are operational choices. JSONL rather than
JSON, one object per line, is not a stylistic preference: it makes a dataset
appendable, streamable, greppable, and diffable line by line. Those properties
decide what your tooling can do for the rest of the project.

## Eleven Required Fields

[`schema.json`](../../../datasets/strongbench/schema.json) requires all of these
on every row:

| Field | What fails without it |
| --- | --- |
| `schema_version` | old rows become unidentifiable when the shape changes |
| `example_id` | rows cannot be referenced, deduped, or traced |
| `source_type` | split assignment, provenance shape, every per-source metric |
| `task_id` | the row cannot be connected to the task it came from |
| `prompt` | nothing to train or evaluate on |
| `messages` | no conversational form for a trainer to consume |
| `target_final_answer` | no supervision signal |
| `labels` | no aggregate analysis, no failure-mode targeting |
| `provenance` | unauditable; a wrong row's siblings cannot be found |
| `quality` | no way to filter by confidence in the row |
| `split` | contamination becomes possible and undetectable |

Two of those carry more weight than the rest. `source_type` decides which split
a row may enter and what its provenance looks like — Lesson 1's point that it is
structural rather than descriptive. And `split` is what makes the contamination
guarantee checkable at all; a dataset where rows lack a split has no defence, it
has an intention.

`rejected_final_answer` is the single optional field, present on corrections
only. Optional-by-source-type is a deliberate schema decision, and it is honest:
requiring it everywhere would force empty values onto rows that have nothing to
reject.

## Both Prompt And Messages

The schema carries `prompt` as a string *and* `messages` as a structured array,
which looks redundant and is not.

`messages` is the trainer-facing form: roles and content, ready for a chat
template. `prompt` is the human-facing and tooling-facing form — what you grep
for, what you show in a review UI, what you dedup on.

Deduplication keys on prompt plus target plus source precisely because `prompt`
is a stable flat string. Keying on `messages` would mean two rows differing only
in a system-prompt revision would count as distinct, which is not what you mean
by a duplicate.

Carrying both is a small cost for two very different consumers.

## Version The Schema From Row One

`schema_version` is required, and this is the field teams most often add later —
by which point the rows that need it most are the old ones that do not have it.

The failure it prevents: you change what `quality` contains, or make a field
required, and now the dataset holds two shapes with nothing to distinguish them.
Every consumer needs a heuristic, the heuristics disagree, and the bug surfaces
as a training run behaving oddly.

Cost of adding it at the start: one string per row. Cost of adding it in month
six: a migration over data you no longer fully understand.

## JSONL Earns Its Place

One JSON object per line, newline-delimited:

- **appendable** — a builder can stream rows without holding the set in memory
- **streamable** — a consumer can process 100k rows without parsing 100k rows first
- **greppable** — `grep failure_correction cleaned.jsonl` is a valid first look
- **diffable** — a changed row is a changed line, so review shows what moved
- **partially recoverable** — one malformed line loses one row, not the file

That last property matters more than it sounds. A single JSON array is
all-or-nothing: one truncated write and the whole dataset fails to parse.

The cost is that JSONL has no place for file-level metadata, which is why the
counts live in `metrics.json` and the description in `dataset-card.md`. Splitting
data from metadata is the tradeoff, and it is the right one — it also means the
card can be regenerated without touching the rows.

## Sorted Keys, Stable Order

Every builder writes with sorted keys and a fixed row order, which is what makes
the artifacts byte-reproducible and lets CI gate on `git diff --exit-code`.

Without it, rebuilding a dataset produces a diff on every line and the gate is
useless — so no one can tell an intentional data change from key-order churn.
Determinism in serialisation is a precondition for reviewing data changes at all.

## Common Failure Modes

- **Adding `schema_version` later.** The rows that need it are already written.
- **Optional fields nobody fills.** They read as coverage and are empty.
- **No `provenance`.** One unauditable row makes every future audit incomplete.
- **`split` as metadata rather than a required field.** Contamination becomes
  undetectable.
- **A single JSON array.** One bad write loses the file.
- **Unsorted keys.** Every rebuild diffs, so no diff is meaningful.
- **Deduping on the structured form.** A system-prompt edit makes duplicates
  look distinct.
- **Metadata inside the rows.** Counts drift per row and no consumer trusts them.

## Exercise

Open [`schema.json`](../../../datasets/strongbench/schema.json) and
[`cleaned.jsonl`](../../../datasets/strongbench/cleaned.jsonl).

1. `split` is a required field with an enum of three values. Name the downstream
   guarantee that becomes impossible if it were optional, and where in the
   pipeline that guarantee is enforced.
2. The schema carries both `prompt` and `messages`. Give one operation that
   needs the flat string and one that needs the structured form, and say what
   breaks if you keep only `messages`.
3. `rejected_final_answer` is the only optional field. Argue for keeping it
   optional rather than requiring it with an empty default.

Check your answer:

```text
1. The contamination guarantee — that no benchmark-derived correction reaches
   training data. It is enforced twice: choose_split assigns corrections only to
   dev or heldout, and sft_rejection_reason refuses any row whose split is
   "heldout" from the SFT export. Both read the field directly, so an optional
   split would give both a null case to handle and neither could make a
   guarantee.

2. The flat string is needed for deduplication, which keys on prompt plus target
   plus source, and for grep and review UIs. The structured form is needed by a
   trainer applying a chat template with roles. Keeping only messages would move
   dedup onto the structured form, so two rows differing only in a system-prompt
   revision would no longer look like duplicates — and the duplicate would
   survive to be split across train and heldout.

3. Requiring it with an empty default puts a meaningless value on 122 rows and
   makes "has a rejected answer" a check on emptiness rather than presence.
   Optional keeps the field's presence meaningful: counting rows that have it
   gives the preference-training ceiling directly. It also documents the
   asymmetry — only corrections can have one — in the schema rather than in
   prose someone has to read.
```

Then add a field to the schema and write down which downstream step would fail
without it. If nothing would fail, it belongs in `provenance` or nowhere.

## Checkpoint

You are ready to move on when every required field in your schema has a
downstream step that fails without it, your rows carry a schema version, and
your serialisation is deterministic enough to review a data change as a diff.

## Reading

- [`datasets/strongbench/metrics.json`](../../../datasets/strongbench/metrics.json)
  — the file-level metadata JSONL cannot hold. Note that every count is derived
  from the rows rather than maintained beside them.
- [`model_improvement/strongbench/sft-schema.json`](../../../model_improvement/strongbench/sft-schema.json)
  — the downstream schema. Compare which fields survive into a training export
  and which do not; that subset is the real answer to what the schema was for.
