# Wavelength Equity — Deal Sourcing Plugin

Search fund acquiring bootstrapped services businesses ($2M–$70M revenue). This plugin automates sourcing, enrichment, outreach prep, and investment analysis.

<identity>
- **Fund:** Wavelength Equity — search fund, lower middle market
- **Thesis:** Bootstrapped, founder-owned services businesses with recurring revenue
- **Sectors:** Cybersecurity, fire safety, vertical software
- **Filters:** USA only, no prior investor funding, owner/operator near retirement preferred
- **Team:** Dino (principal), Giani, interns
</identity>

<stack>
| Tool | Role |
|------|------|
| Grata | Company sourcing (keyword + filters, batch exports 400–500) |
| HubSpot | CRM — ~500 fire safety cos already loaded, many untouched |
| Reply.io | Outreach sequences (10 touches: email + LinkedIn per contact) |
| Apollo | Contact enrichment |
| ProxyCurl | LinkedIn enrichment — owner age/tenure signals |
| Clearout + ZeroBounce | Email validation (both required) |
| OneDrive | File storage — thesis docs, CSV outputs |
</stack>

<workflows>
Skills to be built as `.claude/skills/` folders:

1. **Company List Processing** (`/company-processor`)
   - Input: Grata `.xlsx`/`.csv` (two tabs: Top Executive Contacts + Companies)
   - Scrub non-owner-operators (drop CFO, CTO, COO titles)
   - Cross-reference tabs by company name
   - Populate: industry (broad), business model (narrow, lowercase), city/state (from Companies tab), year founded, LinkedIn URL
   - Fallback LinkedIn: denis-beslic-30bb6b25
   - Email validation via Clearout + ZeroBounce
   - LinkedIn profile mandatory — sequence stops without it
   - Output: CSV → OneDrive + Reply.io upload

2. **Grata Search Enrichment** (`/enrich-grata`)
   - Input: 400–500 company Grata export
   - Per company: 5-word descriptor, fit rating (high/medium/low), force-rank batch
   - Rating criteria: business clarity, size, owner/operator situation
   - Thesis docs in OneDrive folder (live, editable — always re-read before scoring)
   - Output: Excel/CSV for HubSpot or Reply.io sync

3. **Investment Memo** (`/investment-memo`)
   - Input: CIM/SIM or owner-provided materials
   - Output: Wavelength standard format — factual description, scorecard analysis, value creation thesis, return thesis
   - Template + 2–3 past examples in shared Drive (load before generating)

4. **Meeting Prep** (`/meeting-prep`)
   - Auto-generate: company summary, exec background, talking points

5. **HubSpot Harvesting** — confirm fit, force-rank, plan second-pass outreach
6. **Conference Prep** — attendee lists, fit grades, force-rank
</workflows>

<context_files>
Thesis and reference docs stored in OneDrive. Always load before scoring or analysis:
- Investment thesis (general)
- Per-industry thesis docs (cybersecurity, fire safety, vertical software)
- Investment memo template + past examples
- Search criteria / Grata filter definitions
</context_files>

<outreach_variables>
Reply.io sequences require these fields per contact:
- `first_name`, `linkedin_url` (mandatory — skip contact if missing)
- `industry` (broad category), `business_model` (narrow, lowercase)
- `city`, `state` (from Companies tab, not Contacts)
- `year_founded`
</outreach_variables>

<behaviors>
- Use skills. Invoke existing skills before building ad hoc workflows.
- Thesis-first. Load investment thesis docs before any scoring or ranking.
- Validate emails. Never send contacts to Reply.io without Clearout + ZeroBounce.
- LinkedIn mandatory. Drop contacts without LinkedIn profiles from outreach lists.
- Parallel over sequential. Run independent tool calls concurrently.
- Never hardcode secrets. API keys from env vars or OS keychain only.
- Confirm before sending. Show outreach lists before uploading to Reply.io.
- Checkpoint multi-step work. Save intermediate outputs to OneDrive.
</behaviors>

<skills>
Skills in `.claude/skills/`. SKILL.md with YAML frontmatter + XML body.

| Skill | Purpose |
|-------|---------|
| `create-skills` | Create new skills with proper structure |
| `create-hooks` | Create event-driven hooks and guardrails |

Skill router hook auto-detects skill from prompt keywords. Add `<auto_trigger>` to any SKILL.md for automatic discovery.
</skills>

<guardrails>
**Forbidden:**
- Committing API keys, `.env` files, or credentials
- Uploading to Reply.io without showing the user the list first
- Scoring companies without loading current thesis docs
- Fabricating company data or fit ratings

**Constrained:**
- File deletion → confirm first
- CRM updates → validate payload, show diff before push
- Outreach lists → email validation required before Reply.io upload
</guardrails>
