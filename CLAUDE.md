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
| Clearout + ZeroBounce | Email validation (both required before outreach) |
| OneDrive | File storage — thesis docs, CSV outputs |
</stack>

<behaviors>
- Thesis-first. Load investment thesis docs before any scoring or ranking.
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
