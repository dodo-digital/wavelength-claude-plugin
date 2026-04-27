# Simple Skill Template

Use for single-file skills with one clear workflow. Max 150 lines.

---

```markdown
---
name: {skill-name}
description: {What it does}. Use when {trigger conditions}. {Third person}
context_budget:
  skill_md: 150
---

<auto_trigger>
keywords:
  - "{keyword-1}"
  - "{keyword-2}"

intent_patterns:
  - "{verb}.*{object}"
</auto_trigger>

<objective>
{Clear goal statement - what this skill accomplishes}
{Keep under 10 lines}
</objective>

<quick_start>
{Minimal path to common use}
1. {First step}
2. {Second step}
3. {Third step}
</quick_start>

<process>
{Step-by-step instructions}

1. **{Step name}** [{HIGH/MEDIUM/LOW} freedom]
   {Instructions for this step}

2. **{Step name}** [{freedom level}]
   {Instructions}

3. **{Step name}** [{freedom level}]
   {Instructions}
</process>

<success_criteria>
- [ ] {Measurable outcome 1}
- [ ] {Measurable outcome 2}
- [ ] {Measurable outcome 3}
</success_criteria>
```

---

## Freedom Level Guidelines

**HIGH freedom** — Give principles, let Claude decide approach:
```
1. **Write the analysis** [HIGH freedom]
   Create content that delivers clear value and matches the expected format.
```

**MEDIUM freedom** — Give patterns and locations:
```
2. **Search for examples** [MEDIUM freedom]
   Look in these locations:
   - data/examples/ (primary)
   - outputs/ (secondary)
   Return up to 5 relevant matches.
```

**LOW freedom** — Give exact commands:
```
3. **Save output** [LOW freedom]
   Write to outputs/{date}-{name}.md
   Do not modify the path format.
```
