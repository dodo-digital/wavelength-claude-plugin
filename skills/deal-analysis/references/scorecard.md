# Deal Scorecard

<overview>
Weighted scoring system for evaluating deal fit against the Wavelength Equity investment thesis. Total possible score: 100 points.

Each category has a low threshold (minimum to earn any points) and a high threshold (to earn maximum points). Scoring is proportional between thresholds.

**Scoring formula**: `points = ((metric - low_threshold) / (high_threshold - low_threshold)) * max_points`
- Below low threshold: 0 points
- Above high threshold: full points for category
- Between: proportional
</overview>

<categories>

## Scale (7.5 points)

| Sub-measure | Max Points | Low Threshold | High Threshold | Notes |
|---|---|---|---|---|
| Total revenue | 7.5 | $5M | $65M | Target range. Below $5M scores 0. Consider smaller for high-growth industries. |

## Growth (30 points)

| Sub-measure | Max Points | Low Threshold | High Threshold | Notes |
|---|---|---|---|---|
| Industry growth rate | 10 | 3% | 10%+ | Forward-looking industry growth rate |
| Company revenue CAGR | 12.5 | 5% | 20%+ | Historical company revenue growth |
| Market opportunity | 7.5 | 2 (saturated) | 5 (early innings) | Qualitative 1-5: how early in the market development cycle. Early cell phone insurance in the 90s = 5. Declining saturated market = 1. |

## Revenue Quality (27.5 points)

| Sub-measure | Max Points | Low Threshold | High Threshold | Notes |
|---|---|---|---|---|
| Recurring revenue % | 12.5 | 30% | 85%+ | Percentage of revenue that is contractual or subscription-based |
| Gross retention rate | 10 | 80% | 95%+ | GRR — must be reported separately from NRR |
| Customer concentration | 5 | Top customer >25% | Top customer <10% | Lower concentration = higher score. Inverse scoring. |

## Profitability & Capital Efficiency (15 points)

| Sub-measure | Max Points | Low Threshold | High Threshold | Notes |
|---|---|---|---|---|
| EBITDA margin | 10 | 10% | 25%+ | Adjusted EBITDA margin |
| Capital intensity | 5 | High (>15% capex/rev) | Low (<5% capex/rev) | Lower capex ratio = higher score. Inverse scoring. |

## Other Factors (20 points)

| Sub-measure | Max Points | Low Threshold | High Threshold | Notes |
|---|---|---|---|---|
| Ownership situation fit | 10 | Low fit | High fit | Owner ready to retire, 20-30yr tenure, benefits from liquidity event + incoming operator. Young/energetic owner who seems like the obvious person to keep running it = low fit. |
| Business model fit | 5 | Partial | Strong | How well does this match the target industry archetype? An MSP that is purely project-based install work = partial. An MSP with recurring managed services contracts = strong. |
| Differentiation / mission critical | 5 | Commodity | Highly differentiated | Vertical specialization, switching costs, regulatory advantages. A dental MSP maintaining industry-specific hardware and practice management software = high. A generic break-fix IT shop = low. |

</categories>

<scoring_modifiers>

## Additional Scoring Notes

**Geographic preference**: Companies headquartered in the New York City metro area receive a modest positive bias. This is a thumb on the scale — it should not override fundamentals but may tip a borderline decision.

**Fit assessment tiers**:
- **High fit** (70+ points): Strong candidate, warrants active pursuit
- **Medium fit** (50-69 points): Viable if specific strengths offset gaps
- **Low fit** (<50 points): Pass unless exceptional circumstances

**When inputs are missing**: Score only what's available. Note which categories are unscored and flag them as data gaps. Do not estimate missing inputs without explicit user approval.

**Qualitative scoring**: For ownership fit, business model fit, and differentiation — map the qualitative assessment to a percentage within the category range. A "strong fit" on ownership = ~80-100% of the 10 available points. "Partial fit" = ~40-60%. "Poor fit" = ~0-20%.

</scoring_modifiers>

<thesis_context>

## Investment Thesis Context

**Investor profile**: Traditional search fund (Wavelength Equity) acquiring one platform company. Operator will step in as CEO — "chapter 2 leadership for an exceptional company." Prior operating experience in offshore IT services, based in New York.

**Target company profile**:
- Revenue: $5M–$65M. Will consider down to $2–3M for high-growth industries with sticky revenues (e.g., cybersecurity, vertical SaaS) — rationale: high growth means the company grows into target size within the first year.
- EBITDA: $1M+ floor. Flexible downward if company is growing quickly and has recurring revenue.
- Sticky revenues, ideally contractual recurring / subscription-based.
- Growth in both the industry and the company itself. Key indicators: LTM YoY revenue growth and 3-year CAGR.
- Low capital intensity, strong margins.

**Ideal ownership profile (ICP)**:
- Bootstrapped owner-operator, typically 45–70 years old, seeking to slow down (often retire).
- Seeks liquidity and cares deeply about team, customers, and mission — i.e., legacy matters.
- Ideally has led the company for 10–20+ years and brought it to maturity.
- Wavelength's value prop: competitive offer (liquidity event) bundled with an operator who will carry the burden of leading the company in the next chapter.
- **Red flags**: Owner who is young, energetic, and the obvious choice to keep running the business — they just need a capital partner, not an operator. Wavelength's bid will not stand out. Also skeptical of companies founded 2–3 years ago that aren't yet proven.

**Primary industry focus**: Specialized MSSPs/MSPs with two sub-theses:
- **(A) Vertical specialization** — managed IT for specific verticals (dental IT infrastructure, hospitality, etc.). More defensible than generalist MSPs due to industry-specific hardware/software expertise and switching costs.
- **(B) OT security** — Operational Technology security protecting hardware/software that monitors and controls physical devices (ICS, SCADA, IoT) across manufacturing, energy, and utilities.

Rationale: small, defensible niches. Action plan: significant resource investment (conferences, river guides, deep outreach).

**Secondary industries** (automated high-volume outreach, no conference-level investment):
- Penetration testing — 12% overall growth, 29% for PTaaS. Challenge: too commoditized, moderately prone to agentic AI disruption.
- SOC (Security Operations Centers) — general.
- Fire safety — attractive ICT business model. Challenge: too picked over by private equity. Backing off.
- Technical education / trade schools — thesis: find another deal resembling Fire Tech Productions.
- Vertical SaaS — inspection management.
- Vertical SaaS — construction technology.
- PEOs (Professional Employer Organizations).

Broadly, these industries remain attractive if a strong platform can be acquired at a fair or good price. Will also opportunistically consider opportunities outside target industries.

**Risk factors to avoid**:
- Customer concentration (>20% single customer, >50% top 3, >75% top 5)
- Declining overall market
- Early-stage / unproven business models
- Owners who seem like the obvious choice to keep running the business

</thesis_context>
