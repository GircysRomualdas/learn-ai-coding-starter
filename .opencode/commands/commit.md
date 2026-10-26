---
description: Review the diff, commit project changes, then rebase on origin/main
---

Review the pending diff with `git status` and `git diff` before committing.
Then stage and commit the project changes with `$ARGUMENTS` as the commit
message. After the commit succeeds, run `git pull --rebase origin main`.

Report the commit hash, commit message, and the result of the rebase.
