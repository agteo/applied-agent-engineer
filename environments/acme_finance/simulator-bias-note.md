# Simulator Bias Note

This simulator is deterministic and fixture-sized. It is useful for teaching state transitions, verifier design, reward decomposition, and rollout logging, but it is easier than a real finance operations environment.

Scope: expense reimbursement only. The state schema names drafts, approvals, and submitted reports; invoices, purchase orders, vendors, reconciliation records, and the exception queue are not implemented and should not be described as if they were.

Known omissions: messy OCR, partial receipts, changing policies, multi-actor delays, adversarial vendors, real payment rails, ambiguous human approvals, and any model-based verifier.

Treat high simulator reward as readiness for harder evaluation, not proof of production reliability.
