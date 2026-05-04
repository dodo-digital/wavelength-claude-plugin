# Wavelength Equity — Deal Sourcing Plugin

Search fund acquiring bootstrapped services businesses. This plugin automates sourcing, enrichment, outreach prep, and investment analysis.

<identity>
- **Fund:** Wavelength Equity — search fund, lower middle market
- **Thesis:** Bootstrapped, founder-owned services businesses with recurring revenue
- **Sectors:** Cybersecurity, fire safety, vertical software
- **Filters:** USA only, no prior investor funding, owner/operator near retirement preferred
- **Revenue:** $2M–$70M (Grata estimates, acknowledged unreliable)
- **Team:** Dino (principal), Giani, interns
</identity>

<stack>
| Tool | Role |
|------|------|
| Grata | Company sourcing — keyword search, batch exports (400–500) |
| HubSpot | CRM — existing pipeline, ~500 fire safety cos loaded |
| Reply.io | Outreach sequences — 10 touches per contact (email + LinkedIn) |
| Apollo | Contact enrichment |
| ProxyCurl | LinkedIn enrichment — owner age/tenure signals |
| Wavelength MCP | Hosted email validation (Clearout + ZeroBounce). Tools: validate_email, zb_validate_email, bulk_validate, bulk_status, bulk_results, check_credits. API keys server-side, no local keys needed. |
| OneDrive | File storage — thesis docs, CSV outputs |
</stack>

<brain>
Persistent knowledge base. Injected at session start by the SessionStart hook.

- **Thesis:** `context/thesis.md` — what we're looking for. Load before scoring or ranking.
- **Sources:** `context/sources.md` — where data lives across tools (HubSpot, OneDrive, Grata, etc.).
- **Portfolio:** `{brain_dir}/portfolio/` — company research files, one per company. Accumulated over sessions.
- **Learnings:** `{brain_dir}/learnings/` — cross-deal insights and patterns.
- **Thesis notes:** `{brain_dir}/thesis-notes.md` — Dino's refinements to the canonical thesis.

The brain directory path is injected at session start. After analyzing a company, ask if the user wants to save findings to the brain.
</brain>

<behaviors>
- Thesis-first. Load `context/thesis.md` before any scoring or ranking.
- Brain-aware. Check portfolio for prior research before analyzing a company. Save findings after analysis.
- Validate before send. Never push contacts to Reply.io without email validation and user confirmation.
- LinkedIn mandatory. Drop contacts without LinkedIn profiles from outreach lists.
- Parallel over sequential. Run independent tool calls concurrently.
- Never hardcode secrets. API keys from env vars or OS keychain only.
- Checkpoint multi-step work. Save intermediate outputs to OneDrive.
</behaviors>

<guardrails>
**Forbidden:**
- Committing API keys, `.env` files, or credentials
- Uploading to Reply.io without showing the list first
- Scoring companies without loading current thesis docs
- Fabricating company data or fit ratings

**Constrained:**
- File deletion → confirm first
- CRM updates → show diff before push
- Outreach lists → email validation required before upload
</guardrails>
