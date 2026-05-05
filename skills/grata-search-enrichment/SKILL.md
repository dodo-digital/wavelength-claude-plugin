---
name: grata-search-enrichment
description: Score and rank Grata search exports against Wavelength's investment thesis. Use when enriching company lists, prioritizing search results, or building shortlists from Grata exports. Generates descriptors, rates fit, force-ranks, and outputs a prioritized shortlist.
context_budget:
  skill_md: 150
---

<auto_trigger>
keywords:
  - "grata search"
  - "search enrichment"
  - "score companies"
  - "rank companies"
  - "company shortlist"
  - "prioritize list"
  - "thesis fit"
  - "grata enrichment"

intent_patterns:
  - "score.*grata"
  - "rank.*companies"
  - "enrich.*export"
  - "prioritize.*list"
  - "shortlist.*grata"
  - "rate.*fit"
</auto_trigger>

<objective>
Take a raw Grata search export (400-500 companies), score each company against the investment thesis, generate descriptors, rate fit (HIGH/MEDIUM/LOW), force-rank within tiers, and output a prioritized shortlist. Replaces manual ChatGPT batch processing.

This skill is UPSTREAM of company-processor — it narrows the list. Company-processor then prepares outreach for the selected companies.
</objective>

<quick_start>
1. User drops a Grata export xlsx
2. Skill discovers format, validates against known schema
3. Asks target industry + any extra exclusions
4. Scores in batches of 30-50, generates descriptors and ratings
5. Force-ranks, previews top results, generates output files
</quick_start>

<essential_principles>
- **Claude scores, Python does I/O.** Python scripts ONLY read xlsx → JSON and write JSON → xlsx/csv. ALL scoring, descriptor generation, fit rating, and rationale writing is done by Claude reading the data and using its judgment. NEVER write a Python script with scoring logic, keyword matching, or business rules. That defeats the entire purpose of this skill.
- **Run to completion.** This skill does NOT stop until output files exist on disk. Asking a question via AskUserQuestion is a checkpoint within the flow, not an exit. After the user answers, keep going. Never print a question as plain text and wait — that halts execution.
- **AskUserQuestion or nothing.** Every question to the user MUST use the AskUserQuestion tool. Never ask questions as plain text. If you have nothing worth asking, don't ask — just proceed.
- **Smart questions only.** Ask when there's a real judgment call: edge cases from the data, conflicting signals, threshold decisions. Do NOT ask when you have no basis for the question or when the answer is already in scoring-criteria.md.
- **Exclusions from learnings, not data peeking.** If prior calibration (Learned Adjustments) includes exclusions for this industry, suggest those. If nothing exists yet, just offer "None" and free-text. Never infer exclusion options by reading ahead into the data.
- **Self-healing schema.** Never hardcode column positions. Discover structure each run, compare to `references/grata-schema.md`, adapt and update if changed.
- **Thesis-first.** Load `references/scoring-criteria.md` before scoring. Every rating must reference specific thesis criteria.
- **Calibrate before grinding.** Always score 10 companies first, ask targeted questions, record learnings, THEN process the rest. Never skip calibration.
- **Learnings persist via MCP.** At the start of every run, call `get_skill_learnings` with `skill="grata-search-enrichment"` to load shared learnings from the server. Also read `## Learned Adjustments` in scoring-criteria.md for legacy local learnings. After calibration, save new insights via `save_skill_learning` — they propagate to all users automatically.
- **Memory for durable context.** Use `query_context` to check shared memory for target-industry criteria, exclusions, and prior category patterns before scoring. Use `save_skill_learning` for narrow skill adjustments. Use `/memory` or `update_context` for broader reusable context such as industry theses, shortlist rationale, exclusion frameworks, or notable company findings.
- **No fabrication.** If company data is insufficient for confident rating, mark MEDIUM with rationale noting uncertainty. Never invent details.
- **Batch processing.** Process 30-50 companies per scoring pass. Accumulate results. Do not attempt all 400+ in a single prompt.
- **Descriptors are specific.** Must fit "They do {descriptor}" and distinguish from peers. See anti-patterns in scoring-criteria.md.
- **Always generate files.** The job is not done until xlsx + csv output files exist on disk. Chat display is preview only.
- **Tables for everything. No exceptions.** All previews, calibration batches, and summaries MUST be markdown tables. NEVER output numbered free-text lists, card-style blocks, or separator lines between entries. If showing companies, it is a table. Period. Example: `| # | Company | Revenue | Founded | Descriptor | Fit | Key Signal |`
- **Plain English questions.** The user is a non-technical search fund operator. Never use jargon (TLD, NAICS, domain extension). Say what you mean simply: "Two companies list US addresses but their websites are .ae (UAE) and .ma (Morocco) — should I treat them as US companies or not?" Frame every question so the answer is obvious from the phrasing.
</essential_principles>

