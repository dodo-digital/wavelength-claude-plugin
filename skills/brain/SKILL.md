---
name: brain
description: Wavelength's LLM-maintained knowledge base. Compiles deal research, CIM analyses, and sourcing insights into a structured wiki with linked articles, auto-maintained indexes, and cross-referenced concepts. The LLM writes and maintains all wiki content — you rarely touch it directly.
invocation: /brain
---

<essential_principles>

**You are the wiki compiler.** You write and maintain all content in the brain. The user rarely edits brain files directly. When new information enters the system — from a CIM analysis, a Grata export, a conversation, a call note — you compile it into structured wiki articles, update indexes, and link related concepts.

**Brain location:** Injected at session start as `brain_dir` by the SessionStart hook. If not available, resolve from `CLAUDE_PLUGIN_DATA` env var or default to `~/.wavelength/brain`.

**Static references** (ship with plugin): `{plugin_root}/context/thesis.md`, `context/sources.md`

**Wiki structure:**
```
brain/
  BRAIN.md              # Master index — auto-maintained, loaded at session start
  companies/            # One article per company analyzed
  industries/           # Industry articles — patterns, dynamics, compiled from cross-company research
  people/               # Key contacts — brokers, founders, operators, advisors
  learnings/            # Cross-deal insights, thesis refinements, patterns
```

**Every article uses wiki-links** to connect related content: `[[companies/acme-security]]`, `[[industries/dental-it]]`, `[[people/john-broker]]`. When creating an article, link it to every related article that already exists. When an existing article is relevant to new content, update it with a backlink.

</essential_principles>

<intake>
What would you like to do?

1. **Compile** — Ingest new information and compile it into wiki articles
2. **Query** — Ask questions against the knowledge base
3. **Maintain** — Lint the wiki, find gaps, suggest connections
4. **Thesis** — View or update investment thesis
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "compile", "save", "add", "ingest", "remember", "store", "log" | Compile |
| 2, "query", "search", "find", "what do we know", "have we seen", "recall" | Query |
| 3, "maintain", "lint", "health check", "clean up", "connections", "gaps" | Maintain |
| 4, "thesis", "criteria", "what are we looking for" | Thesis |
| Company name or context from prior analysis in conversation | Compile (infer from context) |
| A question about a company, industry, or pattern | Query |
</routing>

<compile>

## Compile: Ingest → Structure → Link → Index

This is the core operation. Raw information goes in, structured wiki articles come out.

### Step 1: Identify what's new

Determine what information is being added:
- Output from `/deal-analysis` (memo, scorecard, exploration notes)
- Output from `/red-team` (risk assessment, missing items)
- Output from `/grata-search-enrichment` (batch company scores, shortlist)
- Conversation context (research discussion, call notes, ad-hoc insights)
- Raw documents (CIM, SIM, financials, marketing materials)

### Step 2: Compile company article

If the input involves a specific company, create or update `{brain_dir}/companies/{slug}.md`:

```markdown
---
company: "{Name}"
industry: "{industry-slug}"
sub_industry: "{sub-industry-slug}"
revenue: "{estimate with year}"
ebitda: "{estimate with margin %}"
location: "{City, State}"
source: "{broker-cim | grata | referral | conference | cold-outbound}"
owner_profile: "{age/tenure if known}"
date_added: "{YYYY-MM-DD}"
last_updated: "{YYYY-MM-DD}"
verdict: "{pursuing | passed | watching | analyzed}"
thesis_fit_score: {0-100 or null}
related:
  - "[[companies/{related-slug}]]"
  - "[[industries/{industry-slug}]]"
---

# {Company Name}

## Summary
{2-3 sentences: what they do, who they serve, why they're relevant}

## Thesis Fit
{How this matches the Wavelength thesis — strengths and gaps}

## Key Metrics
| Metric | Value | Source |
|--------|-------|--------|

## Analysis
{Key findings from deal-analysis, red-team, or manual review}

## Concerns
{Red flags, missing data, reasons for caution}

## Next Steps
{What to do next — request CIM, schedule call, pass, etc.}

## Activity Log
- {date}: {what happened}
```

