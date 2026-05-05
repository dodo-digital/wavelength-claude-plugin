# Memory Save Types

Use this reference before calling `update_context`. Memory should contain durable, synthesized context that helps Wavelength make future deal, sourcing, diligence, or outreach decisions.

## Common Inputs

Every saved document should have:

- `slug`: canonical slug from the table below
- `doc_type`: one of the memory types below
- `title`: human-readable title
- `content`: Markdown with stable headings
- `tags`: namespaced tags such as `company/acme-security`, `industry/cybersecurity`, `topic/exclusions`, `skill/grata-search-enrichment`

Prefer a small number of precise tags over broad catch-all tags.

## Types

| Area | doc_type | Use for | Slug | Required tags |
|------|----------|---------|------|---------------|
| `/thesis/` | `thesis` | Wavelength thesis, exclusion rules, evolving criteria | `thesis-{topic}` | `topic/{topic}` |
| `/companies/` | `company` | Company summaries, deal analysis, owner notes, diligence status | `company-{company}` | `company/{company}`, `industry/{industry}`, `status/{status}` |
| `/industries/` | `industry` | Category patterns, market structure, repeated deal learnings | `industry-{industry}` | `industry/{industry}` |
| `/people/` | `person` | Broker, founder, operator, lender, or advisor relationship context | `person-{name}` | `person/{name}` |
| `/learnings/` | `learning` | Reusable operating lessons from skills or workflows | `learning-{topic}` | `topic/{topic}`, `skill/{skill}` when applicable |
| `/sources/` | `source` | Where canonical files, folders, exports, or systems live | `source-{name}` | `source/{name}` |
| `/criteria/` | `criteria` | Scorecard, qualification, filtering, or outreach selection rules | `criteria-{topic}` | `topic/{topic}` |
| `/templates/` | `template` | Reusable memo, outreach, prompt, or export structures | `template-{name}` | `topic/{topic}` |

## Company Template

```markdown
# {Company Name}

## Summary
{2-3 sentences on what they do and why they matter.}

## Status
{pipeline status, ownership, last reviewed date, next action.}

## Thesis Fit
{Fit against Wavelength criteria. Be explicit about fit drivers and disqualifiers.}

## Key Metrics
| Metric | Value | Source |
|--------|-------|--------|

## Analysis
{Durable findings from memo, scorecard, call, or research.}

## Concerns
{Specific risks, missing data, and follow-up diligence questions.}

## Next Steps
{Concrete follow-up.}

## Activity Log
- {YYYY-MM-DD}: {what changed and why}
```

## Industry Template

```markdown
# {Industry}

## Overview
{What the category is and how Wavelength defines it.}

## Thesis Fit
{Why this category is attractive, neutral, or unattractive.}

## Companies Evaluated
| Company | Verdict | Score | Date |
|---------|---------|-------|------|

## Patterns Observed
{Cross-company insights, buyer behavior, margin patterns, recurring risks.}

## Exclusions
{Subcategories or signals that should be filtered out.}

## Open Questions
{What to learn next.}

## Activity Log
- {YYYY-MM-DD}: {what changed and why}
```

## Learning Template

```markdown
# {Topic}

## Current Rule
{The actionable rule future agents should apply.}

## Evidence
- {YYYY-MM-DD}: {source and why it changed our view}

## Applies To
{Industries, skills, tools, or workflows where this matters.}
```

## Criteria Template

```markdown
# {Criteria Name}

## Rule
{The current decision rule.}

## Use When
{When an agent should apply it.}

## Do Not Use When
{Known exceptions.}

## Evidence
- {YYYY-MM-DD}: {why this rule exists}
```

## Source Template

```markdown
# {Source Name}

## What It Contains
{System, folder, file, report, or data source description.}

## How To Access
{Connector, path, URL, or workflow. Do not save secrets.}

## Use For
{When future agents should use this source.}

## Caveats
{Known data quality or permission issues.}
```

## What Not To Save

- Secrets, API keys, access tokens, passwords, or private credentials
- Raw full exports when a short summary plus path is enough
- Unreviewed scratch notes
- Large copyrighted passages copied from documents
- User preferences unrelated to Wavelength deal work
- Temporary CLI output or MCP smoke test logs
