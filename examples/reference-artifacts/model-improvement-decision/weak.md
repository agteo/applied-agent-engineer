# Weak Model Improvement Decision: Acme Expense Agent v1

We should fine-tune a smaller model because the agent has some failures and we
now have a dataset. The model will probably learn the policies and make fewer
mistakes. If fine-tuning does not work, we can try prompt engineering.

## Why This Is Weak

This decision treats any dataset as a reason to train. It does not compare
prompting, tool fixes, retrieval, frontier APIs, or local model adaptation, and
it does not state which benchmark result would prove the training worked.