**If the file already exists**: Update it. Add new findings to Analysis, update metrics, append to Activity Log. Preserve existing content — the wiki is additive.

### Step 3: Compile industry article (if applicable)

If the company belongs to an industry that doesn't have an article yet, create `{brain_dir}/industries/{slug}.md`. If it exists, update it with new data points.

Industry articles compile cross-company patterns:
```markdown
# {Industry Name}

## Overview
{What this industry is, market size, growth dynamics}

## Wavelength Thesis Fit
{Why this industry matters for the search, which sub-thesis it falls under}

## Companies Evaluated
| Company | Verdict | Score | Date |
|---------|---------|-------|------|
| [[companies/{slug}]] | {verdict} | {score} | {date} |

## Patterns Observed
{Cross-company insights — what's consistent across companies in this space}

## Key Risks
{Industry-level risks that apply broadly}

## Open Questions
{What we still need to learn about this industry}
```

### Step 4: Compile people article (if applicable)

If a key person was mentioned (broker, founder, advisor), create or update `{brain_dir}/people/{slug}.md`:
```markdown
# {Name}

**Role:** {broker | founder | advisor | operator}
**Company:** [[companies/{slug}]] or firm name
**Contact:** {email, phone, LinkedIn if known}

## Context
{How we know them, relationship history}

## Notes
- {date}: {interaction or insight}
```

### Step 5: Extract learnings

If cross-deal insights emerged (patterns, red flags, thesis refinements), append to the appropriate file in `{brain_dir}/learnings/`:
- `patterns.md` — recurring patterns across deals
- `red-flags.md` — warning signs to watch for
- `thesis-refinements.md` — how the thesis is evolving based on what we're seeing
- `{topic}.md` — topic-specific learnings

Each learning entry:
```markdown
## {date} — {topic}
**Source:** [[companies/{slug}]] or conversation
{The insight — what we learned and why it matters}
```

### Step 6: Update BRAIN.md index

After compiling, **always** update `{brain_dir}/BRAIN.md`:
- Add/update the company in the Companies table
- Add/update industry in the Industries list
- Add any new learnings to Key Learnings
- Update Recent Activity with what just happened
- Update the "Last updated" timestamp

</compile>

<query>

## Query: Research answers across the wiki

1. Read `{brain_dir}/BRAIN.md` to understand what's in the wiki.
2. Based on the question, identify relevant articles (companies, industries, learnings).
3. Read those articles.
4. Synthesize an answer with references to specific articles: "Based on [[companies/acme-security]] and [[industries/dental-it]]..."
5. If the query reveals a gap, note it: "We don't have data on X yet. Want me to research it?"

**If the wiki doesn't have the answer**: Say so directly. Don't fabricate. Suggest what to look into.

</query>

<maintain>

## Maintain: Lint, connect, enhance

Run periodically or on request. Checks:

1. **Index consistency**: Does BRAIN.md accurately reflect what's in the wiki? Missing entries? Stale verdicts?
2. **Broken links**: Do all wiki-links point to existing articles?
3. **Missing connections**: Are there companies in the same industry that aren't linked? People associated with companies that don't have backlinks?
4. **Data gaps**: Which company articles are thin? What metrics are missing across the board?
5. **Pattern detection**: Are there emerging patterns across companies that should become a learnings entry?
6. **Stale content**: Articles that haven't been updated in a long time — are verdicts still current?

Output a health report with specific action items. Offer to fix issues automatically.

</maintain>

<thesis>

## Thesis: View or update

**View**: Read `{plugin_root}/context/thesis.md` and any refinements in `{brain_dir}/learnings/thesis-refinements.md`.

**Update**: Append dated entries to `{brain_dir}/learnings/thesis-refinements.md`. The canonical thesis ships with the plugin. Personal refinements layer on top.

</thesis>

<auto_compile>

## Auto-compile (triggered by CLAUDE.md behavior, not by /brain invocation)

After ANY deal analysis (`/deal-analysis`, `/red-team`, `/grata-search-enrichment`), the system should ask:

"Want me to compile this into the brain?"

If yes, run the Compile workflow using the analysis output as input. This is how the wiki grows organically from normal deal work.

</auto_compile>
