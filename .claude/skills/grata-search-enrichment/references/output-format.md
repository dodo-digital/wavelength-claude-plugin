# Output Format — Grata Search Enrichment

## File Naming

- Enriched: `{industry}-{YYYY-MM-DD}-enriched.xlsx`
- Shortlist: `{industry}-{YYYY-MM-DD}-shortlist.csv`

Industry slug is lowercase, hyphenated (e.g., "fire-safety", "cybersecurity", "vertical-software").

## Enriched XLSX — All Companies

### Sheet 1: Enriched Companies

| # | Column | Source | Description |
|---|--------|--------|-------------|
| 1 | force_rank | Enrichment | H1, H2, M1, M2, L |
| 2 | fit_rating | Enrichment | HIGH, MEDIUM, LOW |
| 3 | descriptor | Enrichment | ~5 word description of what company does |
| 4 | rationale | Enrichment | 1-2 sentence explanation of rating |
| 5+ | (all original Grata columns) | Grata export | Preserved as-is from source |
| Last | owner_signals | Enrichment | Evidence of owner-operator (from exec tabs) |

**Formatting:**
- Bold header row
- Auto-width columns (max 50 chars)
- Conditional row fill: GREEN for HIGH, YELLOW for MEDIUM, no fill for LOW
- Sorted by force_rank (H1 first, then H2, ..., M1, M2, ..., L)

### Sheet 2: Summary

| Row | Content |
|-----|---------|
| 1 | Total Companies: {n} |
| 2 | HIGH fit: {n} |
| 3 | MEDIUM fit: {n} |
| 4 | LOW fit: {n} |

## Shortlist CSV — High-Fit Only

For quick review, Grata re-curation, or HubSpot import.

| # | Column | Description |
|---|--------|-------------|
| 1 | force_rank | H1, H2, H3... |
| 2 | company_name | From Grata Companies tab |
| 3 | descriptor | Generated ~5 word description |
| 4 | rationale | Why this company is high-fit |
| 5 | revenue | Grata revenue estimate |
| 6 | employees | Employee count |
| 7 | year_founded | 4-digit year |
| 8 | hq | Headquarters location |
| 9 | website | Company website URL |
| 10 | owner_signals | Owner-operator evidence |

**Sort order:** By force_rank ascending (H1, H2, H3...).

**Encoding:** UTF-8, standard CSV (comma-delimited, quoted strings where needed).

## Data Quality Flags

During preview (step 6), report these flags:
- Companies with no description (cannot generate descriptor confidently)
- Companies with revenue outside thesis range
- Companies with no founding year
- Companies where owner presence cannot be determined
- Any companies that required assumptions (flagged in rationale)
