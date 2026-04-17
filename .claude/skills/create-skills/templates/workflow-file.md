# Workflow File Template

Standard structure for individual workflow files. Keep under 200 lines.

---

```markdown
<required_reading>
- references/{always-needed}.md
- references/{for-this-workflow}.md
</required_reading>

<objective>
{What this specific workflow accomplishes}
{One clear goal}
</objective>

<when_to_use>
{Conditions when this workflow applies}
- {Condition 1}
- {Condition 2}
</when_to_use>

<process>
1. **{Step Name}** [{HIGH/MEDIUM/LOW} freedom]
   {Instructions for this step}
   {Be specific for LOW, principled for HIGH}

2. **{Step Name}** [{freedom level}]
   {Instructions}

3. **{Step Name}** [{freedom level}]
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

**HIGH freedom** — Give principles:
```
1. **Write the post** [HIGH freedom]
   Create content that opens with a hook, delivers clear value,
   and matches the expected voice.
```

**MEDIUM freedom** — Give patterns:
```
2. **Search for examples** [MEDIUM freedom]
   Look in these locations:
   - data/examples/ (primary)
   - outputs/ (secondary)
   Return up to 5 relevant matches.
```

**LOW freedom** — Give exact scripts:
```
3. **Commit changes** [LOW freedom]
   Run exactly:
   git add -A && git commit -m "{message}"
   Do not modify these commands.
```
