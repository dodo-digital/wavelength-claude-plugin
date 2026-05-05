# Changelog

## [1.4.3] - 2026-05-04

### Changed
- Renamed the local `brain` concept to `memory` and made it explicitly MCP-backed.
- Replaced local brain startup initialization with shared memory guidance for `query_context` and `update_context`.
- Added memory references for save types, virtual filesystem conventions, and query policy.
- Updated deal-analysis, red-team, Grata enrichment, and company-processor guidance to query shared memory before relevant work and save durable findings afterward.

## [1.4.2] - 2026-05-04

### Fixed
- MCP server URL now points at the canonical OAuth endpoint `/mcp`.
- Removed the legacy `WL_MCP_TOKEN` Authorization header from plugin MCP config so Claude Code can use OAuth.

## [1.4.1] - 2026-05-04

### Added
- **Auto dependency detection** — SessionStart hook checks for Python 3.9+ and openpyxl on every session. If missing, Claude offers to install them automatically. No manual setup needed.
- **Brain skill** (`/brain`) — Persistent knowledge base that compiles deal research, CIM analyses, and sourcing insights into a structured wiki with linked articles and cross-referenced concepts
- **Red Team skill** (`/red-team`) — Extracted from deal-analysis into standalone skill. Stress-test deals from 3 adversarial perspectives (Skeptical LP, Operating Partner, Industry Insider)
- **SessionStart brain injection** — Wiki index and brain context auto-loaded into every session
- **MCP server bundled** — Plugin declares Wavelength MCP inline in plugin.json, auto-connects on install

### Changed
- Deal Analysis skill now routes red-team requests to `/red-team`
- Removed missing-items agent from deal-analysis memo generation (consolidated into red-team)

### Fixed
- MCP server declaration in plugin.json (inline mcpServers matching Compound Engineering pattern)
- Plugin.json cleaned of invalid fields that blocked installation
- MCP URL path standardized to `/api/mcp`

## [1.1.0] - 2026-04-21

### Added
- **Deal Analysis skill** — Generate investment memos from CIMs, SIMs, or any deal materials
  - 4 modes: Generate memo, Explore deal, Score deal, Red team
  - Full OA memo generation with 8 parallel sub-agents (revenue quality, financial analysis, industry analysis, right-to-win, mission criticality, value creation, risk assessment, missing items)
  - 100-point weighted scorecard aligned to Wavelength ICP (scale, growth, revenue quality, profitability, other factors)
  - OA memo format matched to Wavelength's actual template (header metadata table, Deal Killers with mitigants + tests, thesis section)
  - Interactive explore mode for Q&A and deal sounding board
  - Red team mode with 3 adversarial personas (Skeptical LP, Operating Partner, Industry Insider)
  - Accepts CIMs, SIMs, company documents, or conversation context

## [1.0.0] - 2026-04-20

### Added
- **Plugin structure** — Proper `.claude-plugin/plugin.json` manifest for installation via Claude Code
- **Grata Search Enrichment skill** — Score and rank 400-500 company Grata exports against investment thesis
  - Self-healing schema discovery (adapts when Grata changes export format)
  - Claude reads and scores every company individually (no algorithmic shortcuts)
  - Calibration loop: scores 10 first, asks targeted questions, records learnings
  - Learned adjustments persist across runs per industry
  - Outputs: enriched xlsx (color-coded) + shortlist csv (HIGH + MEDIUM fit)
  - Force-ranking within tiers (H1, H2... M1, M2...)

### Skills included
| Skill | Purpose |
|-------|---------|
| `grata-search-enrichment` | Score Grata exports → prioritized shortlist |
| `company-processor` | Transform shortlist → Reply.io-ready contacts |
| `create-skills` | Create new Claude Code skills |
| `create-hooks` | Create new event-driven hooks |

## [0.1.0] - 2026-04-20

### Added
- Initial grata-search-enrichment skill (basic structure)
- Company-processor skill
- Hook framework with skill router
- MCP setup script