<process>
1. **Discover and validate schema** [LOW freedom]
   Run `scripts/discover_export.py` on the uploaded file.
   Read `references/grata-schema.md`. Compare silently.
   - **Match → say nothing, proceed immediately to step 2.** Do not report column counts, tab names, or structure details.
   - **Minor mismatch** (renamed column, new column, removed column) → one sentence: "Schema changed: {what changed}. Updated grata-schema.md." Then proceed.
   - **Unrecognizable** → stop, ask user to confirm column mapping.

2. **Intake and load learnings** [LOW freedom]
   Load shared learnings from MCP: call `get_skill_learnings` with `skill="grata-search-enrichment"` and the target industry (once known).
   Query shared memory with `query_context` for the target industry and relevant criteria/exclusion tags once the industry is known.
   Also load `references/scoring-criteria.md` for static thesis criteria and legacy local learnings.

   Use AskUserQuestion to ask:
   - Target industry (e.g., "fire safety", "cybersecurity")
   - If MCP or local learnings exist for this industry and include exclusions or rules worth confirming, offer those as suggested options (e.g., "Apply prior rule: MSPs without dedicated SOC = LOW"). This is useful — it reminds the user what was learned before.
   - If NO learned adjustments exist for this industry, just offer "None" + free-text for exclusions. Do not guess.

   After answers, proceed immediately.

3. **Show plan and proceed** [LOW freedom]
   Show a short execution plan table, then **immediately start extraction.** Do NOT ask "Ready to proceed?" or wait for confirmation. The plan is informational — the user can interrupt if they want to adjust.

   ```
   | Step | What | Est. |
   |------|------|------|
   | Extract | {n} companies + owner signals | ~30s |
   | Calibrate | Score first 10, ask 3-5 questions | ~3 min |
   | Score | Remaining {n-10} in batches of 40 | ~10 min |
   | Rank + Output | Force-rank, generate xlsx + csv | ~2 min |
   ```

   Then immediately proceed to step 4. No gate.

4. **Extract company data to JSON** [MEDIUM freedom]
   Use Python ONLY to extract raw data from the xlsx into a JSON file. No scoring, no filtering, no keyword matching. Python reads cells and writes JSON.

   Extract per company:
   - name, description, revenue, employees, founded, HQ, industry, website, ownership_type
   - Owner signals from exec tabs: titles containing Owner/Founder/President/CEO, exec names, exec count

   Save to `/tmp/grata_extracted.json` as an array of objects. This is what Claude reads next.

5. **Calibration batch — Claude reads and scores** [LOW freedom]
   Read the first 10 companies from `/tmp/grata_extracted.json` using the Read tool.

   **HOW SCORING WORKS — this is non-negotiable:**
   - You (Claude) read each company's raw data: description, revenue, founding year, HQ, exec signals
   - You think about what this business actually does
   - You write a descriptor that captures their specific activity
   - You rate fit (HIGH/MEDIUM/LOW) based on scoring-criteria.md
   - You write a 1-2 sentence rationale explaining why
   - You output a JSON array of scored objects

   **Do NOT write a Python script to score. Do NOT use keyword matching. Do NOT apply algorithmic rules.** The value is YOUR reading comprehension and judgment. A script cannot understand "Provides managed detection and response for mid-market financial services" — you can.

   After scoring 10, display as a markdown table (ONLY format — no cards, no lists):

   | # | Company | Revenue | Founded | Descriptor | Fit | Key Signal |
   |---|---------|---------|---------|------------|-----|------------|
   | 1 | Acme Fire | $12M | 1998 | fire inspection and compliance | HIGH | founder age 62 |

   Then use AskUserQuestion with 3-5 targeted calibration questions:
   - **Plain English.** Say "website is .ae which is UAE" not "domain TLD."
   - **Concrete.** Name the company and the issue.
   - **Decision-oriented.** "Should X count as Y or Z?" not "what do you think?"
   - Ask about patterns, thresholds, and edge cases actually encountered.

   After answers:
   - Adjust scoring approach for remaining batches
   - Save each calibration insight via MCP: call `save_skill_learning` with `skill="grata-search-enrichment"`, the target industry, category `"adjustment"`, and a single actionable statement per learning
   - Also record in `references/scoring-criteria.md` under `## Learned Adjustments` as local backup (format: `- [{industry}] {adjustment} (learned {date})`)

