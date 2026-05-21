# Workflow: What's Missing

<required_reading>
**Read these reference files NOW:**
1. references/missing-items.md
</required_reading>

<process>

## Step 1: Load Context

Ensure CIM or company information is loaded. If a memo or red-team analysis has already been generated in this conversation, use that as additional context — flag gaps that weren't addressed.

**If the input is a PDF deck/CIM**: render every page to an image and analyze the images — do NOT rely on the Read tool or text extraction for PDFs (the Read tool fails on PDFs on Windows; text extraction misses graphics-heavy slides and can be misleading). See `references/missing-items.md` → "How to Access the Document". Convenience CLI: `scripts/render_pdf.py`.

If nothing is loaded: "What deal are we reviewing? Share the CIM or tell me about the company."

## Step 2: Systematic Gap Detection

Deploy the missing items checklist from `references/missing-items.md` against the available materials.

For each checklist category:
1. Scan the entire document — critical data surfaces in financials, customer sections, appendices, not just where you'd expect
2. Mark items as **present** (with page citation) or **missing**
3. For partial data, note precisely what's absent (e.g., "GRR disclosed but NRR not provided")

## Step 3: Prioritize and Present

Present results in priority order per the reference file format:

1. **Critical Missing — Deal Breakers**: Items that could change the investment decision
2. **High Priority Gaps**: Important for valuation and risk assessment
3. **Red Flags Found**: Concerning data points that ARE in the CIM

For each missing item:
- State what's missing specifically
- Why it matters for this deal (1 sentence)
- What to ask for in the next management call or data request

## Step 4: Generate Action Items

Synthesize the gaps into a prioritized data request list:

| Priority | Data Needed | Why It Matters | Ask Who |
|----------|-------------|----------------|---------|
| 1 | ... | ... | Management / Broker |

Keep to the top 10-15 items. Don't create a 50-item list — focus on what would actually change the investment decision.

</process>

<success_criteria>
This workflow is complete when:
- [ ] Full CIM reviewed against the approved checklist
- [ ] Missing items categorized by severity (critical / high / medium)
- [ ] Page citations provided where partial data exists
- [ ] Red flags identified from data that IS present
- [ ] Prioritized data request list generated (top 10-15 items)
- [ ] Action items mapped to who to ask (management vs broker)
</success_criteria>
