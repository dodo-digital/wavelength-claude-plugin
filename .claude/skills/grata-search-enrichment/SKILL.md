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
- **Run to completion.** This skill does NOT stop until output files exist on disk. Asking a question via AskUserQuestion is a checkpoint within the flow, not an exit. After the user answers, keep going. Never print a question as plain text and wait — that halts execution.
- **AskUserQuestion or nothing.** Every question to the user MUST use the AskUserQuestion tool. Never ask questions as plain text. If you have nothing worth asking, don't ask — just proceed.
- **Smart questions only.** Ask when there's a real judgment call: edge cases from the data, conflicting signals, threshold decisions. Do NOT ask when you have no basis for the question or when the answer is already in scoring-criteria.md.
- **Exclusions from learnings, not data peeking.** If prior calibration (Learned Adjustments) includes exclusions for this industry, suggest those. If nothing exists yet, just offer "None" and free-text. Never infer exclusion options by reading ahead into the data.
- **Self-healing schema.** Never hardcode column positions. Discover structure each run, compare to `references/grata-schema.md`, adapt and update if changed.
- **Thesis-first.** Load `references/scoring-criteria.md` before scoring. Every rating must reference specific thesis criteria.
- **Calibrate before grinding.** Always score 10 companies first, ask targeted questions, record learnings, THEN process the rest. Never skip calibration.
- **Learnings persist.** Read `## Learned Adjustments` in scoring-criteria.md at start of every run. Apply them. Update after calibration.
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
   Load `references/scoring-criteria.md` — read `## Learned Adjustments` section first.

   Use AskUserQuestion to ask:
   - Target industry (e.g., "fire safety", "cybersecurity")
   - If Learned Adjustments exist for this industry and include exclusions or rules worth confirming, offer those as suggested options (e.g., "Apply prior rule: MSPs without dedicated SOC = LOW"). This is useful — it reminds the user what was learned before.
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

4. **Extract company data** [MEDIUM freedom]
   Read the Companies tab into structured JSON (use Python or Read tool with offset/limit for large files).
   Scan executive tabs for owner-operator signals:
   - Founder/Owner in title → strong signal
   - Small exec team (1-3 contacts) → moderate signal
   - No institutional titles (VP of BD, Chief Strategy Officer) → moderate signal
   Save extracted JSON to a temp file for batch processing.

5. **Calibration batch** [LOW freedom]
   Score the FIRST 10 companies only. Output MUST be a single markdown table — never a numbered list, never card blocks:

   | # | Company | Revenue | Founded | Descriptor | Fit | Key Signal |
   |---|---------|---------|---------|------------|-----|------------|
   | 1 | Acme Fire | $12M | 1998 | fire inspection and compliance | HIGH | founder age 62 |
   | 2 | ... | ... | ... | ... | ... | ... |

   This is the ONLY acceptable format. Do not deviate.

   Then use AskUserQuestion with 3-5 targeted calibration questions. Rules for questions:
   - **Plain English.** No jargon. No acronyms the user wouldn't use. Say "website is .ae which is UAE" not "domain TLD."
   - **Concrete.** Name the specific company and the specific issue. "Bellwether's founder is 66 — that's a strong retirement signal. But Systems Engineering's CEO is 45. Where's your cutoff for 'near retirement'?"
   - **Decision-oriented.** Frame so the user can answer in one sentence. Not "what do you think about X?" but "Should X count as Y or Z?"
   - Edge cases actually encountered in the first 10
   - Patterns: "7 of 10 are general IT companies that added cybersecurity. Want me to score those differently from pure cyber firms?"
   - Thresholds: "Where's the age cutoff for retirement signal — 50? 55? 60?"

   Do NOT ask generic "does this look right?" — ask about specific judgment calls.

   After answers:
   - Adjust scoring approach for remaining batches
   - Record adjustments in `references/scoring-criteria.md` under `## Learned Adjustments`
   - Format: `- [{industry}] {adjustment} (learned {date})`

6. **Score remaining batches** [HIGH freedom]
   Apply calibrated criteria to remaining companies.
   Process 30-50 per batch:
   - Read batch from extracted JSON
   - For each company: generate descriptor, rate fit (HIGH/MEDIUM/LOW), write 1-2 sentence rationale
   - Apply calibration adjustments consistently
   - Append scored results to accumulation file
   Repeat until all companies processed.

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
