# Weak Model Improvement Decision: StrongBench Expense Agent v1

> A plausible bad example. Every sentence below is the kind of thing that
> survives a review meeting.

## Recommendation

Fine-tune a small model with LoRA on the prepared dataset.

## Rationale

The agent passes 89 of 100 benchmark tasks, which leaves 11 failures. We have a
cleaned dataset of 152 examples ready to go, and LoRA is cheap — a single GPU
for a couple of hours. Prompt engineering has already been tried and the
remaining failures look like the model not applying the policies correctly.

If the fine-tune improves the benchmark we will adopt it. If it does not, we
will have learned something and can revisit prompting.

---

## Why This Is Weak

**1. It never counts where the failures live.** "Look like the model not
applying policies" is an impression. The annotated failures carry namespaced
labels, and summing them gives 49 tools-and-retrieval against 13 model — nearly
four to one *against* the stated diagnosis. The decision is answerable by
arithmetic and this memo does not do it.

**2. Cheapness is used as a reason.** LoRA being affordable is not evidence it
is the right intervention. A cheap run pointed at a tool bug still produces a
model that has memorised compensations for a defect nobody fixed, and the
defect stays.

**3. "152 examples ready to go" is wrong on inspection.** Corrections cannot
enter the training split, so the real figure is 78 train rows, mostly synthetic.
The memo has not opened the export it proposes to train on.

**4. The success criterion is a single metric.** "If the benchmark improves" can
be satisfied by gaining five ordinary tasks while losing two safety-relevant
ones. An adoption gate must be a conjunction — held-out improvement **and** no
regression in the unsafe-submission slice.

**5. There is no rejection condition.** "If it does not work we will have
learned something" is not a decision rule. What result would make you revert?
Written after the run, that answer will be shaped by the run.

**6. No alternatives are compared.** Tool fixes, retrieval fixes, prompt
revision as a cheap control, a larger hosted model — none appear, so there is no
way to know whether the chosen intervention is the best available or simply the
one someone wanted to try. Compare [`good.md`](good.md), which carries an
evidence status per candidate including "not measured".
