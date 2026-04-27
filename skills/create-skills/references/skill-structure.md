<overview>
Directory structure, naming conventions, and validation checklist for Claude Code skills.
</overview>

<directory_structure>
```
skill-name/
├── SKILL.md              # Main entry point (required)
├── workflows/            # One per use case (router only)
│   ├── workflow-1.md
│   └── workflow-2.md
├── references/           # Shared knowledge (optional)
│   └── domain-knowledge.md
├── templates/            # Output formats (optional)
│   └── output-format.md
└── scripts/              # Automation scripts (optional)
    └── helper.py
```
</directory_structure>

<naming_conventions>
Use **verb-noun convention** for skill names:
- `create-skills`, `create-hooks` — Building/authoring
- `analyze-deals`, `enrich-contacts` — Analysis/processing
- `generate-memos`, `generate-reports` — Generation

Validation rules:
- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- Must match directory name exactly
- No reserved words: "anthropic", "claude"
</naming_conventions>

<frontmatter_requirements>
Every SKILL.md must have valid YAML frontmatter:

```yaml
---
name: skill-name
description: What it does. Use when [trigger conditions]. Third person.
context_budget:
  skill_md: 150  # or 200 for router
  max_references: 4  # router only
---
```

Required fields:
- `name:` — Skill identifier (kebab-case)
- `description:` — What it does AND when to use (includes trigger phrases)
- `context_budget:` — Token budget declaration

Description must:
- Be non-empty, max 1024 characters
- Use third person ("Processes files" not "I process files")
- Include trigger phrases ("Use when...")
</frontmatter_requirements>

<xml_requirements>
Remove ALL markdown headings from skill body content. Replace with semantic XML tags.

Required tags (every skill):
- `<objective>` — What the skill does (1-3 paragraphs)
- `<quick_start>` — Immediate actionable guidance
- `<success_criteria>` — How to know it worked (checkbox format)

Conditional tags:
- `<essential_principles>` — Critical non-skippable content
- `<intake>` — User routing options
- `<routing>` — Intent-to-workflow mapping table
- `<process>` — Step-by-step procedure
- `<auto_trigger>` — Keywords for skill router
- `<references_index>` — Reference file listing
- `<templates_index>` — Template file listing
</xml_requirements>

<validation_checklist>
Before finalizing a skill, verify:

- [ ] YAML frontmatter valid (name matches directory, description in third person)
- [ ] No markdown headings in body (pure XML structure)
- [ ] Required tags present: objective, quick_start, success_criteria
- [ ] All XML tags properly closed
- [ ] SKILL.md under line limit (150 simple, 200 router)
- [ ] Auto-trigger block present with keywords
- [ ] File paths use forward slashes
- [ ] References one level deep from SKILL.md
</validation_checklist>
