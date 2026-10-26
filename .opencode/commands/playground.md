---
description: Start the SlopLang playground, reusing an existing server when present
---

Start the SlopLang playground on port `$ARGUMENTS`, defaulting to `8080` when
`$ARGUMENTS` is empty.

These are the current TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Check the output for an existing Sloperator server. If one is already listening,
report its port and URL and do not start another. Otherwise, run
`uv run playground/server.py $ARGUMENTS` in the background, using `8080` when
`$ARGUMENTS` is empty, and report the URL it prints.
