# StrongBench Failure Taxonomy

- `EVALUATION.expected_answer_wrong`: The expected answer may be wrong or underspecified.
- `MODEL.instruction_following`: The answer ignores a required boundary such as employee-only submission.
- `MODEL.reasoning`: Wrong arithmetic, category interpretation, or policy application in the final answer.
- `RETRIEVAL.citation`: The answer omitted an expected policy source.
- `TOOLS.arguments`: The agent called a tool with arguments that were too broad, too narrow, or malformed.
- `TOOLS.interpretation`: The agent saw the tool result but reported the wrong operational conclusion.
- `TOOLS.selection`: A required tool was not called.
