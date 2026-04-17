# Wavelength Claude Plugin

A Claude Code plugin for Wavelength Equity's deal sourcing and analysis workflows. Built by [Dodo Digital](https://dododigital.ai).

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Git installed
- Python 3.9+ (for hooks)

### Setup

1. Clone this repo:

```bash
git clone git@github.com:dodo-digital/wavelength-claude-plugin.git
cd wavelength-claude-plugin
```

2. Run the MCP setup script to configure external tool integrations:

```bash
./scripts/setup-mcps.sh
```

3. Open Claude Code in this directory:

```bash
claude
```

That's it. Claude Code automatically loads the `CLAUDE.md` instructions, skills, and hooks from the `.claude/` directory.

### Verify Installation

Run these commands inside Claude Code to verify everything is working:

```
/create-skills
```

You should see the skill creation wizard activate. Type `/create-hooks` to verify the hook creation skill.

## What's Included

### Skills

Skills are modular capabilities that Claude Code can invoke. Each skill lives in `.claude/skills/` and contains a `SKILL.md` file with instructions.

| Skill | Purpose |
|-------|---------|
| `company-processor` | Transform Grata exports into validated Reply.io-ready contact lists |
| `create-skills` | Create new Claude Code skills with proper structure and context engineering |
| `create-hooks` | Create new hooks (event-driven automations) for validation, routing, and guardrails |

### Hooks

Hooks are event-driven scripts that run automatically during Claude Code sessions. They live in `.claude/hooks/`.

| Hook | Event | Purpose |
|------|-------|---------|
| Skill Router | `UserPromptSubmit` | Auto-detects which skill to activate based on your prompt |

### How Skills Work

Skills follow a progressive disclosure pattern:

```
Layer 1: Metadata (name, description) → loaded at startup (~50 tokens)
Layer 2: SKILL.md → loaded when skill triggers
Layer 3: References/workflows → loaded on-demand during execution
```

Each skill folder can contain:

```
skill-name/
├── SKILL.md              # Main instructions (required)
├── workflows/            # Step-by-step procedures (optional)
├── references/           # Shared knowledge (optional)
├── templates/            # Output formats (optional)
└── scripts/              # Automation scripts (optional)
```

### How Hooks Work

Hooks intercept Claude Code events and can inject context, block actions, or validate outputs. The hook framework uses a router pattern:

1. An event fires (e.g., user submits a prompt)
2. The router dispatches to matching handlers
3. Handlers return decisions (approve, block, ask) and optional context
4. Results are combined and returned to Claude Code

## Adding New Skills

Use the built-in skill:

```
/create-skills
```

Or manually create a folder in `.claude/skills/` with a `SKILL.md` file. After adding a skill, the skill router will automatically detect it on the next prompt.

## Adding New Hooks

Use the built-in skill:

```
/create-hooks
```

This guides you through creating a new handler and registering it in the hook router.

## Team Usage

Each team member should:

1. Clone this repo
2. Have their own Claude Code subscription (Pro or Team)
3. Add any personal API keys to their OS keychain (never commit secrets)

## MCP Integrations

External tools are connected via MCP (Model Context Protocol) servers. Run `./scripts/setup-mcps.sh` to configure.

| Tool | MCP Status | Notes |
|------|-----------|-------|
| ZeroBounce | Ready — `@zerobounce/mcp` (npm) | Email validation. Official MCP. |
| Clearout | Custom needed | Email validation. REST API available, no standalone MCP. |
| Reply.io | Custom needed | Official MCP is search-only (limited). Need custom for uploads. |
| OneDrive | Manual setup | Community MCPs available. Requires Azure app registration. |
| HubSpot | Optional | Grata syncs directly. Add if needed for other workflows. |
| Apollo | Available — community | Contact enrichment. Multiple GitHub implementations. |
| ProxyCurl | Available — community | LinkedIn enrichment. Node.js-based MCP. |
| Grata | N/A | No API. Input is always a file export. |

## Project Structure

```
wavelength-claude-plugin/
├── CLAUDE.md                    # Project-level instructions for Claude
├── README.md                    # This file
├── scripts/
│   └── setup-mcps.sh           # MCP server configuration script
├── .claude/
│   ├── settings.json            # Hook registrations and permissions
│   ├── skills/                  # Modular capabilities
│   │   ├── company-processor/   # Grata export → Reply.io workflow
│   │   ├── create-skills/       # Skill for creating new skills
│   │   └── create-hooks/        # Skill for creating new hooks
│   └── hooks/
│       └── router/              # Event-driven hook framework
│           ├── framework.py     # Core dispatch loop
│           ├── models.py        # Data types
│           ├── handlers/        # Domain-specific handlers
│           └── skill-router/    # Auto-skill detection
└── .gitignore
```

## Support

Contact [Dodo Digital](https://dododigital.ai) for questions or to request new workflows.
