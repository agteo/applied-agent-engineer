# Simulator Bias Note

This simulator is deterministic and fixture-sized. It is useful for teaching state transitions, verifier design, reward decomposition, and rollout logging, but it is easier than a real finance operations environment.

Known omissions: messy OCR, partial receipts, changing policies, multi-actor delays, adversarial vendors, real payment rails, and ambiguous human approvals. Treat high simulator reward as readiness for harder evaluation, not proof of production reliability.
