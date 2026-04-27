---
name: company-processor
description: Process Grata exports into validated, enriched Reply.io-ready contact lists. Use when uploading company lists, processing Grata exports, preparing outreach contacts, or building Reply.io campaigns. Transforms xlsx exports, enriches with Apollo, validates emails via Clearout + ZeroBounce, generates messaging variables, and uploads to Reply.io.
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
  - "process list"
  - "contact list"

intent_patterns:
  - "process.*grata"
  - "upload.*reply"
  - "prepare.*contacts"
  - "build.*campaign"
  - "convert.*csv"
  - "process.*list"
  - "outreach.*prep"
</auto_trigger>

<objective>
Transform a raw Grata export (.xlsx) into a validated, enriched contact list ready for Reply.io upload. This skill replaces the manual intermediate worksheets between raw Grata export and Reply.io — all transformation happens programmatically. Merges company data with executive contacts from all tabs, filters to owner-operators only, generates messaging variables (industry, business_model, year_founded), validates emails via MCP tools (Clearout + ZeroBounce), enriches via Apollo, previews for approval, then saves output CSVs and uploads to Reply.io.

This skill is DOWNSTREAM of grata-search-enrichment — it takes the selected companies and prepares outreach. Grata-search-enrichment narrows; company-processor executes.
</objective>

<quick_start>
1. User drops a Grata export xlsx (or shortlist from grata-search-enrichment)
2. Skill discovers format, validates against known schema
3. Asks target industry + Reply.io sequence
4. Extracts contacts, filters owner-operators, merges company data
5. Generates messaging variables (business_model via Claude, rest mechanical)
6. Validates emails via MCP (Clearout + ZeroBounce)
7. Enriches sparse contacts via Apollo
8. Previews first 5 rows for approval
9. Saves master CSV + Reply.io upload CSV, uploads to Reply.io
</quick_start>

<essential_principles>
- **Claude judges, Python transforms.** Python scripts handle I/O: read xlsx → JSON, write JSON → CSV. Claude generates business_model descriptors and makes quality judgment calls. NEVER write a Python script with business logic or descriptor generation. Python moves data; Claude understands it.
- **Run to completion.** This skill does NOT stop until output files exist on disk and (if Reply.io is available) contacts are uploaded. AskUserQuestion is a checkpoint within the flow, not an exit. After the user answers, keep going.
- **AskUserQuestion or nothing.** Every question MUST use the AskUserQuestion tool. Never ask questions as plain text. If you have nothing worth asking, proceed.
- **Owner-operators only.** Scrub anyone who is not clearly an owner, president, founder, or CEO. No CFO, CTO, COO, VP, director. See role filter in field-mappings.md.
- **Both exec tabs.** Pull contacts from BOTH "Top Executive Contacts" AND "Other Executive Contacts" — Grata mislabels roles across tabs. Merge, then deduplicate by email (keep more senior title).
- **Company location, not executive.** City and state come from the Companies tab headquarters field. Never use the executive's personal location.
- **LinkedIn mandatory.** Every contact must have a LinkedIn URL. If missing, use fallback: `https://www.linkedin.com/in/denis-beslic-30bb6b25/`
- **Validate before send.** Never upload to Reply.io without showing preview and getting explicit user approval.
- **Self-healing schema.** Never hardcode column positions. Discover structure each run, compare to known schema in `references/processing-rules.md`, adapt and update if changed.
- **Learnings persist via MCP.** At the start of every run, call `get_skill_learnings` with `skill="company-processor"` to load shared learnings from the server. After each run, call `save_skill_learning` for any new insights. Learnings are shared automatically across all users — no local file edits needed.
- **Case rules.** Industry is broad and lowercase ("fire safety"). Business model is narrow, specific, and lowercase except acronyms ("OSHA compliance management software").
- **Deduplicate.** After merging both exec tabs, deduplicate by email. Same person in both tabs → keep entry with more senior title.
- **No HubSpot.** Grata syncs directly to HubSpot via its own integration. This skill handles Reply.io only.
- **Tables for everything.** All previews and summaries MUST be markdown tables. NEVER output numbered lists or card-style blocks.
- **Plain English questions.** The user is a non-technical search fund operator. Never use jargon. Say what you mean simply.
- **MCP-first for validation.** Always use Wavelength MCP tools for email validation and Apollo enrichment. They have the API keys server-side. Only fall back to scripts if MCP is unavailable.
</essential_principles>

<process>
1. **Discover and validate schema** [LOW freedom]
   Run `scripts/discover_export.py` on the uploaded file.
   Read `references/processing-rules.md` — check the `## Known Schema` section.
   - **Match → proceed silently.** Do not report column counts or structure.
   - **Minor mismatch** (renamed column, new column) → one sentence: "Schema changed: {what}. Updated processing-rules.md." Then proceed.
   - **Unrecognizable** → stop, ask user to confirm tab/column mapping.

2. **Intake and load learnings** [LOW freedom]
   Load learnings from MCP: call `get_skill_learnings` with `skill="company-processor"` and the target industry (once known).
   Load `references/processing-rules.md` for static rules (role filter, location parsing, business model rules).
   Load `references/field-mappings.md` for output column specs.

   Use AskUserQuestion to ask:
   - Target industry (e.g., "fire safety", "cybersecurity") — this becomes the batch-constant `industry` field
   - Which Reply.io sequence? Query `reply_list_sequences` via MCP, show active sequences, let user pick
   - If MCP learnings exist for this industry, surface them as options to confirm or skip

   After answers, proceed immediately.

