# Wavelength Equity — Claude Code Plugin

A deal sourcing and analysis toolkit for Wavelength Equity. Skills automate repeatable workflows. Hooks enforce guardrails and route skills automatically.

<behaviors>
- **Use skills.** Invoke existing skills rather than reinventing workflows.
- **Start simple.** Solve with the smallest change first. Add complexity only after simpler approach fails.
- **Parallel over sequential.** Run independent tool calls concurrently.
- **Never guess secrets.** API keys and credentials come from environment variables or OS keychain. Never hardcode.
- **Ask before destructive actions.** Confirm with the user before deleting files, force-pushing, or modifying shared state.
</behaviors>

<skills>
Skills live in `.claude/skills/`. Each has a `SKILL.md` with YAML frontmatter and XML-structured instructions.

**Built-in skills:**
| Skill | Purpose |
|-------|---------|
| `create-skills` | Create new skills with proper structure |
| `create-hooks` | Create new hooks for validation and routing |

**Skill structure:**
```
skill-name/
├── SKILL.md              # Router (max 200 lines)
├── workflows/            # One per use case
├── references/           # Shared knowledge
└── templates/            # Output formats
```

**Key principles:**
1. Progressive disclosure — load only what's needed
2. Pure XML structure — use `<tags>` not `## headings` in skill bodies
3. Context budgets — every skill declares its token cost
4. Required reading — workflows declare which references to load
</skills>

<hooks>
Hooks live in `.claude/hooks/router/`. The framework dispatches to handlers based on event type and matchers.

**Hook events:**
- `UserPromptSubmit` — Runs when user sends a prompt. Used for skill routing.
- `PreToolUse` — Runs before a tool executes. Used for validation gates.
- `PostToolUse` — Runs after a tool executes. Used for post-action handlers.
- `SessionStart` — Runs when a session begins. Used for initialization.
- `Stop` — Runs when a session ends. Used for cleanup.

**Adding hooks:** Use the `create-hooks` skill or manually add handlers in `.claude/hooks/router/handlers/`.
</hooks>

<guardrails>
**Forbidden:**
- Committing API keys, credentials, or `.env` files
- Running destructive commands without confirmation
- Guessing personal or business details

**Constrained:**
- File deletion → confirm with user first
- Sensitive API calls → validate payload before sending
- Multi-step workflows → checkpoint progress
</guardrails>
