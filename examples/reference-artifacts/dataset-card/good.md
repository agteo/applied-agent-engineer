# Good Dataset Card: Acme Agent Training Dataset v1

## Intended Use

Use this dataset to prototype supervised correction, preference, and regression
data workflows for the Acme Expense Agent. It is a teaching dataset, not
production financial data.

## Sources

- 22 Level 1 trace demonstrations.
- 30 Level 3 failure corrections.
- 100 synthetic gap-targeted examples.

## Cleaning And Splits

The builder writes 155 raw rows, rejects 3 cleaning fixtures, and emits 152
cleaned rows. Rejection reasons include duplicate prompt/target/source triples,
missing provenance, and invalid target contracts.

Train/dev/heldout splits are written separately. Benchmark-derived failure
corrections stay out of the train split to reduce contamination risk.

## Limitations

Synthetic examples are template-generated. They are useful for teaching data
pipelines and targeting known gaps, but they cannot support a model-improvement
claim without held-out benchmark evidence.

## Why This Is Good

This card states intended use, sources, counts, filters, split policy,
contamination controls, and limits. It tells a learner what the dataset can and
cannot prove.
