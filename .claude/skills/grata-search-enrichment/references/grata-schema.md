# Grata Export Schema — Living Knowledge File

This file documents the known structure of Grata search exports. Claude reads this during processing and **updates it** when the format changes. Do not edit manually unless correcting an error.

## Self-Healing Rules

1. **Tab renamed but structure matches** → add name variant, update primary name
2. **Column header renamed but position/data matches** → add header variant
3. **New column appears** → document it with position, type, samples
4. **Column removed** → mark `removed: YYYY-MM-DD`, keep for reference
5. **Always confirm identity using sample values**, not just header text

## Known Tab Structure

### Tab 1: Companies

**Core columns (used for scoring):**

| Position | Header | Type | Example | Variants |
|----------|--------|------|---------|----------|
| 0 | Grata Link | url | "https://search.grata.com/search?c=TBUHTFX4" | added: 2026-04-20 |
| 1 | Company Id | text | "TBUHTFX4" | added: 2026-04-20 |
| 2 | Domain | url | "systemsengineering.com" | Previously "Website" |
| 3 | Name | text | "Systems Engineering" | Previously "Company Name" |
| 4 | Description | text | "Systems Engineering provides managed IT..." | |
| 5 | LinkedIn | url | "linkedin.com/company/systemsengineering-/" | added: 2026-04-20 |
| 6 | Revenue Estimate | number | "33000000" | Now raw integer, was range string ("$5M - $10M") |
| 7 | Employee Estimate | number | "210" | Previously "Employees" |
| 8 | Employees on Professional Networks | number | "210" | added: 2026-04-20 |
| 9 | Employee Growth (Monthly) | percentage | "2.19%" | added: 2026-04-20 |
| 10 | Employee Growth (Quarterly) | percentage | "9.27%" | added: 2026-04-20 |
| 11 | Employee Growth (6 months) | percentage | "12.77%" | added: 2026-04-20 |
| 12 | Employee Growth (Annual) | percentage | "47.83%" | added: 2026-04-20 |
| 13 | Total Review Count | number | "24" | added: 2026-04-20 |
| 14 | Aggregate Rating | number | "5" | added: 2026-04-20 |
| 15 | Headquarters | text | "Portland, ME" | |
| 16 | Mailing Address | text | "120 Exchange Street, Portland, ME 04101, USA" | added: 2026-04-20 |
| 17 | Year Founded | number | "1988" | |
| 18 | Ownership | text | "Bootstrapped" | Previously "Ownership Type" (was "Private") |
| 19 | Owner | text | (often empty) | added: 2026-04-20 |
| 20 | Investors | text | (often empty) | added: 2026-04-20 |
| 21 | Ultimate Owner | text | (often empty) | added: 2026-04-20 |
| 22 | Funding Stage | text | "No Funding" | added: 2026-04-20 |
| 23 | Last Funding Amount | number | (often empty) | added: 2026-04-20 |
| 24 | Last Funding Date | date | (often empty) | added: 2026-04-20 |
| 25 | Total Funding Amount | number | (often empty) | added: 2026-04-20 |
| 26 | Total Funding Rounds | number | "0" | added: 2026-04-20 |
| 27 | Business Model | text | "Services" | added: 2026-04-20 |
| 28 | NAICS 2 | text | "54 Professional, Scientific, and Technical Services" | added: 2026-04-20 |
| 29 | NAICS 3 | text | "541 Professional, Scientific, and Technical Services" | added: 2026-04-20 |
| 30 | NAICS 4 | text | "5415 Computer Systems Design and Related Services" | added: 2026-04-20 |
| 31 | NAICS 5 | text | "54151 Computer Systems Design and Related Services" | added: 2026-04-20 |
| 32 | NAICS 6 | text | "541519 Other Computer Related Services" | added: 2026-04-20 |
| 33 | Grata Industries | text | (often empty) | added: 2026-04-20 |
| 34 | Primary Email | email | "info@systemsengineering.com" | added: 2026-04-20 |
| 35 | Primary Phone | phone | "1-207-772-3199" | added: 2026-04-20 |
| 36 | Notes | text | "Priority: High ($33M revenue). Systems Engineering provides..." | added: 2026-04-20, contains pre-written priority notes |
| 37 | Executive First Name | text | "Matt" | added: 2026-04-20, inline exec data |
| 38 | Executive Last Name | text | "McGrath" | added: 2026-04-20 |
| 39 | Executive Title | text | "President & CEO" | added: 2026-04-20 |
| 40 | Executive Email | email | "mmcgrath@syseng.com" | added: 2026-04-20 |
| 41 | Executive Email Deliverability | text | "Deliverable" | added: 2026-04-20 |
| 42 | Executive Linkedin | url | "linkedin.com/in/matt-mcgrath-42a77723/" | added: 2026-04-20 |
| 43 | Key People | text | "Matt McGrath (President & CEO), Eric Tennyson (CFO)" | added: 2026-04-20 |
| 44 | Status | text | (often empty) | added: 2026-04-20 |
| 45 | Priority | text | "High" | added: 2026-04-20 |
| 46 | Channel | text | (often empty) | added: 2026-04-20 |

