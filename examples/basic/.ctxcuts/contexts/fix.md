# Fix Mode

Target: {{ target | default: "Not specified" }}
Focus: {{ focus | default: "root cause and smallest safe change" }}
Output: {{ output | default: "patch plan + verification" }}

You are fixing a specific issue.

Rules:
- Make the smallest safe change.
- Avoid unrelated refactors.
- Preserve existing behavior unless explicitly required.
- Explain the root cause.
- Include tests or verification steps.
