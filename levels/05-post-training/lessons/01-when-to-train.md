# Lesson 1: When To Train

## Core Idea

Fine-tuning is an intervention, not a default step.

## Train When

Training may help when:

- failures are consistent and data-addressable
- the desired behavior is hard to express in prompts
- latency or cost requires a smaller model
- you have enough high-quality examples
- evals can measure the change

## Do Not Train When

Avoid training when:

- tools are broken
- retrieval is missing
- the prompt is unclear
- evals are weak
- data quality is poor
- the behavior changes frequently

## Checkpoint

You are ready to move on when you can argue for or against training using Level 2 and Level 3 evidence.