3. **Extract contacts to JSON** [MEDIUM freedom]
   Run `scripts/extract_contacts.py` on the xlsx with the target industry as an argument.

   The script:
   - Reads all three tabs (Companies, Top Executive Contacts, Other Executive Contacts)
   - Filters to owner-operators only (Owner, President, Founder, CEO, Managing Partner, Principal)
   - Cross-references contacts to Companies tab by company name
   - Extracts city/state from Companies tab headquarters field (NOT exec location)
   - Populates LinkedIn (exec tab value, or fallback URL)
   - Outputs JSON array to `/tmp/company_processor_extracted.json`

   Claude then reads the JSON and generates `business_model` for each contact:
   - Read each company's description
   - Write a ~5 word lowercase descriptor (except acronyms)
   - Must fit: "I was researching the {industry} sector, specifically companies in {business_model}"
   - Save enriched JSON back to `/tmp/company_processor_enriched.json`

   **Do NOT write a Python script to generate business_model. That is Claude's judgment work.**

4. **Validate emails via MCP** [LOW freedom]
   Check credits first: call `check_credits` via MCP.

   For batches ≤ 20 emails:
   - Use `validate_email` (Clearout) for each batch
   - Use `zb_validate_email` (ZeroBounce) for each batch

   For batches > 20 emails:
   - Use `bulk_validate` with provider="clearout", then poll `bulk_status`, then `bulk_results`
   - Use `bulk_validate` with provider="zerobounce", then poll `bulk_status`, then `bulk_results`

   Map results to `clearout_rating` and `zerobounce_rating` fields on each contact.

   **If MCP unavailable:** Warn user, skip validation, flag all emails as "unvalidated."

5. **Apollo enrichment (if needed)** [MEDIUM freedom]
   For contacts missing email or with sparse data:
   - Use `apollo_enrich_person` (single) or `apollo_bulk_enrich_people` (up to 10 at a time)
   - Fill in missing fields: email, LinkedIn, title confirmation

   For companies where business_model descriptor is uncertain:
   - Use `apollo_enrich_org` to get richer company details
   - Revise descriptor with better data

   Skip this step entirely if all contacts have email + LinkedIn + sufficient company data.

6. **Build output** [LOW freedom]
   Run `scripts/format_output.py` with the enriched JSON.

   Produces TWO files:
   - **Master CSV** (all columns): email, first_name, last_name, company_name, title, industry, business_model, year_founded, city, state, linkedin_profile, clearout_rating, zerobounce_rating
   - **Reply.io upload CSV** (green + yellow only): email, first_name, last_name, company_name, title, industry, business_model, year_founded, city, state, linkedin_profile

   Red columns (clearout_rating, zerobounce_rating) excluded from Reply.io file.

7. **Preview and approve** [LOW freedom]
   Show the user a summary:

   | Metric | Value |
   |--------|-------|
   | Total contacts extracted | {n} |
   | Owner-operators kept | {n} |
   | Dropped (non-operator) | {n} |
   | Emails validated | {n} |
   | Invalid emails flagged | {n} |
   | Missing LinkedIn (fallback used) | {n} |

   Then first 5 rows as a table:

   | # | Name | Company | Title | Industry | Business Model | City | State | Email Valid? |
   |---|------|---------|-------|----------|----------------|------|-------|-------------|

   Wait for explicit approval. AskUserQuestion with "Approve upload" / "Edit first" / "Save locally only" options.

8. **Upload to Reply.io** [LOW freedom]
   On approval:
   - Use `reply_push_contacts` via MCP to add contacts to the selected sequence
   - Batch in groups of 50 (API limit is 500 but be conservative)
   - Report results: added count, error count, any failures

   Save both CSVs locally regardless.

   **If Reply.io API fails or is not configured:** Save CSVs, instruct user to import via Reply.io > People > Import.

9. **Update learnings** [LOW freedom]
   After each run, save new learnings via MCP using `save_skill_learning` with `skill="company-processor"`:
   - Schema changes → category: `schema-change`
   - Title edge cases (new titles that needed judgment) → category: `edge-case`
   - Business model patterns that worked well → category: `pattern`
   - Data quality issues → category: `adjustment`
   - Calibration insights from user feedback → category: `adjustment`

   Each learning should be a single actionable statement. Save one learning per call — don't batch multiple insights into one entry. These are shared across all users automatically.
</process>

<not_yet_available>
- **OneDrive integration** — output files saved locally until OneDrive API configured.
- **HubSpot deduplication** — cannot yet cross-reference against existing HubSpot pipeline to exclude already-contacted companies.
- **Per-industry thesis documents** — Dino has not yet shared these. Using general criteria.
</not_yet_available>

<success_criteria>
- [ ] Schema discovery runs without hardcoded assumptions
- [ ] Contacts pulled from BOTH executive tabs, not just one
- [ ] Non-owner-operators scrubbed (no CFO, CTO, COO, VP)
- [ ] City/state from company location, not executive
- [ ] LinkedIn populated for every row (fallback used if needed)
- [ ] Industry is broad and lowercase; business model is narrow and specific
- [ ] Business model generated by Claude, not a script
- [ ] Email validation run via MCP (or skipped with warning)
- [ ] Preview shown and user approved before upload
- [ ] Master CSV + Reply.io CSV generated on disk
- [ ] Contacts uploaded to Reply.io (or manual instructions given)
- [ ] New learnings saved to MCP via save_skill_learning
- [ ] Skill ran to completion — files exist on disk when done
</success_criteria>
