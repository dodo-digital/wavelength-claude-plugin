# Processing Rules — Company Processor

## Known Schema

The Grata export is an .xlsx with three tabs. Schema details live in the grata-search-enrichment skill's `references/grata-schema.md` — this is the single source of truth for column positions and format changes. This file tracks PROCESSING rules specific to the company-processor workflow.

### Expected Tabs

| Tab | Purpose | Key Columns |
|-----|---------|-------------|
| Companies | Company-level data | Name, Description, Revenue Estimate, Headquarters, Year Founded, Executive First Name/Last Name/Title/Email/LinkedIn |
| Top Executive Contacts | Primary contacts | First Name, Last Name, Company, Title, Work Email, LinkedIn, Age |
| Other Executive Contacts | Secondary contacts (often has owners Grata mislabeled) | Same structure as Top Executive Contacts |

### Tab Name Variants

Grata occasionally renames tabs. Match by content pattern, not name.

| Standard Name | Known Variants |
|---------------|----------------|
| Companies | "Company Data", "Company List" |
| Top Executive Contacts | "Top Executives", "Primary Contacts" |
| Other Executive Contacts | "Other Executives", "Additional Contacts", "Secondary Contacts" |

## Role Filter

### Include (owner-operator titles)
- Owner, Co-Owner
- President, Co-President
- Founder, Co-Founder
- CEO, Chief Executive Officer
- Managing Partner, Managing Member
- Principal (if sole/primary)

### Exclude (non-operator roles)
- CFO, CTO, COO, CIO, CISO, CMO
- VP, Vice President
- Director
- Manager
- Board Member, Advisor

### Edge Cases
- "Partner" without "Managing" → include but flag for user review
- "General Manager" → exclude (operational, not ownership)
- "Owner/CTO" dual title → include (owner takes priority)
- "Former CEO" / "Previous Owner" → exclude
- "Interim CEO" → exclude

## Business Model Generation Rules

The `business_model` field is Claude-generated, NOT scripted. Rules for Claude:

- All lowercase except acronyms (OSHA, DOT, IT, MDR, SOC)
- ~3-7 words, specific to what the company does
- Must fit: "I was researching the {industry} sector, specifically companies in {business_model}"
- Based on company description field. If description is empty, use NAICS codes + company name as fallback signals
- NEVER use marketing language ("leading provider", "innovative solutions", "cutting-edge")

### Good Examples
| Description | Business Model |
|-------------|---------------|
| Provides fire inspection and code compliance services | fire inspection and code compliance services |
| Develops DOT and OSHA compliance management software | DOT and OSHA compliance management software |
| Penetration testing and vulnerability assessment firm | penetration testing and vulnerability assessment |
| Managed detection and response for mid-market | managed detection and response services |

### Anti-Patterns
- "fire safety" (too broad — that's the industry)
- "cybersecurity solutions" (generic)
- "technology company" (meaningless)
- "services company" (says nothing)

## Location Parsing

Grata exports location as a single string. Parsing rules:
- Split on comma
- City = first segment, trimmed
- State = second segment, trimmed
- Discard country if present (third segment)
- Keep state as-is (abbreviation or full name)
- ALWAYS use Companies tab → Headquarters, NEVER exec personal location

## Email Validation Thresholds

After Clearout + ZeroBounce validation:
- **Safe to send:** Clearout safe_to_send = "yes" AND ZeroBounce status = "valid"
- **Risky:** Either provider flags as "catch-all" or "unknown"
- **Do not send:** Either provider flags as "invalid", "disposable", or bounce_type = "hard"

Include all contacts in master CSV regardless. Only upload "safe to send" + "risky" (with warning) to Reply.io. Never upload "do not send."

## Deduplication Rules

1. After merging both exec tabs, deduplicate by email address (case-insensitive)
2. If same person appears in both tabs, keep the entry with the more senior title
3. Title seniority order: Owner > Founder > CEO > President > Managing Partner > Principal
4. If same seniority, keep the Top Executive Contacts version (primary tab)

## Learned Adjustments

Run-to-run calibration insights. Load these BEFORE processing. Apply consistently unless user overrides.

Format: `- [{industry}] {adjustment} (learned {date})`

<!-- Adjustments will be added here after each run -->
