# Query Generation

Gramorpher generates query test cases based on the specified grammar and corpus, but the specified grammar might have the non-terminal symbols recursively ...

Therefore, Gramorpher takes the following strategies for efficient query generation.

## Strategy 1: Find shallowest grammar form based on corpus symbols