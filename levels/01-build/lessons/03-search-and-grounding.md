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

## Checkpoint

You are ready to move on when every policy claim in the final answer has at least one source id or is marked as uncertain.

