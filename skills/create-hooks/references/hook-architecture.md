<overview>
Technical reference for the hook router framework. Covers the dispatch loop, handler results, decision priority, and output formatting.
</overview>

<framework_flow>
The router framework processes hooks in this order:

1. **parse_stdin()** — Read JSON from stdin (Claude Code provides event data)
2. **matches()** — Filter handlers by matcher regex against tool_name or event matcher
3. **run_handler()** — Execute each matching handler, catch exceptions
4. **combine_results()** — Merge all handler results following priority rules
5. **format_output()** — Convert to event-specific JSON format for stdout
6. **Exit** — Exit with combined exit code (0 = success, 2 = block)
</framework_flow>

<handler_result>
Every handler returns a `HandlerResult` dataclass:

```python
@dataclass
class HandlerResult:
    decision: Decision = Decision.NONE      # APPROVE/BLOCK/ASK/NONE
    reason: str = ""                         # Human-readable reason
    additional_context: str = ""             # Injected into agent prompt
    stderr_message: str = ""                 # Visible in terminal
    exit_code: int = 0                       # 0=success, 2=block
    suppress_further: bool = False           # Skip remaining handlers
```

Decisions:
- **NONE** — No opinion (default). Other handlers can still decide.
- **APPROVE** — Allow the action. Lower priority than BLOCK.
- **ASK** — Prompt the user for confirmation.
- **BLOCK** — Deny the action. Highest priority, overrides all others.
</handler_result>

<decision_priority>
When multiple handlers return results, they're combined by priority:

```
BLOCK > ASK > APPROVE > NONE
```

If any handler returns BLOCK, the combined result is BLOCK regardless of other handlers.
Context from all handlers is concatenated. Exit code is max of all handlers.
</decision_priority>

<output_formats>
Different events expect different JSON output:

**PreToolUse:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny|ask|allow",
    "permissionDecisionReason": "reason",
    "additionalContext": "injected text"
  }
}
```

**UserPromptSubmit:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "injected text"
  }
}
```

**SessionStart / PreCompact:**
```json
{
  "additionalContext": "injected text"
}
```

**PostToolUse:**
```json
{
  "message": "feedback text"
}
```

**Stop:**
```json
{
  "decision": "block|approve",
  "reason": "reason"
}
```
</output_formats>

<input_data>
Each event provides different data via stdin:

**UserPromptSubmit:**
- `prompt` — The user's input text

**PreToolUse:**
- `tool_name` — Name of the tool being called (e.g., "Write", "Bash", "Edit")
- `tool_input` — The tool's parameters as a dict

**PostToolUse:**
- `tool_name` — Name of the tool that was called
- `tool_input` — The tool's parameters
- `tool_result` — The tool's output

**SessionStart:**
- `matcher` — One of "startup", "compact", or "clear"
</input_data>

<handler_registration>
Handlers are registered in event entry point files:

```python
#!/usr/bin/env python3
"""EventName event router."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router.framework import dispatch
from router.models import HandlerConfig
from router.handlers.module_name import handler_function

HANDLERS = [
    HandlerConfig(
        fn=handler_function,
        matcher=r"Write|Edit",    # Optional: only match these tools
        name="handler-name",      # For logging
    ),
]

if __name__ == "__main__":
    dispatch(HANDLERS, "EventName")
```

The `matcher` field is a regex pattern:
- For PreToolUse/PostToolUse: matches against `tool_name`
- For SessionStart: matches against `matcher` field (startup/compact/clear)
- If `None`: handler always runs
</handler_registration>

<best_practices>
- Handler errors are caught, not fatal — always wrap risky operations in try/except
- Use `stderr_message` for terminal-visible output (debugging)
- Use `additional_context` for prompt-visible output (injecting instructions)
- Use `suppress_further=True` to short-circuit remaining handlers
- Keep handlers fast — each has a timeout (default 10 seconds)
- One handler per domain concern (skills, git, validation)
</best_practices>
