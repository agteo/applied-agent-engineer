# Lesson 2: ML Foundations for Post-training

## Core Idea

Learners should understand the training loop, not just run a notebook.

## Concepts

- tokens and tokenization
- tensors
- loss functions
- gradient descent
- backpropagation
- optimizers
- train, validation, and test sets
- overfitting
- checkpoints
- learning rate
- batch size

## Minimal Loop

```python
outputs = model(**batch)
loss = outputs.loss
loss.backward()
optimizer.step()
optimizer.zero_grad()
```

## Checkpoint

You are ready to move on when you can explain what the loss represents and why validation matters.

