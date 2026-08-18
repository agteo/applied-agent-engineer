# Lesson 2: ML Foundations for Post-training

## Core Idea

Track 5B requires a real training run. Eleven bullet points and a five-line loop will not prepare you for one, and this lesson does not pretend otherwise.

This lesson is a **prerequisite gate**, not a substitute course. Take one of the courses below before attempting Lab 3, or come in already knowing this material.

## Prerequisite Courses

Pick one and finish it. Each is free, self-paced, and code-first.

- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — the closest fit to this track. Chapters 1-3 cover transformers, tokenization, datasets, and a full fine-tuning loop with the same library stack Lab 3 uses. Chapter 11 covers supervised fine-tuning and LoRA directly. Budget roughly 15-20 hours.
- [fast.ai Practical Deep Learning for Coders](https://course.fast.ai/) — better if you have never trained any model. Broader than you need, stronger on intuition for loss, overfitting, and learning rates. Budget 40+ hours.
- [Karpathy, Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — best if you want backpropagation to stop being a black box. Build a transformer from scratch. Budget 20+ hours.

For the specific libraries Lab 3 uses, read [TRL's SFT documentation](https://huggingface.co/docs/trl/en/sft_trainer) and [PEFT's LoRA guide](https://huggingface.co/docs/peft/en/developer_guides/lora) alongside the course.

## Concepts You Must Already Understand

If any of these is unfamiliar, you are not ready for Lab 3:

- tokens and tokenization
- tensors and shapes
- loss functions, and what a loss curve going flat means
- gradient descent and backpropagation
- optimizers, learning rate, and batch size
- train, validation, and test splits
- overfitting, and how to see it in a validation curve
- checkpoints, and what is actually inside one
- the difference between full fine-tuning and a LoRA adapter

## Minimal Loop

The loop itself is four lines. Recognising it is not the same as knowing what to do when it produces a bad model.

```python
outputs = model(**batch)
loss = outputs.loss
loss.backward()
optimizer.step()
optimizer.zero_grad()
```

## Checkpoint

You are ready for Lab 3 when you can:

1. Explain what your loss number represents in the units of your data.
2. Explain why a falling training loss with a rising validation loss is bad news.
3. Read a LoRA config and say what rank, alpha, and target modules each control.
4. Estimate the VRAM your run needs before you rent the GPU. See [resources/gpu.md](../../../resources/gpu.md) for what that costs.

If you cannot do all four, complete Track 5A instead. A rigorous model improvement decision memo is a real deliverable, and it is worth more than a training run you cannot interpret.
