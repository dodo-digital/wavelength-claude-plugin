# Wavelength Claude Plugin

A Claude Code plugin for Wavelength Equity's deal sourcing and analysis workflows. Built by [Dodo Digital](https://dododigital.ai).

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Python 3.9+ with `openpyxl` (`pip3 install openpyxl`)

### Install as Plugin

```bash
claude /plugin install github:dodo-digital/wavelength-claude-plugin
```

This installs the plugin and all its skills into your Claude Code environment. Skills update automatically when the plugin updates.

### Manual Install (alternative)

```bash
git clone git@github.com:dodo-digital/wavelength-claude-plugin.git
cd wavelength-claude-plugin
claude
```

### MCP Setup (optional)

If you use external integrations (ZeroBounce, Reply.io, etc.), run:

```bash
./scripts/setup-mcps.sh
```

## Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `grata-search-enrichment` | Score Grata exports against thesis, generate prioritized shortlist | Drop a Grata xlsx or say "score companies" |
| `company-processor` | Transform shortlist into Reply.io-ready contact lists | "process companies" or "prepare outreach" |
| `create-skills` | Create new Claude Code skills | `/create-skills` |
| `create-hooks` | Create event-driven hooks | `/create-hooks` |

## Workflow

```
Grata export (400-500 companies)
    ↓
[grata-search-enrichment]  ← scores, ranks, outputs shortlist
    ↓
Human review (pick top targets)
    ↓
[company-processor]  ← enriches contacts, validates emails, formats for Reply.io
    ↓
Reply.io upload
```

## What Grata Search Enrichment Does

1. **Discovers schema** — Reads your Grata xlsx, adapts to format changes automatically
2. **Asks industry + exclusions** — One question to configure the run
3. **Calibrates** — Scores first 10 companies, asks 3-5 targeted questions, records learnings
4. **Scores every company** — Claude reads each company individually and rates fit (HIGH/MEDIUM/LOW)
5. **Force-ranks** — Orders companies within each tier (H1, H2... M1, M2...)
6. **Outputs files** — Enriched xlsx (color-coded) + shortlist csv (HIGH + MEDIUM)

Learned adjustments persist between runs. Each industry gets smarter over time.

## Output Files

| File | Contents |
|------|----------|
| `{industry}-{date}-enriched.xlsx` | All companies with fit rating, descriptor, rationale, color-coding |
| `{industry}-{date}-shortlist.csv` | HIGH + MEDIUM companies only, sorted by rank |

## Project Structure

```
wavelength-claude-plugin/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── .claude/
│   ├── settings.json            # Permissions and hook config
│   ├── skills/
│   │   ├── grata-search-enrichment/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── discover_export.py
│   │   │   │   └── format_output.py
│   │   │   └── references/
│   │   │       ├── grata-schema.md
│   │   │       ├── scoring-criteria.md
│   │   │       └── output-format.md
│   │   ├── company-processor/
│   │   ├── create-skills/
│   │   └── create-hooks/
│   └── hooks/
│       └── router/
├── CLAUDE.md                    # Project instructions
├── CHANGELOG.md
├── README.md
└── scripts/
    └── setup-mcps.sh
```

## Updating

If installed as a plugin, updates pull automatically. For manual installs:

```bash
cd wavelength-claude-plugin && git pull
```

## Support

Contact [Dodo Digital](https://dododigital.ai) for questions or new workflow requests.
