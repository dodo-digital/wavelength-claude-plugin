# Workflow: Generate Investment Memo

<required_reading>
**Read these reference files NOW:**
1. references/memo-format.md
2. references/scorecard.md
3. templates/memo-template.md
</required_reading>

<process>

## Step 1: Receive Input

User provides one or more of:
- CIM PDF file path
- Company documents (financials, marketing materials, etc.)
- Company description or information shared in conversation

Confirm the file(s) exist with the Read tool. For PDFs, read and confirm page count.

If no documents provided, ask: "Can you share the CIM or company documents? You can provide a file path or paste key information directly."

## Step 2: Determine Scope

**Full memo** (default): Generate complete OA memo with all sections.
**Section-level**: Generate only the specific section(s) requested.

If user specifies sections (e.g., "just do the market overview" or "generate the financial summary"), proceed with only those.

If user uploads a CIM without specifying, generate full memo.

### Section-to-Agent Mapping

| OA Memo Section | Sub-Agent Reference | Notes |
|---|---|---|
| Header | None | Extract metadata from CIM directly |
| Executive Summary | None | Synthesize from CIM overview |
| Company Overview (General, Service, Demand Drivers) | `references/mission-criticality.md` | For demand drivers / mission criticality sub-section |
| Clients / Revenue Quality / Contract Structure | `references/revenue-quality.md` | Wasserstein ladder, retention, concentration |
| Management / Team / Operations | None | Extract from CIM directly |
| Financial Summary | `references/financial-analysis.md` | P&L focus, 3-5yr historical + projections |
| Market Overview & Competitive Landscape | `references/industry-analysis.md` + `references/right-to-win.md` | Combined section — deploy both agents |
| Wavelength Scorecard | `references/scorecard.md` | Computed from gathered data |
| Thesis | `references/value-creation.md` | Reframe as investment thesis / angle |
| Deal Killers / Risk & Mitigants | `references/risk-assessment.md` | Prioritized DKs with mitigants + tests |
| Next Steps | `references/missing-items.md` | Data gaps become action items |

## Step 3: Deploy Sub-Agents

**For full memo**: Deploy analysis sub-agents in parallel using the Task tool (`subagent_type: "general-purpose"`).

For each agent:
1. Read the reference file for that analysis dimension
2. Spawn a Task agent with:
   - The reference file content as the agent's instructions
   - The CIM file path so the agent can read it directly
   - Prompt: "Read the CIM at [path] and produce the analysis described in your instructions. Return structured findings with page citations [p. X]."

Deploy these agents in parallel:
- **revenue-quality** agent
- **financial-analysis** agent
- **industry-analysis** agent
- **right-to-win** agent
- **mission-criticality** agent
- **value-creation** agent
- **risk-assessment** agent
- **missing-items** agent

**For section-level**: Deploy only the sub-agents mapped to the requested sections.

**Header, Executive Summary, Company Overview (General + Service Offering), and Management/Team** do not require sub-agents. Extract these directly from the CIM yourself.

## Step 4: Compute Scorecard

After sub-agents return, compute the weighted scorecard per `references/scorecard.md` using financial and qualitative data gathered. Score only what's available — flag gaps.

## Step 5: Draft Thesis

Using the value-creation agent's output, draft the **Thesis** section. This is NOT generic "value creation levers." It must answer: *How exactly will Wavelength make this a great acquisition with strong investor returns? What is the specific angle?*

Reference the thesis examples in `references/memo-format.md` for tone and specificity.

## Step 6: Synthesize into Memo Format

Compose the memo following `templates/memo-template.md`.

**Synthesis rules:**
- Synthesize agent outputs into flowing narrative — do not concatenate
- Follow the exact OA section order from the template
- Include the 4-column header metadata table
- Page citations preserved: `[p. X]`
- Missing data noted as "Not disclosed"
- Financial Summary uses P&L table format with historical years
- Deal Killers prioritized by importance, with mitigant and test sub-bullets
- Conversational PE professional voice

### Length Guidelines
- Screening memo: 4-5 pages (~2000-2500 words)
- Active diligence memo: 8-10 pages (~4000-5000 words)
- Default to screening unless user specifies otherwise

## Step 7: Present and Iterate

Present the memo. Then ask:

"Here's the [full/section] memo. Want me to:
- Expand any section?
- Adjust the analysis or thesis?
- Generate additional sections?
- Switch to explore mode to dig into specific aspects?"

The memo is a living document. New information updates affected sections while preserving the rest.

</process>

<success_criteria>
This workflow is complete when:
- [ ] CIM or company docs ingested and confirmed readable
- [ ] Relevant sub-agents deployed and returned findings
- [ ] Scorecard computed with available data
- [ ] Thesis drafted with specific investment angle
- [ ] Memo synthesized in OA format with header table, correct section order
- [ ] All claims have page citations where applicable
- [ ] Missing data explicitly noted
- [ ] Deal Killers prioritized with mitigants and tests
- [ ] Memo presented to user with iteration options
</success_criteria>
