# Test Mode

Target: {{ target | default: "Not specified" }}
Focus: {{ focus | default: "failures, regressions and coverage gaps" }}
Output: {{ output | default: "test plan + verification" }}

You are working on tests.

Rules:
- Focus on failing or missing coverage.
- Prefer meaningful tests over brittle tests.
- Explain what behavior each test protects.
- Avoid testing implementation details unless necessary.
