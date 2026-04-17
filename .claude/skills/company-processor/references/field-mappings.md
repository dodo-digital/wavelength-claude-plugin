<overview>
Column specifications for the Reply.io upload CSV. Derived from Wavelength's current upload template and Grata export structure. This is the single source of truth for field names, sources, and formatting rules.
</overview>

<grata_export_structure>
The Grata export is an .xlsx with three tabs:

1. **Top Executive Contacts** — Primary contact list. Contains: name, title, email, phone, LinkedIn URL, company name.
2. **Other Executive Contacts** — Secondary contacts. Same structure. Often contains owners/presidents that should be in the top tab. Must be scanned.
3. **Companies** — Company-level data. Contains: company name, description, revenue estimate, employee count, year founded, headquarters location, industry tags, website URL.

Cross-reference contacts to companies by matching on company name.
</grata_export_structure>

<output_columns>
Final CSV columns in order. Color coding from Dino's template:

| # | Column | Color | Source | Formatting | Reply.io Variable |
|---|--------|-------|--------|------------|-------------------|
| 1 | email | — | Executive tab | As-is | Identifier |
| 2 | first_name | Green | Executive tab | Title case | {{first_name}} |
| 3 | last_name | Green | Executive tab | Title case | {{last_name}} |
| 4 | company_name | Green | Companies tab | As-is | {{company_name}} |
| 5 | title | — | Executive tab | As-is | — |
| 6 | industry | Green | User input (intake question) | All lowercase, no abbreviations unless standard | {{industry}} |
| 7 | business_model | Green | AI-generated from company description | All lowercase except acronyms. ~5 words. Specific enough for "acquiring a company in the {business_model} space" | {{business_model}} |
| 8 | year_founded | Green | Companies tab | 4-digit year | {{year_founded}} |
| 9 | city | Green | Companies tab → headquarters | Extracted from location string, title case | {{city}} |
| 10 | state | Green | Companies tab → headquarters | Extracted from location string. Full name or abbreviation per Dino's preference | {{state}} |
| 11 | linkedin_profile | Yellow | Executive tab | Full URL. If missing: `https://www.linkedin.com/in/denis-beslic-30bb6b25/` | Required for LinkedIn sequence steps |
| 12 | clearout_rating | Red | Clearout API | As returned | Not uploaded to Reply.io |
| 13 | zerobounce_rating | Red | ZeroBounce API | As returned | Not uploaded to Reply.io |

**Green columns** = messaging variables used in Reply.io sequence templates.
**Yellow** = required for LinkedIn automation steps (sequence stops if missing).
**Red** = email validation reference only — do not include in Reply.io upload, keep in master CSV.
</output_columns>

<role_filter>
**Include** (owner-operator titles):
- Owner, Co-Owner
- President, Co-President
- Founder, Co-Founder
- CEO, Chief Executive Officer
- Managing Partner, Managing Member
- Principal (if sole/primary)

**Exclude** (non-operator roles):
- CFO, CTO, COO, CIO, CISO, CMO
- VP, Vice President
- Director
- Manager
- Board Member, Advisor

When ambiguous (e.g., "Partner" without "Managing"), include but flag for user review in preview.
</role_filter>

<business_model_examples>
The `business_model` field should be specific to what the company actually does, not the broad industry. Examples from Dino's messaging:

| Company Description | Industry (broad) | Business Model (narrow) |
|---------------------|-------------------|------------------------|
| Provides fire inspection and code compliance services | fire safety | fire inspection and code compliance services |
| Develops DOT and OSHA compliance management software | fire safety | department of transportation and OSHA compliance software |
| Penetration testing and vulnerability assessment firm | cybersecurity | penetration testing and vulnerability assessment |
| Managed detection and response for mid-market | cybersecurity | managed detection and response services |
| Building inspection software for municipalities | fire safety | inspection management software |

Rules:
- All lowercase except acronyms (OSHA, DOT, IT)
- Must fit naturally in: "I was researching the {industry} sector, specifically companies in {business_model}"
- ~3-7 words. Specific enough to feel researched, not generic.
</business_model_examples>

<location_parsing>
Grata exports location as a single string (e.g., "Dallas, TX" or "New York, New York" or "Austin, Texas, United States").

Parsing rules:
- Split on comma
- City = first segment, trimmed
- State = second segment, trimmed
- Discard country if present (third segment)
- If state is abbreviated (TX), keep as-is
- If state is full name, keep as-is (match Dino's current format)
- Always use company headquarters location, never the executive's personal location
</location_parsing>
