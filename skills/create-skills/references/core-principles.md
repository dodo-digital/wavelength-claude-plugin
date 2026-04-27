<overview>
Core principles of context engineering for Claude Code skills. These apply to every skill.
</overview>

<progressive_disclosure>
Don't load everything upfront. Structure content in layers.

```
Layer 1: Metadata
├── name, description
├── ~30-50 tokens at startup
└── Loaded for ALL skills

Layer 2: SKILL.md
├── Loaded when skill triggers
├── Max 200 lines (router) or 150 lines (simple)
└── Contains essential principles + routing

Layer 3: Supporting files
├── Loaded on-demand during execution
├── Referenced by <required_reading>
└── Zero tokens until needed
```

The constraint isn't "how much can I include?" but "how do I structure so Claude loads only what's needed?"
</progressive_disclosure>

<conciseness>
The context window is a public good.

Default assumption: Claude is already very smart.

Before adding content, ask:
- Does Claude need this, or does it already know?
- Can this be in a reference file instead of inline?
- Is this the minimum needed?
- Does this paragraph justify its token cost?
</conciseness>

<xml_structure>
Use XML blocks, not markdown headings, in skill bodies.

```xml
<!-- Good -->
<objective>
Clear goal statement
</objective>

<process>
Step-by-step instructions
</process>
```

Why: 25% token savings vs markdown, unambiguous section boundaries, better Claude performance.
</xml_structure>

<required_reading_pattern>
Every workflow declares which references to load.

```xml
<required_reading>
- references/core-principles.md (always)
- references/specific-topic.md (for this workflow only)
</required_reading>
```

This ensures context is task-specific, not monolithic. Irrelevant references stay on disk at zero tokens.
</required_reading_pattern>

<essential_inline>
Critical content goes directly in SKILL.md. Content that must always be loaded, cannot be skipped, and shapes every workflow — put it inline, not in a reference.
</essential_inline>
