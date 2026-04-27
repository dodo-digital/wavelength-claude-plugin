# Wavelength Claude Plugin

A Claude Code plugin for Wavelength Equity's deal sourcing and analysis workflows. Built by [Dodo Digital](https://dododigital.ai).

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Python 3.9+ with `openpyxl` (`pip3 install openpyxl`)

### Install

Open Claude Code and run:

```
/plugin marketplace add dodo-digital/wavelength-claude-plugin
/plugin install wavelength-equity@wavelength
```

The plugin installs permanently and auto-updates when the repo is updated. No further setup needed.

### Wavelength MCP Setup

The plugin connects to Wavelength's hosted MCP server for email validation (Clearout + ZeroBounce). API keys are server-side — team members only need a personal token from Dino.

**Claude Code users:**

1. Get your token from Dino
2. Add to your shell profile: `export WL_MCP_TOKEN="your-token"`
3. Restart Claude Code — tools auto-connect via `.mcp.json`
4. Test: ask Claude to run `check_credits`

**Claude Cowork users:**

1. Get your personal token from Dino
2. Go to Customize > Connectors > Add custom connector
3. Enter URL: `https://wavelength-mcp.vercel.app/mcp/YOUR-TOKEN-HERE`
4. Click Add — tools appear in Cowork conversations

### Other MCP Setup (optional)

If you use additional integrations (Reply.io, OneDrive, etc.), run:

```bash
./scripts/setup-mcps.sh
```

## Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `grata-search-enrichment` | Score Grata exports against thesis, generate prioritized shortlist | Drop a Grata xlsx or say "score companies" |
| `company-processor` | Transform shortlist into Reply.io-ready contact lists | "process companies" or "prepare outreach" |
| `deal-analysis` | Generate OA investment memos, score deals, explore deals, red-team theses | `/deal-analysis` or drop a CIM/SIM |
| `create-skills` | Create new Claude Code skills | `/create-skills` |
| `create-hooks` | Create event-driven hooks | `/create-hooks` |

## Workflows

### Sourcing → Outreach

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

### Deal Analysis

```
CIM / SIM / company docs / conversation context
    ↓
[deal-analysis]  ← 4 modes:
    ├── Generate memo  — Full OA memo (8 parallel sub-agents)
    ├── Explore deal   — Interactive Q&A / sounding board
    ├── Score deal     — 100-point weighted scorecard
    └── Red team       — Stress-test from 3 adversarial perspectives
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
├── skills/
│   ├── grata-search-enrichment/   # Grata export scoring
│   ├── company-processor/         # Contact list prep
│   ├── deal-analysis/             # Investment memo generation
│   │   ├── SKILL.md              # Router (4 modes)
│   │   ├── workflows/            # generate-memo, explore, score, red-team
│   │   ├── references/           # 10 analysis dimensions + scoring
│   │   └── templates/            # OA memo template
│   ├── create-skills/
│   └── create-hooks/
├── hooks/
│   ├── hooks.json                 # Hook manifest (plugin convention)
│   └── router/                    # Event router framework
├── CLAUDE.md                      # Project instructions
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
