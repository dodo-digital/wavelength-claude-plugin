# Data Sources — Where to Find What

## Grata
- **What:** Company sourcing platform. Keyword search, batch exports (400–500 companies per search).
- **Contains:** Company name, revenue estimates (unreliable), employee count, founding year, location, ownership type, industry tags, description.
- **Access:** Web app. Exports as XLSX/CSV.
- **Plugin skill:** `/grata-search-enrichment` (score exports), `/company-processor` (transform to contacts)

## HubSpot
- **What:** CRM. Existing pipeline, ~500 fire safety companies loaded.
- **Contains:** Contacts, companies, deals, pipeline stages, activity history, notes.
- **Key tables:** Contacts (name, email, phone, company, title), Companies (name, industry, revenue, employees), Deals (stage, value, close date, notes).
- **Access:** HubSpot API or web app. Claude connector available.

## Reply.io
- **What:** Outreach sequencing. 10 touches per contact (email + LinkedIn).
- **Contains:** Campaign lists, contact records, sequence templates, delivery stats.
- **Access:** Reply.io API. Plugin MCP has `search_reply_contacts`, `create_reply_contact`, `add_to_campaign` tools.

## Apollo
- **What:** Contact enrichment.
- **Contains:** Email addresses, phone numbers, job titles, company data, LinkedIn URLs.
- **Access:** Apollo API. Plugin MCP has `apollo_enrich_person`, `apollo_search_people` tools.

## OneDrive
- **What:** File storage. Thesis docs, CIMs, CSV outputs, company materials.
- **Folder structure:** (Update this as Dino organizes)
  - `/Deal Pipeline/` — Active deal materials, CIMs, SIMs
  - `/Research/` — Industry reports, market data
  - `/Exports/` — Grata exports, processed lists
- **Access:** Microsoft connector in Claude Code. Add via Settings > Connected Tools.

## Wavelength MCP Server
- **What:** Hosted tools for email validation, contact enrichment, Reply.io workflows, and shared memory.
- **Tools available:** `validate_email`, `zb_validate_email`, `bulk_validate`, `bulk_status`, `bulk_results`, `check_credits`, `apollo_enrich_person`, `apollo_bulk_enrich_people`, `apollo_enrich_org`, `apollo_search_people`, `reply_list_sequences`, `reply_search_contact`, `reply_push_contacts`, `query_context`, `update_context`, `save_skill_learning`, `get_skill_learnings`, plus admin tools.
- **Access:** Automatically connected via plugin MCP declaration. API keys are server-side.

## Shared Memory
- **What:** MCP-backed shared context for Wavelength deal work.
- **Contains:** Company notes, industry patterns, people notes, thesis updates, source references, criteria, templates, and reusable learnings.
- **Access:** `/memory` skill. List with `query_context {}`, search by `slug`, `tags`, or `keyword`, and save with `update_context`.
