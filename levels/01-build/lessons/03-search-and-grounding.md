# Lesson 3: Search and Grounding

## Core Idea

Agents should not invent policy. They should retrieve policy and cite the source.

In Level 1, retrieval can be simple. The important skill is separating what the model knows from what the system can verify.

## Retrieval Boundary

The policy search tool should answer:

- Which source matched?
- What text was retrieved?
- Why was it relevant?
- How confident is the search result?

The final answer should answer:

- What does the policy imply for the user task?
- Which source ids support the answer?
- What remains uncertain?

## First Implementation

Start with keyword search over local Markdown or JSON policy fixtures.

Later modules can replace the implementation with embeddings, a vector database, or hybrid search. The tool contract should remain stable.

## Anti-patterns

- Letting the model answer policy questions without retrieval.
- Returning long documents instead of focused snippets.
- Omitting source ids.
- Treating retrieval score as truth.
- Hiding search failures from the final answer.

## Common Failure Modes

- Citing a policy id that was never retrieved.
- Using keyword search that returns the broadest policy instead of the relevant one.
- Answering from memory when the task requires fixture evidence.

## Exercise

For a missing-receipt question, name the policy ids the agent must retrieve before answering.

Check your answer:

```text
A strong answer retrieves `policy-receipts-001` and, when approval is required, `policy-approval-001`; it should not cite unseen policy ids.
```

Use the Acme Expense Agent trace to confirm the answer against the agent harness rather than relying on memory.

## Checkpoint

You are ready to move on when every policy claim in the final answer has at least one source id or is marked as uncertain.
