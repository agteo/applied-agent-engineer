# Lesson 4: LoRA and QLoRA

## Core Idea

LoRA adapts a model by training small low-rank adapter weights instead of updating all model weights.

QLoRA combines quantization with LoRA to reduce memory needs.

## Concepts

- base model
- adapter
- rank
- alpha
- target modules
- quantization
- checkpoint
- merge vs serve adapter

## Checkpoint

You are ready to move on when you can explain what artifact training produces and how it will be evaluated.

## Reading

- [TRL](https://huggingface.co/docs/trl/en/index) — the library Lab 3 uses. Read the [SFTTrainer guide](https://huggingface.co/docs/trl/en/sft_trainer) end to end before running anything; most Track 5B failures are configuration mistakes, not conceptual ones.
- [PEFT LoRA guide](https://huggingface.co/docs/peft/en/developer_guides/lora) — what rank, alpha, and target modules actually control. You will be asked to justify each in your training config.
- Cost and VRAM planning: [resources/gpu.md](../../../resources/gpu.md).
