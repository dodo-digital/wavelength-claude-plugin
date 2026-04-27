---
name: create-skills
description: Create Claude Code skills with context engineering built in. Use when building new skills, adding workflows, or auditing existing skills. Supports simple and router archetypes.
context_budget:
  skill_md: 200
  max_references: 6
---

<auto_trigger>
keywords:
  - "create skill"
  - "new skill"
  - "add skill"
  - "build skill"
  - "skill template"

intent_patterns:
  - "create.*skill"
  - "add.*skill"
  - "build.*workflow"
  - "new.*workflow"
</auto_trigger>

<objective>
Create well-structured, context-efficient Claude Code skills that follow progressive disclosure patterns. Each skill declares its context budget and loads only what's needed.
</objective>

<essential_principles>
1. **Progressive Disclosure** — Layer 1: Metadata (~50 tokens at startup). Layer 2: SKILL.md (when triggered). Layer 3: References (on-demand).
2. **Conciseness** — The context window is a public good. Only add context Claude doesn't already have.
3. **Pure XML Structure** — Use `<tags>` not `## headings` in skill bodies. 25% token savings.
4. **Required Reading** — Every workflow declares which references to load.
</essential_principles>

<quick_start>
1. User describes what the skill should do
2. Classify archetype: simple (single file) or router (multiple workflows)
3. Generate SKILL.md with appropriate structure
4. If router: generate workflows and references
5. Validate against success criteria
</quick_start>

<intake>
What would you like to do?

1. **Create simple skill** (single SKILL.md, max 150 lines) → Read templates/simple-skill.md
2. **Create router skill** (SKILL.md + workflows/ + references/) → Read templates/router-skill.md
3. **Add workflow to existing skill** → Read templates/workflow-file.md
4. **Audit existing skill** → Check structure, context budget, XML compliance

Ask the user which they need, or infer from their request.
</intake>

<archetype_selection>
**Simple** — Single SKILL.md (max 150 lines)
- One clear workflow, no sub-components
- Examples: decision traces, goal tracking, basic utilities

**Router** — SKILL.md + workflows/ + references/
- Multiple distinct use cases with shared references
- Examples: deal sourcing, content creation, multi-step analysis
</archetype_selection>

<process>
1. **Gather requirements** [MEDIUM freedom]
   Ask what the skill does, when it triggers, and what outputs it produces.

2. **Select archetype** [LOW freedom]
   Simple: one workflow, < 150 lines. Router: multiple workflows, shared refs.

3. **Generate SKILL.md** [MEDIUM freedom]
   Use the matching template from templates/. Include:
   - YAML frontmatter (name, description with triggers, context_budget)
   - XML-structured body (objective, quick_start, process/routing, success_criteria)
   - `<auto_trigger>` block with keywords and intent patterns

4. **Generate supporting files** [MEDIUM freedom]
   Router only: create workflows/ and references/ directories.
   Each workflow gets `<required_reading>`, `<objective>`, `<process>`, `<success_criteria>`.

5. **Validate** [LOW freedom]
   Read references/skill-structure.md for validation checklist. Verify all criteria pass.
</process>

<references_index>
| Reference | Purpose |
|-----------|---------|
| references/core-principles.md | Context engineering fundamentals |
| references/skill-structure.md | Directory structure, naming, validation |
</references_index>

<templates_index>
| Template | Use For |
|----------|---------|
| templates/simple-skill.md | Single-file skills |
| templates/router-skill.md | Multi-workflow skills |
| templates/workflow-file.md | Individual workflow files |
</templates_index>

<success_criteria>
- [ ] Skill follows selected archetype structure
- [ ] SKILL.md under line limit (150 simple, 200 router)
- [ ] Frontmatter has name, description with triggers, context_budget
- [ ] Pure XML structure (no markdown headings in body)
- [ ] Auto-trigger block with keywords for skill router
- [ ] All workflows have `<required_reading>` (router only)
- [ ] success_criteria uses checkbox format
</success_criteria>