6. **Score remaining batches — Claude reads and scores every row** [HIGH freedom]

   **Mechanism — follow exactly:**
   1. Read 20-25 companies at a time from `/tmp/grata_extracted.json` (use Read tool with offset/limit)
   2. For EACH company in the batch, YOU read its description and data, then output a scored JSON object with: company_name, descriptor, fit_rating, rationale, plus all original fields
   3. Write the batch's scored results to `/tmp/grata_scored_batch_N.json` (use Python ONLY for the file write — you provide the JSON content, Python writes it)
   4. Repeat for next batch until all companies are scored
   5. After all batches: merge all batch files into `/tmp/grata_scored_all.json` (Python merge — no re-scoring)

   **Verification:** After merge, count must equal total extracted. If any company is missing, go back and score it. Every single row gets Claude's eyes on it.

   **Batch size:** 20-25 companies per batch. This keeps each scoring pass focused enough for quality. For 500 companies = ~20-25 batches.

   **What Claude outputs per company:**
   ```json
   {
     "company_name": "Bellwether Technology",
     "descriptor": "managed cybersecurity and SOC defense services",
     "fit_rating": "HIGH",
     "rationale": "Founded 1980, dedicated SOC practice, founder Poco Sloss (age 66) still active. Pure cyber, recurring managed contracts, $14M revenue in sweet spot.",
     "revenue": "$14M",
     "employees": "85",
     "year_founded": "1980",
     "hq": "New Orleans, LA",
     "website": "bellwethertech.com",
     "owner_signals": "Founder/CEO Poco Sloss, age 66, listed since founding"
   }
   ```

   **Do NOT write a Python scoring script. Do NOT batch-apply rules algorithmically.** Each company gets individual attention from Claude.

7. **Force-rank** [HIGH freedom]
   Second pass on scored results:
   - Load all HIGH-fit companies, rank by: thesis alignment > description clarity > revenue fit > founding year > owner presence
   - Assign H1, H2, H3...
   - Load all MEDIUM-fit companies, rank similarly
   - Assign M1, M2, M3...
   - LOW-fit companies all get "L" (no individual ranking)

8. **Preview and generate output** [LOW freedom]
   Show the user a summary table:

   | Tier | Count | Example |
   |------|-------|---------|
   | HIGH | 12 | Bellwether Technology (H1) |
   | MEDIUM | 34 | Pro4ia (M1) |
   | LOW | 405 | — |

   Then the top 20 HIGH-fit in detail:

   | Rank | Company | Descriptor | Revenue | Founded | Rationale |
   |------|---------|------------|---------|---------|-----------|
   | H1 | ... | ... | ... | ... | ... |

   Plus: data quality flags, calibration adjustments applied this run.

   Then IMMEDIATELY generate output — pipe complete enrichment JSON to `scripts/format_output.py <industry> <output_dir>`.
   Report file locations:

   | File | Path | Records |
   |------|------|---------|
   | Enriched xlsx | ./{industry}-{date}-enriched.xlsx | {n} |
   | Shortlist csv | ./{industry}-{date}-shortlist.csv | {high_count} |

   Suggest next step: "Run company-processor on the shortlist to prepare outreach contacts."

   Do NOT wait for approval between preview and file generation. The files are the deliverable.
</process>

<not_yet_available>
- **Per-industry thesis documents** — Dino has not yet shared these. Using general thesis + sector criteria until received.
- **OneDrive integration** — output files saved locally until OneDrive API configured.
- **HubSpot deduplication** — cannot yet cross-reference against existing HubSpot pipeline to exclude already-contacted companies.
</not_yet_available>

<success_criteria>
- [ ] Schema discovery runs without hardcoded assumptions
- [ ] grata-schema.md updated if format changed
- [ ] All companies scored with descriptor + fit rating + rationale
- [ ] No fabricated data in descriptors or ratings
- [ ] HIGH-fit companies force-ranked (H1, H2, H3...)
- [ ] Calibration questions asked via AskUserQuestion (not plain text)
- [ ] Enriched xlsx generated with conditional formatting (green HIGH, yellow MEDIUM)
- [ ] Shortlist csv generated with only HIGH-fit companies, sorted by rank
- [ ] Skill ran to completion — files exist on disk when done
</success_criteria>
