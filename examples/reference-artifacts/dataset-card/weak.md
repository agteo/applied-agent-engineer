# Weak Dataset Card: StrongBench Agent Training Dataset v1

> A plausible bad example. It has every section a card is supposed to have,
> which is what makes it instructive — completeness is not the same as
> disclosure.

## Intended Use

Training and evaluating the StrongBench Expense Agent.

## Sources

Curated from agent interactions, reviewed failures, and generated examples.

## Schema

Each row has a prompt, a target answer, labels, and a split.

## Cleaning

Malformed and duplicate rows were removed. The remaining rows were reviewed for
quality.

## Metrics

- 152 examples
- split into train, dev, and test

## Limitations

The dataset is small and domain-specific.

## Privacy

No production data.

---

## Why This Is Weak

**1. Sources are described, not located.** "Curated from agent interactions"
cannot be checked. A source line should name a file or a command, so a reader
can go and look at what they are being asked to trust.

**2. The synthetic fraction is hidden.** Two thirds of these rows are
template-generated. That is the single most decision-relevant fact about the
dataset, and the card is not wrong in any checkable way for omitting it — which
is exactly why disclosing it has to be a deliberate habit. A model that improves
on this data may have learned the generator.

**3. Metrics are hand-typed and incomplete.** "152 examples" was true on the day
it was written. There is no raw count, no rejected count, no per-source
breakdown, and no per-split counts — so nothing here reconciles against the
files, and nobody would notice when it stopped being true. Generate the numbers
from the build.

**4. "Reviewed for quality" describes no rule.** Which filters ran? What did
they reject, and how many? A cleaning section without rejection reasons and
counts is a claim that someone was careful.

**5. The splits have no rule.** "Train, dev, and test" says nothing about how a
row is assigned, and therefore nothing about contamination. The load-bearing
guarantee — that examples derived from the benchmark cannot enter training — is
absent, so a reader cannot tell whether held-out numbers from this data mean
anything.

**6. Limitations is one line, and it is the wrong line.** "Small and
domain-specific" is true of most datasets and actionable for none. The real
limitations are the synthetic majority and the fact that correction targets are
compact oracle summaries rather than answers you would ship — train on those and
deterministic graders pass while the output quality regresses.

**7. Privacy asserts without stating what was checked.** "No production data" is
the right answer; saying which fixtures were used is what makes it verifiable.

Compare [`good.md`](good.md), where sources are paths, metrics come from the
build, the split rule is stated, and Limitations is the longest section on the
page.
