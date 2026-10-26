---
name: create-and-validate
description: Add a SlopLang example and exact-output test, then run the full validation suite
---

# Create and Validate

Use this skill when asked to add an example and regression coverage for a SlopLang
language feature and validate the result in one pass.

## Workflow

1. Load the `create-test-program` skill and follow its instructions exactly. This
   skill adds nothing to that workflow; do not duplicate or reinterpret it here.
2. Once the example and its exact-output test are in place, load the `validate`
   skill and follow its instructions.
3. Report the files changed, the example's exact stdout, and the result of each
   validation check. Report failures before proposing fixes.
