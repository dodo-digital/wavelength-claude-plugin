# Scoring Criteria — Grata Search Enrichment

## General Investment Thesis

From Wavelength Equity identity:
- **Fund:** Search fund, lower middle market
- **Thesis:** Bootstrapped, founder-owned services businesses with recurring revenue
- **Sectors:** Cybersecurity, fire safety, vertical software
- **Filters:** USA only, no prior investor funding, owner/operator near retirement preferred
- **Revenue:** $2M–$70M (Grata estimates, acknowledged unreliable)

## Tier Definitions

### HIGH — Strong thesis alignment
- Services business (inspection, consulting, managed services, SaaS+services)
- Recurring or repeat revenue model
- Revenue $2M–$70M estimated
- Founded 15+ years ago (owner likely near retirement)
- Owner-operator signals present (founder still listed, small team, no institutional backing)
- No VC/PE funding history
- USA headquarters

### MEDIUM — Partial alignment or edge cases
- Meets most criteria but one dimension is unclear or borderline
- Revenue outside range but close ($1.5M or $80M)
- Founded 10-14 years ago
- Mixed services/product model
- Owner presence unclear but no institutional signals
- Industry adjacent (e.g., environmental consulting for fire safety search)

### LOW — Does not fit thesis
- Pure product company (hardware, consumer goods)
- Construction, general contracting
- VC-backed or PE portfolio company
- MSP/reseller (low margins, commodity)
- Founded < 5 years ago (too early)
- International headquarters
- Revenue clearly under $1M or over $100M
- No services component

## Sector-Specific Criteria

### Fire Safety
- **YES:** Fire inspection, fire suppression service, fire alarm monitoring, code compliance consulting, fire protection engineering, sprinkler installation/maintenance
- **NO:** Fire truck manufacturing, construction, general HVAC, home security (consumer), fire damage restoration

### Cybersecurity
- **YES:** Penetration testing, vulnerability assessment, managed detection and response (MDR), security consulting, compliance auditing, incident response, security awareness training
- **NO:** MSP/reseller (SentinelOne partner), consumer antivirus, hardware firewall manufacturer, general IT support with "cyber" in name

### Vertical Software
- **YES:** Niche SaaS serving specific industry + professional services (implementation, consulting), inspection management software, compliance platforms with services arm
- **NO:** Consumer apps, horizontal SaaS (CRM, HR), pure platform plays, marketplace models

<per_industry_thesis>
<!-- STATUS: NOT YET AVAILABLE -->
<!-- Dino has not yet shared per-industry thesis documents. When received, add detailed criteria here. -->
<!-- Until then, use the general thesis + sector-specific criteria above. -->
</per_industry_thesis>

## Descriptor Rules

The descriptor is a ~5-word lowercase phrase describing what the company does.

**Format:**
- All lowercase except acronyms (OSHA, DOT, IT, MDR)
- Must fit naturally in: "They do {descriptor}"
- 3–7 words, specific enough to distinguish from peers
- Based on company description and available data — never fabricated

**Good examples:**
- "fire inspection and code compliance services"
- "penetration testing and vulnerability assessment"
- "OSHA compliance management software"
- "managed detection and response services"
- "commercial fire sprinkler maintenance"

**Bad examples (anti-patterns):**
- "fire safety" (too broad — that's the industry, not the descriptor)
- "cybersecurity solutions provider" (generic marketing language)
- "technology company" (meaningless)
- "B2B SaaS platform for enterprise" (buzzwords, not specific)
- "leading provider of innovative services" (marketing fluff)

## Force-Ranking Signals

Within each tier, rank by (in priority order):
1. **Thesis alignment strength** — how cleanly does it match? No asterisks vs. "probably fits"
2. **Description clarity** — can you confidently say what they do? Clear > ambiguous
3. **Revenue fit** — closer to sweet spot ($5M–$30M) ranks higher
4. **Founding year** — older = more likely owner retirement ready
5. **Owner-operator presence** — founder name visible, small exec team, no board listed

## Ranking Format

- `H1, H2, H3...` — High-fit companies, ranked
- `M1, M2, M3...` — Medium-fit companies, ranked
- `L` — Low-fit companies (not individually ranked, all get "L")

## Learned Adjustments

Calibration insights from previous runs. Load these BEFORE scoring. Apply consistently unless user overrides.

Format: `- [{industry}] {adjustment} (learned {date})`

<!-- Adjustments are appended here by the calibration step (process step 4). -->
<!-- Example: -->
<!-- - [cybersecurity] MSP with dedicated SOC and own analysts = MEDIUM, pure reseller = LOW (learned 2026-04-20) -->
<!-- - [cybersecurity] Owner age under 50 with no succession signals = downgrade by one tier (learned 2026-04-20) -->
<!-- - [fire safety] Fire damage restoration is OUT of scope, fire suppression maintenance is IN (learned 2026-04-21) -->
