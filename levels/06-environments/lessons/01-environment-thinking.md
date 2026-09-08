# Lesson 1: Environment Thinking

## Core Idea

A benchmark asks an agent a question and grades the answer. An environment gives
an agent a world, lets it act, and grades what it *did*.

That difference is not a matter of degree. A benchmark can tell you the total was
wrong. Only an environment can tell you that a report was filed by someone with
no authority to file it — because filing is an action against state, and a
question-and-answer format has nowhere for the state to live.

The shift is from grading outputs to grading trajectories, and it unlocks the
three things Levels 6 and 7 are built on: **process verification** (did it check
what it claimed to check), **safety properties** (did it avoid something
forbidden), and **reward** (a decomposable score rather than pass/fail).

The cost is that you are now maintaining a simulated world, which is a real
engineering burden and easy to over-build. Environment thinking is largely the
discipline of building the smallest world your verifiers actually read.

## What Changes When State Exists

Level 2 grades a final answer against expected fields. Level 6 grades the same
task by asking what happened:

| Question | Benchmark | Environment |
| --- | --- | --- |
| Is the total right? | compare fields | compare fields |
| Did it look up the receipt? | infer from the answer | `audit_log` has the lookup |
| Did it cite a policy it retrieved? | cannot tell | compare cited against retrieved |
| Did it file a draft? | cannot tell | `drafts[draft-{task_id}]` |
| Did it submit without authority? | cannot tell | `submitted_reports` plus the actor |
| Did it change anything at all? | cannot tell | initial hash vs terminal hash |

Only the first row survives the move to a benchmark. Everything else needs a
world that remembers.

This is what makes the reward hacker from Lesson 5 catchable. It produces the
correct total on all 120 rollouts and fails all 120, because five of the eight
checks ask about process and state rather than output. Under a benchmark it
would score full marks.

## An Environment Is A Contract, Not A Domain

The most useful idea in this level is that "environment" names an *interface*.
[`environments/contract.py`](../../../environments/contract.py) states it as a
list of functions every environment must provide:

```python
REQUIRED_FUNCTIONS = [
    "build_environment_bundle",
    "generate_tasks",
    "run_scripted_policy",
    "run_reward_hacking_policy",
    "verify_rollout",
    "score_reward",
    "write_environment_bundle",
]
```

Notice `run_reward_hacking_policy` is *required*. An environment that cannot
produce an adversarial policy has no evidence its verifiers discriminate, so the
contract refuses to call it complete. That is a strong opinion encoded as an
interface, and it is the right one.

Because the contract exists, the runner is domain-agnostic:

```bash
python3 -m environments.runner environments.code_repair --out <dir>
```

Any module implementing the seven functions can be built, validated and scored by
code that knows nothing about expenses or code.

## The Same Contract, A Different World

This repo has two environments, and comparing them is the fastest way to see
what is domain-specific and what is not:

| | `strongbench_finance` | `code_repair` |
| --- | --- | --- |
| Tasks | 120 distinct | 60 distinct |
| Tools | 7 | 5 |
| Verifier types | deterministic, state, constraint, model-based | the same four |
| Reference policy | 1.000 success, 2.1 avg reward | 1.000 success |
| Hacker caught | 120 / 120 | 60 / 60 |
| Hacker's signature move | cites policies it never retrieved | **fabricated test claims: 60** |

The domains share nothing: one reasons about receipts and approval boundaries,
the other about failing tests and code changes, with categories like `off_by_one`,
`none_guard` and `state_machine`. What transfers is the *shape* — tasks, tools
that own state, verifiers over process, a reward built from checks, and an
adversary that must be caught.

`fabricated_test_claims: 60` is the tell that the transfer is real. It is the
code-repair equivalent of citing an unretrieved policy: the agent claims the
tests pass without having run them. Different world, same class of dishonesty,
same structural defence — verify the process, not the assertion.

**If your verifier design only works in one domain, it is probably domain
trivia rather than a skill.** Porting once is how you find out.

## Build The Smallest World Your Checks Read

The pressure in environment design runs toward realism, and realism is mostly a
trap. Every field of state you add is a field you must keep consistent through
every transition, forever, and most of them will never be read.

The rule from Lesson 2 applies at the level of the whole design: add state when
a check needs it. The finance simulator holds six employees, three managers, six
policies, thirty-two receipts and eight trips — enough to generate 120 distinct
tasks and no more. It has no vendors, no invoices, no payment rails, and its
bias note says so explicitly.

A small world that supports sharp verifiers beats a large one whose checks are
vague.

## Common Failure Modes

- **Building an environment where a benchmark would do.** If nothing you want to
  grade is about state, you are paying for a world you do not need.
- **Grading only the final answer.** Discards everything the environment exists
  to provide.
- **No adversarial policy.** No evidence any check discriminates.
- **Modelling the domain rather than the checks.** Consistency obligations
  without verification value.
- **A contract that is documentation.** If the runner cannot execute an
  arbitrary conforming module, the interface is aspirational.
- **One domain only.** Verifier skill that has never transferred may be trivia.
- **Confusing simulator success with readiness.** High reward in a fixture-sized
  world is readiness for harder evaluation, nothing more.

## Exercise

Open [`environments/contract.py`](../../../environments/contract.py) and the
metrics for both environments.

1. `run_reward_hacking_policy` is a required function of the contract. Argue why
   an adversarial policy belongs in the interface rather than in the tests.
2. `code_repair` reports `fabricated_test_claims: 60` for its hacker;
   `strongbench_finance` reports citations of unretrieved policies. Name the
   shared property both are detecting, and the general defence.
3. Both reference policies score 1.000 with `distinct_rewards: 1`. What does
   that tell you about using either environment for training, and which Level 7
   claim does it block?

Check your answer:

```text
1. Because a verifier suite with no policy that fails it is unevidenced. Tests
   check that code runs; the hacker checks that the checks discriminate, which
   is a property of the environment's design rather than of its implementation.
   Putting it in the contract means an environment cannot be called complete
   without shipping the evidence that its verifiers bite — and the runner can
   compute a catch rate for any conforming module without knowing the domain.

2. Both detect a claim the agent did not earn: citing a policy it never
   retrieved, and asserting tests pass without running them. The shared property
   is an assertion about evidence the agent never obtained. The general defence
   is to record what the agent actually did — retrievals, test runs — in state,
   and verify the claim against that record rather than accepting the claim.

3. Neither is usable as training data. One distinct reward across every rollout
   means zero within-policy variance, so there is no signal about what to do
   differently — advantage estimation has nothing to work with. It blocks any
   claim that experience improved the policy, which is why the Level 7 report
   states plainly that its rollout set is a regression suite and not training
   data.
```

Then run `python3 -m environments.runner environments.code_repair --out /tmp/cr`
and read the validation output. The runner never mentions code or expenses,
which is the property the contract buys.

## Checkpoint

You are ready to move on when you can say which of your grading questions need
state and which do not, your environment implements a contract a generic runner
can execute, and you have an adversarial policy your verifiers catch.

## Reading

- [`environments/README.md`](../../../environments/README.md) — how the two
  environments relate to the shared contract. Read it before adding a third.
- [`environments/strongbench_finance/simulator-bias-note.md`](../../../environments/strongbench_finance/simulator-bias-note.md)
  — what this world deliberately does not model. Write the equivalent for yours
  early; it is much harder to be honest about after you have shipped results.
