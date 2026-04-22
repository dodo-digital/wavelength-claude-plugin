# Changelog

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
