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

| Position | Header | Type | Example | Variants |
|----------|--------|------|---------|----------|
| 0 | Company Name | text | "Acme Fire Services" | |
| 1 | Website | url | "acmefire.com" | |
| 2 | Description | text | "Provides fire inspection..." | "Company Description" |
| 3 | Revenue Estimate | text | "$5M - $10M" | "Revenue", "Revenue Range" |
| 4 | Employees | number | "45" | "Employee Count", "# Employees" |
| 5 | Year Founded | number | "1998" | "Founded" |
| 6 | Headquarters | text | "Dallas, TX" | "HQ", "Location" |
| 7 | Industry | text | "Fire Safety" | "Industry Tags", "Sector" |
| 8 | Ownership Type | text | "Private" | "Ownership" |

**Notes:** Columns beyond position 8 vary by search. Common extras: Funding Status, Last Funding Date, Similar Companies, Grata Score.

### Tab 2: Top Executive Contacts

| Position | Header | Type | Example | Variants |
|----------|--------|------|---------|----------|
| 0 | Company Name | text | "Acme Fire Services" | |
| 1 | First Name | text | "John" | |
| 2 | Last Name | text | "Smith" | |
| 3 | Title | text | "President & Owner" | "Job Title" |
| 4 | Email | email | "john@acmefire.com" | "Work Email" |
| 5 | Phone | phone | "(214) 555-1234" | "Work Phone" |
| 6 | LinkedIn URL | url | "linkedin.com/in/..." | "LinkedIn", "LinkedIn Profile" |

### Tab 3: Other Executive Contacts

Same structure as Tab 2. Contains additional executives — often includes owner-operators that Grata classified as non-primary.

**Known variant names:** "Other Executives", "Additional Contacts", "Other Executive Contacts"

## Column Mapping Rules

When discovering a new export:
1. Match tabs by content pattern (company-level data vs. contact-level data), not just name
2. Match columns by position first, then confirm with sample values
3. If a column moved position but header and data match → update position in this file
4. If an entirely new column appears → add to the table with `added: YYYY-MM-DD`

## Change History

| Date | Change | Action Taken |
|------|--------|--------------|
| (initial) | Schema documented from known exports | Baseline established |
