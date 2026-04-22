# Workflow: Score Deal

<required_reading>
**Read these reference files NOW:**
1. references/scorecard.md
</required_reading>

<process>

## Step 1: Gather Inputs

The scorecard requires specific metrics. These can come from:
- A CIM already analyzed in this conversation
- Sub-agent outputs from a generate-memo workflow
- User providing metrics directly
- Company documents or descriptions

### Required Inputs

| Input | Category | How to obtain |
|---|---|---|
| Total revenue | Scale | CIM financials, user input |
| Industry growth rate | Growth | CIM industry section, external research |
| Company revenue CAGR | Growth | CIM financials |
| Market opportunity (1-5) | Growth | Qualitative: how early-innings is this market? |
| Recurring revenue % | Revenue Quality | CIM revenue breakdown |
| Gross retention rate (GRR) | Revenue Quality | CIM retention data |
| Top customer concentration % | Revenue Quality | CIM customer data |
| EBITDA margin | Profitability | CIM financials |
| Capex as % of revenue | Profitability | CIM financials |
| Ownership situation fit (qualitative) | Other | CIM overview, user judgment |
| Business model fit (qualitative) | Other | Comparison to thesis archetype |
| Differentiation level (qualitative) | Other | CIM competition section |

If metrics are not available from prior analysis, ask the user to provide them. Present the table and ask: "Which of these can you provide? I'll score what we have and flag the gaps."

## Step 2: Compute Scorecard

For each category, apply proportional scoring:

```
score = ((metric - low_threshold) / (high_threshold - low_threshold)) * max_points
```

- Below low threshold: 0 points
- Above high threshold: full max_points
- Between: proportional

For qualitative measures (market opportunity, ownership fit, business model fit, differentiation): map the qualitative assessment to a percentage within the category range.

## Step 3: Present Results

Output the scorecard as a formatted table:

| Category | Weight | Metric | Score | Max |
|---|---|---|---|---|
| Scale | 7.5% | $Xm revenue | X.X | 7.5 |
| Growth | 30% | X% industry, X% company | X.X | 30 |
| Revenue Quality | 27.5% | X% recurring, X% GRR | X.X | 27.5 |
| Profitability | 15% | X% EBITDA margin | X.X | 15 |
| Other Factors | 20% | ownership, fit, differentiation | X.X | 20 |
| **Total** | **100%** | | **X.X** | **100** |

Below the table, provide a brief narrative:
- Overall fit assessment: **High** (70+) / **Medium** (50-69) / **Low** (<50)
- Strongest and weakest dimensions with one sentence each
- Geographic modifier note if applicable (NYC-area = modest positive bias)

## Step 4: Flag Missing Inputs

List any inputs that were:
- **Missing**: Category unscored, noted as gap
- **Estimated**: Source of estimate stated
- **Qualitative**: Basis for qualitative judgment stated

Recommend specific data to gather to improve scorecard accuracy.

</process>

<success_criteria>
This workflow is complete when:
- [ ] All available metrics gathered from CIM, conversation, or user input
- [ ] Proportional scoring computed correctly for each category
- [ ] Scorecard table presented with clear formatting
- [ ] Fit assessment narrative provided (High/Medium/Low with rationale)
- [ ] Missing or estimated inputs explicitly flagged
- [ ] Recommendations for improving score accuracy provided
</success_criteria>
