---
name: create-hooks
description: Create Claude Code hooks for validation, routing, and guardrails. Use when adding event-driven automations, validation gates, or context injection to the plugin.
context_budget:
  skill_md: 150
  max_references: 2
---

<auto_trigger>
keywords:
  - "create hook"
  - "new hook"
  - "add hook"
  - "build hook"
  - "hook handler"
  - "guardrail"
  - "validation gate"

intent_patterns:
  - "create.*hook"
  - "add.*hook"
  - "add.*guardrail"
  - "add.*validation"
</auto_trigger>

<objective>
Create event-driven hooks that intercept Claude Code actions for validation, context injection, or guardrails. Hooks use the router framework pattern: a handler function receives event data and returns a decision (approve, block, ask) with optional context.
</objective>

<quick_start>
1. Decide which event to hook (UserPromptSubmit, PreToolUse, PostToolUse, SessionStart, Stop)
2. Create a handler function in `hooks/router/handlers/`
3. Register the handler in the event's entry point script
4. Add the event to `hooks/hooks.json` if not already registered
</quick_start>

<process>
1. **Identify the event** [LOW freedom]
   Choose from available hook events:
   | Event | When It Fires | Common Uses |
   |-------|---------------|-------------|
   | `UserPromptSubmit` | User sends a prompt | Skill routing, context injection |
   | `PreToolUse` | Before a tool executes | Validation gates, permission checks |
   | `PostToolUse` | After a tool executes | Post-action handlers, logging |
   | `SessionStart` | Session begins | Initialization, git sync |
   | `Stop` | Session ends | Cleanup, auto-commit |

2. **Create the handler** [MEDIUM freedom]
   Create a new file in `hooks/router/handlers/` or add a function to an existing handler file.

   Handler signature:
   ```python
   from ..models import HandlerResult, Decision

   def my_handler(input_data: dict) -> HandlerResult | None:
       """EventName: what this handler does."""
       # Extract relevant data from input_data
       # input_data keys vary by event:
       #   UserPromptSubmit: prompt
       #   PreToolUse: tool_name, tool_input
       #   PostToolUse: tool_name, tool_input, tool_result
       #   SessionStart: matcher (startup/compact/clear)

       # Return a result
       return HandlerResult(
           decision=Decision.APPROVE,  # or BLOCK, ASK, NONE
           reason="Why this decision",
           additional_context="Text injected into agent prompt",
       )
   ```

3. **Register the handler** [LOW freedom]
   Edit the event's entry point in `hooks/router/`:

   ```python
   # In {event_name}.py
   from router.handlers.{module} import my_handler

   HANDLERS = [
       # ... existing handlers
       HandlerConfig(
           fn=my_handler,
           matcher=r"regex_pattern",  # Optional: filter by tool name
           name="my-handler",
       ),
   ]
   ```

4. **Register the event** [LOW freedom]
   If the event isn't already in `hooks/hooks.json`, add it:

   ```json
   {
     "hooks": {
       "EventName": [
         {
           "matcher": "optional_regex",
           "hooks": [
             {
               "type": "command",
               "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/router/{event_name}.py",
               "timeout": 10
             }
           ]
         }
       ]
     }
   }
   ```

5. **Test the hook** [MEDIUM freedom]
   Run Claude Code and trigger the event. Check stderr for handler output.
   Verify the hook fires by checking for `[router]` messages in terminal output.
</process>

<references_index>
| Reference | Purpose |
|-----------|---------|
| references/hook-architecture.md | Framework internals, decision priority, output formats |
</references_index>

<success_criteria>
- [ ] Handler function created with correct signature
- [ ] Handler registered in event entry point
- [ ] Event registered in hooks/hooks.json (if new)
- [ ] Handler returns appropriate decision type
- [ ] Matcher regex filters correctly (if applicable)
- [ ] Hook tested and fires on expected events
</success_criteria>
