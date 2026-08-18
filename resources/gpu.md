# GPU Resources

The core capstone does not require a GPU.

The advanced model adaptation capstone requires access to GPU compute for SFT or LoRA training. Learners may use any approved environment that fits their budget, data policy, and hardware needs.

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
- estimated cost
- training command
- dependency versions
- model license
- data privacy assumptions

## Recommendation

Use the smallest model and smallest dataset that can test the learning objective.

The capstone is not about chasing leaderboard performance. It is about proving that a local model adaptation can be run, evaluated, and judged honestly against alternatives.

