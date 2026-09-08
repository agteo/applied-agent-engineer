# Lesson Template

The shape every numbered lesson should have, extracted from the two that meet
the full Workstream A depth bar:

- [`levels/02-evaluate/lessons/04-rubrics-and-llm-judges.md`](02-evaluate/lessons/04-rubrics-and-llm-judges.md)
- [`levels/07-reinforcement-learning/lessons/05-ppo-and-grpo.md`](07-reinforcement-learning/lessons/05-ppo-and-grpo.md)

`scripts/check_lesson_depth.py` enforces two of the five criteria below. The
other three need a human, which is why this file exists.

---

## The bar

| # | Criterion | Mechanical? | What satisfies it |
| --- | --- | --- | --- |
| 1 | Core idea in prose, not a noun list | No | Two to four paragraphs that a reader could paraphrase back. A bulleted list of terms fails. |
| 2 | A worked example of the actual mechanism | No | A code block, table or trace **taken from a file in this repo**, walked through. |
| 3 | A named, concrete failure mode | Yes | `## Common Failure Modes`, with failures specific to this topic. |
| 4 | An exercise with a checkable answer | Yes | `## Exercise` plus a `Check your answer:` block. |
| 5 | Reading tied to a specific decision | No | Each link followed by a sentence naming the decision it informs. |

---

## The rule that produces depth

**A lesson's worked example must come from a file in this repository.**

This single constraint does most of the work:

- It makes invented examples impossible.
- It gives the learner something to open, run and modify.
- It keeps lessons true as the code changes, because a moved file becomes a
  broken link and a broken link fails CI.
- It removes "what example should I use?" from the author's job. The repo
  already contains a benchmark report with real failures, 120 caught
  reward-hacking rollouts, a rejected-row log with reasons, six rubrics, and a
  calibration sample.

If you cannot find a repo artifact for a lesson, that is a signal about the
repo, not permission to invent one.

---

## Section order

```markdown
# Lesson N: Title

## Core Idea
Two to four paragraphs. What the thing is, why it exists, what breaks without
it. If the section is a bulleted list of nouns, it is not done.

## <Mechanism>            ← name it for the topic, not "Mechanism"
How it actually works. The part a learner cannot get from the title.

## <Worked Example>       ← name it for the artifact
A real file from this repo, quoted and walked through. Say what to notice and
why it was built that way.

## <The Tricky Part>      ← optional but usually where the value is
The parameter that bites, the ordering that matters, the number that looks
fine and is not.

## Common Failure Modes
Three to six, specific to this topic. Not "handle errors properly".

## Exercise
A task performed against a repo artifact, producing an answer that can be
checked. Then:

Check your answer:

```text
The answer, with the reasoning that makes it checkable.
```

## Checkpoint
"You are ready to move on when you can ..." — a capability, not a feeling.

## Reading
Each link followed by a sentence naming the decision it informs.
```

Headings the checker recognises for criterion 3: `## Common Failure Modes`,
`## Failure Modes`, `## Common Mistakes`. Criterion 4 needs `## Exercise`.

---

## Calibration

| | Typical lesson today | The bar |
| --- | ---: | ---: |
| Lines | 44–66 | 150–200 |
| Worked examples | 0 | at least 1, from the repo |
| Links outside `levels/` | 0 | 2 or more |

A lesson that grew by ~18 lines received a failure-mode block and an exercise.
That passes the gate and does not meet the bar.

---

## Writing the exercise

This is where most lessons fail, so it gets its own rule.

**A recall question is not an exercise.** "Why does Phase 5 reject heldout
rows?" tests whether the reader read the paragraph above it. There is no way to
get it interestingly wrong, so nothing is learned.

**An exercise sends the learner to an artifact and asks them to find something
that is not stated in the lesson.** The rubrics lesson asks which rubric band is
missing from the calibration sample. The answer is not in the prose; it is in
the file, and finding it changes how the reader reads every agreement rate
afterwards.

Good exercise shapes, roughly in order of value:

1. **Audit** — open an artifact, find the gap. ("Which band is absent?")
2. **Trace** — follow one value through the code to where it is decided.
   ("Which line returns `low` for `bench-054`?")
3. **Extend** — add a row, re-run the builder, explain what moved.
4. **Predict then check** — say what will happen, run it, reconcile.

Then, where possible, close with a real command:

```markdown
Then extend the calibration file with your chosen row, re-run
`python3 -m evals.runner --model scripted`, and read the new
`rubric_agreement_rate`. If it dropped, you have learned something the old
number was hiding.
```

---

## Before you call a lesson done

- [ ] Core Idea is prose, and survives being read aloud.
- [ ] At least one worked example, quoted from a repo file, with a link to it.
- [ ] Failure modes are specific to this topic.
- [ ] The exercise sends the reader to an artifact, and the answer block
      explains the reasoning rather than just stating the result.
- [ ] Every Reading link has a sentence naming the decision it informs.
- [ ] Every relative link resolves.
- [ ] **Someone who has not read the lesson can do the exercise with the lesson
      closed and the repo open.** This is the acceptance test. Nothing else on
      this list substitutes for it.

---

## Working order

Batch no more than four lessons at a time. The 18-line uniformity across 46
lessons is what batching twenty-six produces; depth does not survive volume.

Suggested sequence, by how many learners are affected and how ready the
material is:

1. Level 2 — most learners reach it; artifacts are richest
2. Level 6 — the reward table in `ROADMAP.md` belongs in lesson 05
3. Level 7 — lesson 05 is already done and sets the standard
4. Level 5, then Levels 3–4