**Key format changes (2026-04-20):**
- Revenue Estimate changed from range string ("$5M - $10M") to raw integer (33000000)
- Industry column removed, replaced by NAICS codes (positions 28-32) and Grata Industries (33)
- Ownership values changed from "Private" to "Bootstrapped"
- Executive contact info now embedded inline (positions 37-42) in addition to separate tabs
- Notes column contains pre-written priority assessments
- Priority column contains High/Medium/Low pre-ratings

### Tab 2: Top Executive Contacts

| Position | Header | Type | Example | Variants |
|----------|--------|------|---------|----------|
| 0 | Name | text | "Guru Moorthi" | Full name, previously was Company Name |
| 1 | First Name | text | "Guru" | |
| 2 | Last Name | text | "Moorthi" | |
| 3 | Company | text | "Cloud Tech Services, Inc." | Previously "Company Name" |
| 4 | Company Website | url | "cloudtechservices.com" | added: 2026-04-20 |
| 5 | Company Id | text | "7PNMAPH4" | added: 2026-04-20 |
| 6 | Grata Link | url | "https://search.grata.com/search?c=7PNMAPH4" | added: 2026-04-20 |
| 7 | Title | text | "Founder" | Previously at position 3 |
| 8 | Work Email | email | "gmoorthi@cloudtechservices.com" | Previously "Email" |
| 9 | Work Email Verification | text | "Deliverable" | added: 2026-04-20 |
| 10 | Personal Email | email | "guru.v.moorthi@gmail.com" | added: 2026-04-20 |
| 11 | Location | text | "Irving, Texas, United States" | added: 2026-04-20, exec's personal location |
| 12 | City | text | "Ashburn" | added: 2026-04-20 |
| 13 | Region | text | "Virginia" | added: 2026-04-20 |
| 14 | Region Code | text | "VA" | added: 2026-04-20 |
| 15 | Country | text | "USA" | added: 2026-04-20 |
| 16 | LinkedIn | url | "linkedin.com/in/gmoorthi" | Previously "LinkedIn URL" at position 6 |
| 17 | Crunchbase | url | (often empty) | added: 2026-04-20 |
| 18 | Twitter | url | (often empty) | added: 2026-04-20 |
| 19 | Age | number | "59" | added: 2026-04-20 |
| 20 | Is Executive | text | "Yes" | added: 2026-04-20 |

**Note:** Phone column removed from exec tabs. Age column is a strong retirement signal.

### Tab 3: Other Executive Contacts

Same structure as Tab 2. Contains additional executives — often includes owner-operators that Grata classified as non-primary.

**Known variant names:** "Other Executives", "Additional Contacts", "Other Executive Contacts"

## Column Mapping Rules

When discovering a new export:
1. Match tabs by content pattern (company-level data vs. contact-level data), not just name
2. Match columns by position first, then confirm with sample values
3. If a column moved position but header and data match → update position in this file
4. If an entirely new column appears → add to the table with `added: YYYY-MM-DD`

## Revenue Parsing

Revenue Estimate format varies across exports:
- **Range string format:** "$5M - $10M" — parse midpoint or use lower bound
- **Raw integer format:** "33000000" — divide by 1,000,000 for millions
- Always confirm format from sample values before parsing

## Change History

| Date | Change | Action Taken |
|------|--------|--------------|
| (initial) | Schema documented from known exports | Baseline established |
| 2026-04-20 | Major restructure: 47 columns (was 9+), revenue now integer, NAICS codes replace Industry, inline exec data, Priority/Notes columns, Age column on exec tabs | Full schema rewrite |
