# References and Tooling Anchors

The curriculum should be pressure-tested against prior work. Learners should know when they are following established patterns, adapting them, or intentionally building something smaller for pedagogy.

## Evaluation Frameworks

- [Inspect](https://inspect.aisi.org.uk/?lang=en-US): an open-source framework for large language model evaluations with datasets, agents, tools, scorers, sandboxing, and agent evaluation support.
- [OpenAI Evals](https://github.com/openai/evals): a framework and benchmark registry for evaluating LLMs and LLM systems, including custom evals.

## Agent And Environment Benchmarks

- [tau2-bench](https://github.com/sierra-research/tau2-bench): a benchmark for tool-agent-user interaction in real-world domains, with policies, tools, tasks, and evaluation criteria.
- [SWE-bench](https://github.com/princeton-nlp/SWE-bench): a benchmark for evaluating LLMs on real software issues using reproducible Docker-based evaluation.
- [WebArena](https://github.com/web-arena-x/webarena): a self-hostable web environment for evaluating autonomous agents on realistic web tasks.
- [WebArena-Verified](https://servicenow.github.io/webarena-verified/): a verified release emphasizing audited tasks, deterministic scoring, and offline evaluation from traces.

## Post-Training Tooling

- [TRL](https://huggingface.co/docs/trl/v1.7.0/en/index): a Hugging Face library for training transformer language models with methods such as SFT, DPO, GRPO, reward modeling, and related post-training workflows.

## How These Influence The Course

This repo should not ask learners to reinvent prior art blindly.

The Acme curriculum intentionally starts smaller than these systems, but it should borrow their discipline:

- explicit task schemas
- reproducible environments
- deterministic scoring where possible
- clear grader limitations
- task quality review
- trace capture
- benchmark versioning
- cost-aware evaluation
- held-out test sets
- model comparisons on the same benchmark

