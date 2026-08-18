# GPU Resources

The core capstone does not require a GPU.

The advanced model adaptation capstone requires access to GPU compute for SFT or LoRA training. Learners may use any approved environment that fits their budget, data policy, and hardware needs.

## What It Actually Costs

The question a learner needs answered before Lab 3 is not "which provider" but "how many dollars". Here are worked estimates for the Track 5B run: a LoRA or QLoRA fine-tune on Agent Training Dataset v1 from Level 4 — on the order of 500-2,000 agent trace examples, roughly 1-2k tokens each, for 2-3 epochs.

| Setup | GPU | Rough runtime | On-demand rate | Estimated cost |
| --- | --- | --- | --- | --- |
| QLoRA, 1-3B model | T4 16GB | 45-90 min | ~$0.35/hr | **under $1** |
| QLoRA, 7-8B model | L4 24GB | 1.5-3 hr | ~$0.70/hr | **$1-2** |
| LoRA, 7-8B model | A100 40GB | 30-60 min | ~$1.30-3.70/hr | **$1-4** |
| LoRA, 13B model | A100 80GB | 1-2 hr | ~$1.90-4.50/hr | **$2-9** |

The honest headline: **a Track 5B training run costs a few dollars, not a few hundred.** If your estimate comes out above about $25, you have chosen too large a model or too large a dataset for the learning objective — go smaller.

What actually costs money is everything around the run. Budget for it:

- **Failed runs.** Assume three to five attempts before a run you would report. Multiply the table above accordingly.
- **Idle VMs.** A forgotten A100 costs roughly $30 in a nine-hour workday and around $90 over a weekend. This is the single most common way learners lose money on this track. Set a shutdown timer on creation, not after.
- **Persistent disk and snapshots**, which keep billing after the VM stops.
- **Egress**, if you pull checkpoints down instead of evaluating in place.

Two cheaper paths, both legitimate for the capstone:

- **Colab free tier** is genuinely enough for a QLoRA run on a 1-3B model. The costs are runtime disconnects and losing your session, not dollars. Checkpoint to Drive every few hundred steps.
- **Colab Pro at about $10/month** buys more reliable GPU access and longer runtimes, which is usually a better deal than per-hour VM rental for a single capstone.

Estimate VRAM before you rent anything. A rough rule for QLoRA: 4-bit base weights need about 0.6GB per billion parameters, then roughly double it for activations, optimizer state, and a sane batch size. An 8B model in QLoRA fits comfortably in 24GB; in full LoRA at bf16 it does not.

Rates above are on-demand list prices from major clouds and GPU marketplaces, checked in August 2026, and rounded. They move, they vary several-fold by region and provider, and spot or preemptible instances run 60-80% cheaper if your run can survive interruption. **Check current pricing before you commit** — the point of this table is the order of magnitude, not the decimal.

## Managed Notebooks

Managed notebooks are usually the fastest way to start.

- [Google Colab](https://developers.google.com/colab)
- [Google Colab FAQ](https://research.google.com/colaboratory/intl/en-GB/faq.html)

Use these when:

- the dataset is small
- privacy constraints are low
- the learner wants the simplest setup

Watch for:

- runtime limits
- variable GPU availability
- storage limits
- data governance constraints

## Cloud GPU VMs

Cloud VMs are closer to production infrastructure.

- [Google Cloud GPUs](https://cloud.google.com/gpu)
- [Google Cloud Compute Engine GPU overview](https://docs.cloud.google.com/compute/docs/gpus/overview)
- [Google Cloud GPU pricing](https://cloud.google.com/products/compute/gpus-pricing)

Use these when:

- the learner needs more control
- training needs longer runtimes
- cost estimates matter
- the project should resemble company infrastructure

Watch for:

- quota approvals
- region availability
- storage and networking costs
- shutdown discipline

## NVIDIA Software And Containers

NVIDIA resources are useful when working with NVIDIA GPUs, enterprise environments, or containerized training stacks.

- [NVIDIA NGC](https://www.nvidia.com/en-us/gpu-cloud/)
- [NVIDIA NGC Catalog](https://catalog.ngc.nvidia.com/)
- [NVIDIA NGC documentation](https://docs.nvidia.com/ngc/index.html)
- [NVIDIA NGC Catalog User Guide](https://docs.nvidia.com/ngc/latest/ngc-catalog-user-guide.html)

Use these when:

- the learner needs GPU-optimized containers
- the environment is enterprise or on-prem
- reproducibility and deployment portability matter

Watch for:

- driver compatibility
- CUDA versions
- container runtime setup
- organization security requirements

## Required Capstone Notes

For the advanced GPU capstone, learners must include:

- provider or hardware used
- GPU model if known
- runtime
- actual cost, including failed runs, not just the successful one
- training command
- dependency versions
- model license
- data privacy assumptions

## Recommendation

Use the smallest model and smallest dataset that can test the learning objective.

The capstone is not about chasing leaderboard performance. It is about proving that a local model adaptation can be run, evaluated, and judged honestly against alternatives.

