---
name: memory
description: Wavelength's shared MCP-backed memory. Saves and retrieves deal context, company notes, industry patterns, people notes, thesis refinements, and source references using query_context and update_context so knowledge is shared across users.
invocation: /memory
---

<purpose>

Memory is Wavelength's shared context layer. It is not a local folder. It is a virtual filesystem backed by Wavelength MCP:

- Read/list/search with `query_context`
- Save/update with `update_context`
- Version history is handled by the MCP server
- Content is shared across Harrison, Dino, and other authenticated users

Use this skill when the user asks what Wavelength knows, wants something remembered, asks to save deal findings, asks to list memory, or when another Wavelength skill produces durable context future sessions should reuse.

</purpose>

<fast_rules>

- `query_context {}` lists the virtual filesystem.
- `query_context {"slug":"..."}` reads one known item.
- `query_context {"tags":["industry/..."]}` is best for targeted recall.
- `query_context {"keyword":"..."}` is the fallback for fuzzy search.
- `query_context {"slug":"...","include_history":true}` is for audit or change-history questions.
- `update_context` saves durable synthesized context, not scratch work.
- If the user says "remember", "save", "store", "log", or "update memory", save directly.
- Otherwise, ask before saving.

</fast_rules>

<virtual_filesystem>

Use these conventions so memory stays browsable:

| Area | doc_type | Slug pattern | Required tags |
|------|----------|--------------|---------------|
| `/thesis/` | `thesis` | `thesis-{topic}` | `topic/{topic}` |
| `/companies/` | `company` | `company-{company-slug}` | `company/{company-slug}`, `status/{status}` |
| `/industries/` | `industry` | `industry-{industry-slug}` | `industry/{industry-slug}` |
| `/people/` | `person` | `person-{person-slug}` | `person/{person-slug}` |
| `/learnings/` | `learning` | `learning-{topic-slug}` | `topic/{topic}`, `skill/{skill-name}` when applicable |
| `/sources/` | `source` | `source-{source-slug}` | `source/{source-slug}` |
| `/criteria/` | `criteria` | `criteria-{topic-slug}` | `topic/{topic}` |
| `/templates/` | `template` | `template-{template-slug}` | `topic/{topic}` |

When the user asks to "list memory" or "show the filesystem", call `query_context` with no arguments and present the result grouped by area using the table above.

For the full save taxonomy, read `references/save-types.md`.

</virtual_filesystem>

<query_policy>

Read `references/query-policy.md` when deciding whether another skill should query memory.

Default to querying memory before:
- Deal analysis, scorecards, red-team work, or diligence planning
- Grata scoring runs, especially when the industry is known
- Company processing when the company, campaign, industry, or outreach rule may already exist
- Thesis, criteria, source, or template questions

Usually do not query memory for:
- Pure mechanics like installing the plugin, checking MCP status, or validating one email
- One-off syntax, command, or local file questions
- Requests where the user supplied all needed context and memory would add latency without changing the answer

</query_policy>

<read_workflow>

## Query Memory

1. If the user asks for the full index, call `query_context` with `{}`.
2. If the user names a known item, call `query_context` with its exact `slug`.
3. If the user asks by topic, company, industry, person, skill, or source, call `query_context` with tags first.
4. If tags are unknown or broad, call `query_context` with `keyword`.
5. For audit/history questions, include `include_history: true` with the slug.

Examples:

```json
{"slug":"company-acme-security","include_history":true}
{"tags":["industry/cybersecurity"]}
{"tags":["skill/grata-search-enrichment","topic/exclusions"]}
{"keyword":"founder-owned dental IT"}
```

When answering from memory, cite the memory docs by slug: "Based on `company-acme-security` and `industry-cybersecurity`..."

If memory does not contain the answer, say that directly and suggest what should be researched or saved.

</read_workflow>

<write_workflow>

## Save To Memory

Use `update_context` for durable information. Do not save scratch notes, temporary command output, or raw large datasets. Save synthesized context a human would want later.

Before saving:
- Choose one canonical slug.
- Query that slug first if you are updating an existing item.
- Preserve useful existing content and append/update; do not overwrite with a thin summary.
- Use Markdown content with stable headings.
- Add specific tags. Prefer namespaced tags over free-form tags.

Read `references/save-types.md` for the right doc_type, slug, tags, and content template before saving anything beyond a short note.

</write_workflow>

<when_to_save>

Ask whether to save unless the user explicitly says "remember", "save", "log", "store", or "update memory".

Save or offer to save after:
- A deal memo, scorecard, exploration, red-team, or diligence gap analysis
- A Grata scoring calibration or shortlist with reusable criteria
- A company-processor run that reveals schema changes, title edge cases, or outreach rules
- A call note, broker/founder note, or durable person relationship note
- A thesis refinement, new exclusion rule, or recurring pattern across deals
- A source location that future users should know about

Do not save:
- Secrets, API keys, credentials, or private tokens
- Raw full exports when a summarized artifact is enough
- One-off command output
- User preferences unrelated to Wavelength deal work
- Third-party copyrighted material copied in bulk

</when_to_save>

<maintenance>

When asked to maintain or clean memory:

1. Call `query_context` with `{}`.
2. Look for duplicate slugs, thin docs, stale statuses, missing tags, and orphaned docs.
3. Report issues in a table.
4. Ask before making bulk edits.
5. Use `update_context` to normalize content one document at a time.

</maintenance>
