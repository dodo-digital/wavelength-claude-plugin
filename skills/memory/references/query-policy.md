# Memory Query Policy

Use this reference when deciding whether to call `query_context`.

## Query First

Query memory before work where prior Wavelength context could materially change the answer:

- Deal analysis, investment memos, scorecards, red-team reviews, and diligence plans
- Company research when the target company, broker, founder, or industry is known
- Grata scoring, shortlist generation, thesis calibration, or exclusion-rule decisions
- Company processing when outreach rules, title edge cases, industry copy, or schema changes may recur
- Questions about Wavelength thesis, investment criteria, source locations, templates, or prior decisions
- Any request phrased as "what do we know about...", "have we seen...", "did we already...", or "use our memory..."

## Query Shape

Use the narrowest reliable query first:

1. Known exact item:
   ```json
   {"slug":"company-acme-security"}
   ```

2. Company, industry, person, source, topic, or skill:
   ```json
   {"tags":["industry/cybersecurity"]}
   {"tags":["company/acme-security"]}
   {"tags":["skill/grata-search-enrichment","topic/exclusions"]}
   ```

3. Fuzzy question or unknown tags:
   ```json
   {"keyword":"founder-owned dental IT"}
   ```

4. Filesystem/listing request:
   ```json
   {}
   ```

5. Audit or "what changed" request:
   ```json
   {"slug":"industry-fire-safety","include_history":true}
   ```

## Do Not Query By Default

Skip memory when it is unlikely to add value:

- Installing, removing, or debugging the plugin itself
- Checking MCP auth, credits, or endpoint health
- Running a single email validation or one-off API call
- Explaining generic syntax, commands, or local repo files
- Tasks where the user supplied all needed context and prior Wavelength context would not affect the output

If uncertain, make one narrow query. Do not keep searching memory repeatedly unless the first result proves relevant.

## Answering From Memory

- Cite memory docs by slug.
- Distinguish memory facts from fresh analysis.
- If memory is empty or stale, say so directly.
- If you discover an important gap, suggest what should be researched or saved.

Example:

> Based on `industry-cybersecurity` and `criteria-owner-operator-fit`, dedicated SOC providers are preferred, while general MSPs without managed detection are usually marked LOW.
