# Lesson 1: Why Evals Matter

## Core Idea

An agent that works once has not been engineered yet.

Evaluation turns demos into evidence. It helps teams decide whether a system is ready, whether a change helped, and where to invest next.

## Evaluation Questions

A useful eval answers specific questions:

- Did the agent complete the task?
- Was the final answer structurally valid?
- Were policy citations correct?
- Did the agent call the right tools?
- Did the agent avoid unsafe actions?
- How much did it cost?
- How long did it take?
- Did the new version improve over the old one?

## Bad Eval Questions

Avoid vague questions like:

- Is the agent smart?
- Does the answer look good?
- Which model is best?
- Did the demo work?

Those questions hide the behavior you need to measure.

## Evaluation Layers

Use multiple layers:

1. Contract checks: can the output be parsed?
2. Deterministic grading: are known fields correct?
3. Rubric grading: is the answer useful?
4. Human review: do people agree with the automated graders?
5. Regression comparison: did behavior improve?

## Checkpoint

You are ready to move on when you can name the exact behaviors your benchmark should measure.

