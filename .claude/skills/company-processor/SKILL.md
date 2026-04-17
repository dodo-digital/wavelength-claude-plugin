---
name: company-processor
description: Process Grata exports into Reply.io-ready contact lists. Use when uploading company lists, processing Grata exports, preparing outreach contacts, or building Reply.io campaigns. Transforms xlsx/csv exports, enriches fields, validates emails, and uploads to Reply.io.
context_budget:
  skill_md: 150
---

<auto_trigger>
keywords:
  - "company list"
  - "company processor"
  - "grata export"
  - "reply.io"
  - "reply io"
  - "upload contacts"
  - "process contacts"
  - "outreach list"
  - "campaign list"

intent_patterns:
  - "process.*grata"
  - "upload.*reply"
  - "prepare.*contacts"
  - "build.*campaign"
  - "convert.*csv"
  - "process.*list"
</auto_trigger>

<objective>
Transform a raw Grata export (.xlsx/.csv) into a validated, enriched contact list ready for Reply.io upload. Merges company data with executive contacts, filters to owner-operators only, validates emails, generates messaging variables, previews for approval, then saves to OneDrive and uploads to Reply.io.
</objective>

<quick_start>
1. User drops a Grata export file (.xlsx or .csv)
2. Skill asks clarifying questions (target industry, Reply.io sequence)
3. Processes, previews first 5 rows, waits for approval
4. Saves CSV to OneDrive + uploads to Reply.io
</quick_start>

<essential_principles>
- **Owner-operators only.** Scrub anyone who is not clearly an owner, president, or founder. No CFO, CTO, COO.
- **Both tabs.** Pull contacts from BOTH "Top Executive Contacts" AND "Other Executive Contacts" — Grata mislabels roles across tabs.
- **Company location, not executive.** City and state come from the Companies tab, never the executive's personal location.
- **LinkedIn mandatory.** Every contact must have a LinkedIn URL. If missing, use fallback: `https://www.linkedin.com/in/denis-beslic-30bb6b25/`
- **Validate before send.** Never upload to Reply.io without showing preview and getting explicit user approval.
- **Case rules.** Industry and business model are all lowercase, except acronyms (e.g., "OSHA compliance software"). Industry is broad ("fire safety"), business model is narrow and specific to the company.
</essential_principles>

<process>
1. **Intake** [LOW freedom]
   Read the uploaded file. Identify the tabs (Top Executive Contacts, Other Executive Contacts, Companies).
   Ask the user:
   - What is the target industry for this search? (unless obvious from the data)
   - Which Reply.io sequence should this be uploaded to? (query Reply.io for active sequences, show list, let user pick or use default)

2. **Extract and merge** [MEDIUM freedom]
   Read `references/field-mappings.md` for column specs.
   - Pull contacts from both executive tabs
   - Filter to owner-operators only (owner, president, founder, CEO, managing partner — reject CFO, CTO, COO, VP, director)
   - Cross-reference each contact to the Companies tab by company name
   - Extract city and state as separate variables from the Companies tab location field

3. **Generate messaging variables** [MEDIUM freedom]
   For each contact:
   - `industry` — use the target industry from intake (broad, lowercase, sentence-friendly)
   - `business_model` — read company description, generate a narrow ~5-word descriptor (lowercase except acronyms). Must sound specific enough for "I'm interested in acquiring a company in the {business_model} space"
   - `year_founded` — from Companies tab (NOT tenure)
   - Populate LinkedIn from export; if missing, use fallback URL

4. **Validate emails** [LOW freedom]
   <!-- STATUS: NOT YET IMPLEMENTED — need Clearout and ZeroBounce API access -->
   Run each email through Clearout AND ZeroBounce validation.
   Add validation rating columns (red columns — not uploaded to Reply.io but kept in CSV).
   Flag invalid emails in preview.
   **If API access is not yet configured:** Skip validation, warn the user that emails are unvalidated, and note which services are needed.

5. **Build output CSV** [LOW freedom]
   Assemble final CSV matching the Reply.io upload template. See `references/field-mappings.md` for exact column order and formatting.
   Columns: email, first_name, last_name, company_name, title, industry, business_model, year_founded, city, state, linkedin_profile, clearout_rating, zerobounce_rating

6. **Preview and approve** [LOW freedom]
   Show the user a formatted table of the first 5 rows.
   Report: total contacts, contacts dropped (with reasons), any missing fields.
   Wait for explicit "approve" or "looks good" before proceeding.

7. **Save and upload** [LOW freedom]
   <!-- STATUS: Reply.io API integration NOT YET TESTED — may require manual upload fallback -->
   - Save CSV to OneDrive (ask user for folder path if not configured)
   - Upload contact list to the selected Reply.io sequence
   - **If Reply.io API is not yet configured:** Save CSV locally, instruct user to manually import via Reply.io > People > Import
   - Report: file saved location, contacts uploaded count, any errors
</process>

<not_yet_available>
The following components are not yet configured. When you encounter them, tell the user "I do not yet have access to {component}" and ask them to provide it. Once received, update this skill file.

- **Clearout API access** — needed for email validation (step 4)
- **ZeroBounce API access** — needed for email validation (step 4)
- **Reply.io API access** — needed for direct upload (step 7). Until confirmed, offer manual CSV upload as fallback.
- **OneDrive API access** — needed for file storage (step 7). Until confirmed, save files locally.
- **Reply.io upload template** — the exact .csv column structure for Reply.io import. A sample has been reverse-engineered from call notes, but the actual template file should be uploaded to confirm column order.
</not_yet_available>

<success_criteria>
- [ ] Contacts pulled from both executive tabs, not just one
- [ ] Non-owner-operators scrubbed (no CFO, CTO, COO)
- [ ] City/state from company location, not executive
- [ ] LinkedIn populated for every row (fallback used if needed)
- [ ] Industry is broad and lowercase; business model is narrow and specific
- [ ] Email validation run (or skipped with warning if APIs unavailable)
- [ ] Preview shown and user approved before upload
- [ ] CSV saved to OneDrive (or locally if unavailable)
- [ ] Contacts uploaded to Reply.io (or manual instructions given)
</success_criteria>
