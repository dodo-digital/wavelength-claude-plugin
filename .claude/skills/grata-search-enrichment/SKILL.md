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
- **Human-in-the-loop.** Never disappear for a long grind. Confirm key points before acting. Show a short plan. Let the user adjust. Surface checkpoints, not just final output.
- **Self-healing schema.** Never hardcode column positions. Discover structure each run, compare to `references/grata-schema.md`, adapt and update if changed.
- **Thesis-first.** Load `references/scoring-criteria.md` before scoring. Every rating must reference specific thesis criteria.
- **Calibrate before grinding.** Always score 10 companies first, ask targeted questions, record learnings, THEN process the rest. Never skip calibration.
- **Learnings persist.** Read `## Learned Adjustments` in scoring-criteria.md at start of every run. State them to the user. Update after calibration.
- **No fabrication.** If company data is insufficient for confident rating, mark MEDIUM with rationale noting uncertainty. Never invent details.
- **Batch processing.** Process 30-50 companies per scoring pass. Accumulate results. Do not attempt all 400+ in a single prompt.
- **Descriptors are specific.** Must fit "They do {descriptor}" and distinguish from peers. See anti-patterns in scoring-criteria.md.
- **Update the living schema.** If grata-schema.md needs changes after discovery, update it before proceeding.
- **Always generate files.** The job is not done until xlsx + csv output files exist on disk. Chat display is preview only.
- **Tables for everything.** All previews, calibration batches, and summaries must use markdown tables. Fixed columns, aligned, scannable. Never dump free-text lists.
</essential_principles>

<process>
1. **Discover and validate schema** [LOW freedom]
   Run `scripts/discover_export.py` on the uploaded file.
   Read `references/grata-schema.md`. Compare silently.
   - **Match → say nothing, proceed immediately to step 2.** Do not report column counts, tab names, or structure details.
   - **Minor mismatch** (renamed column, new column, removed column) → one sentence: "Schema changed: {what changed}. Updated grata-schema.md." Then proceed.
   - **Unrecognizable** → stop, ask user to confirm column mapping.

2. **Intake and load learnings** [LOW freedom]
   Ask the user:
   - Target industry for this search (e.g., "fire safety", "cybersecurity")
   - Path to industry-specific thesis docs (if available — otherwise use general criteria)
   - Any additional exclusions (e.g., "skip construction", "exclude companies under $3M")

   Then load prior learnings:
   - Read `references/scoring-criteria.md` — especially the `## Learned Adjustments` section
   - If adjustments exist for this industry, state them upfront: "From previous runs, I know: {adjustments}. Still applying these?"
   - If no prior learnings exist, note: "No prior calibration for {industry}. Will calibrate on first batch."

3. **Confirm plan** [LOW freedom]
   After discovery + intake, show a short execution plan. Format:

   ```
   ## Execution Plan
   | Step | What | Est. |
   |------|------|------|
   | Extract | {n} companies from Companies tab | ~30s |
   | Calibrate | Score first 10, ask you 3-5 questions | ~3 min |
   | Score | Remaining {n-10} in {x} batches of 40 | ~15 min |
   | Rank | Force-rank HIGH and MEDIUM tiers | ~2 min |
   | Output | Generate xlsx + csv files | ~30s |

   **Criteria loaded:** {list active criteria + any learned adjustments}
   **Exclusions:** {user-specified exclusions}
   ```

   Wait for user to confirm or adjust (e.g., "skip the exec tab scan", "use batches of 20", "add exclusion: no companies under $5M").

4. **Extract company data** [MEDIUM freedom]
   Read the Companies tab into structured JSON (use Python or Read tool with offset/limit for large files).
   Scan executive tabs for owner-operator signals:
   - Founder/Owner in title → strong signal
   - Small exec team (1-3 contacts) → moderate signal
   - No institutional titles (VP of BD, Chief Strategy Officer) → moderate signal
   Save extracted JSON to a temp file for batch processing.

5. **Calibration batch** [LOW freedom]
   Score the FIRST 10 companies only. Show results in a table:

   | # | Company | Revenue | Founded | Descriptor | Fit | Key Signal |
   |---|---------|---------|---------|------------|-----|------------|
   | 1 | Acme Fire | $12M | 1998 | fire inspection and compliance | HIGH | founder age 62 |

   Then ask targeted calibration questions based on what you observed:
   - Edge cases: "Company X is an MSP with a dedicated SOC — is that MEDIUM or LOW for you?"
   - Threshold questions: "Founder is 45 — is that too young for retirement signal, or still relevant?"
   - Sector boundaries: "Company Y does {adjacent thing} — in or out of scope?"
   - Descriptor style: "Here are my descriptors for the first 10 — are these the right level of specificity?"
   - Any patterns in the data: "6 of 10 are MSP/resellers. Should I auto-LOW all MSPs, or case-by-case?"

   Ask 3-5 targeted questions. Do NOT ask generic "does this look right?" — ask about the specific judgment calls you had to make.

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

8. **Preview and approve** [LOW freedom]
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
   Wait for approval before generating output files.

9. **Generate output** [LOW freedom]
   Pipe complete enrichment JSON to `scripts/format_output.py <industry> <output_dir>`.
   Report file locations in a table:

   | File | Path | Records |
   |------|------|---------|
   | Enriched xlsx | ./cybersecurity-2026-04-20-enriched.xlsx | 451 |
   | Shortlist csv | ./cybersecurity-2026-04-20-shortlist.csv | 12 |

   Suggest next step: "Run company-processor on the shortlist to prepare outreach contacts."
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
- [ ] Preview shown and user approved before file generation
- [ ] Enriched xlsx has conditional formatting (green HIGH, yellow MEDIUM)
- [ ] Shortlist csv contains only HIGH-fit companies, sorted by rank
- [ ] Batch processing handled 400+ companies without context overflow
</success_criteria>
