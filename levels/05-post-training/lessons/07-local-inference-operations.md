# Lesson 7: Local Inference Operations

## Core Idea

A local model is not adopted when it produces a checkpoint. It is adopted when applications can call it reliably, observe it, and survive its failure modes.

This lesson is about serving operations. It can use a base open model, an adapted model from Track 5B, or a smaller CPU/edge model.

## Serving Stack

A practical local inference stack usually has four layers:

1. Client compatibility: an OpenAI-compatible endpoint so the agent does not need model-specific client code.
2. Gateway: routing, aliases, retries, fallbacks, rate limits, usage accounting, and health checks.
3. Inference workers: local engines that serve one or more models.
4. Operations: containers, private networking, metrics, logs, restart policy, and failure drills.

## What To Learn

- How to expose a model through an OpenAI-compatible API.
- How to place a gateway in front of one or more inference workers.
- How to configure model aliases without binding course material to one specific model.
- How to route to local, hosted, or hybrid backends through the same agent interface.
- How to define fallback behavior for connection errors, timeouts, saturation, and unhealthy workers.
- How to measure time to first token, total latency, tokens per second, error rate, request volume, and memory pressure.
- How to distinguish model quality failures from serving failures.

## Tool Categories

The specific tools will change. The categories matter more than any one vendor or model:

- Gateway or proxy: provides client compatibility, routing, fallback, auth, limits, and accounting. Examples include LiteLLM Proxy, Envoy, and OpenResty.
- High-throughput inference engine: serves GPU-backed models with batching and efficient KV-cache management. Examples include vLLM and equivalent serving engines.
- Edge or low-resource runtime: serves quantized models on constrained hardware. Examples include llama.cpp, Ollama, and equivalent runtimes.
- Structured-output-focused runtime: optimizes constrained decoding, caching, or low-latency agent outputs. Examples include SGLang and equivalent runtimes.
- Container runtime: packages serving dependencies and isolates CUDA or runtime versions. Examples include Docker with GPU runtime support.
- Private network or tunnel: exposes the worker only to trusted clients. Examples include private mesh networks, VPNs, and tunnel services.
- Metrics stack: records request, latency, token, error, and resource signals. Examples include Prometheus-compatible metrics and dashboarding tools.

## Failure Modes

Plan for:

- worker process crash
- model load failure
- endpoint timeout
- GPU or memory exhaustion
- malformed model output
- gateway misrouting
- fallback provider outage
- unexpected cost spike after fallback
- private network disconnect

## Checkpoint

You are ready for the lab when the agent can call a gateway endpoint instead of calling a model provider directly, and you can explain what should happen when the local worker becomes unhealthy.
