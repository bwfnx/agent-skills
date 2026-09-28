# AI Analyst Agent Operational Architecture

Use this reference when a user asks for a rigorous assessment, estimative judgment, scenario forecast, actor motivation analysis, or another complex analytical product.

## Core Posture

- Act as a knowledge engineer, not a passive aggregator.
- Make reasoning auditable through a process trace.
- Treat data as symptoms and judgments as diagnoses.
- Prefer model refinement over simply adding more information.
- Treat anomalies and doubt as high-value signals.

## Mental Model Transparency Checklist

Declare these lenses before final analysis:

| Lens | Questions |
| --- | --- |
| Actor motivation | Am I modeling the actor as a rational actor, culturally situated actor, bureaucratic actor, political survivor, or something else? |
| Government process | What assumptions am I making about hierarchy, stability, factional conflict, decision speed, and institutional norms? |
| Red-side perspective | What does the situation look like from the actor's perceived interest, fear, prestige, constraint, or opportunity? |
| US-expectation trap | Where might familiar US incentives or reactions be misleading? |

## ACH Procedure

1. Identify a full set of mutually exclusive hypotheses.
2. List significant evidence, arguments, and relevant absence of evidence.
3. Construct a matrix comparing evidence against hypotheses.
4. Remove evidence with little diagnostic value.
5. Draw tentative conclusions by rejecting weaker alternatives.
6. Run sensitivity analysis on critical evidence.
7. Report probabilities for every live hypothesis.
8. Identify indicators that would confirm, weaken, or overturn each judgment.

### ACH Matrix Template

| Evidence / Argument | Weight (0-1) | H1 | H2 | H3 | Diagnosticity |
| --- | ---: | --- | --- | --- | --- |
| Evidence A | 0.9 | Inconsistent | Consistent | Consistent | High |
| Evidence B | 0.4 | Consistent | Consistent | Consistent | None / Low |

Use `Consistent`, `Inconsistent`, `Neutral`, or `Not applicable`. Diagnosticity is high when evidence separates hypotheses; it is low when all hypotheses explain the evidence equally well.

## Open-Mind Protocols

| Protocol | Use When | Prompt |
| --- | --- | --- |
| Red-side audit | Actor intent or adversarial incentives matter. | "If I were the actor, what would I believe is in my interest, and where would that diverge from US expectations?" |
| Crystal ball | The lead assumption may be anchoring the analysis. | "Assume the lead assessment is completely false. What plausible scenario explains the evidence?" |
| Thinking backwards | A future outcome needs precursor analysis. | "Assume the unexpected future happened. What had to occur first?" |
| Devil's advocacy | Consensus feels too easy. | "Defend the minority hypothesis using the same evidence." |

## Strategic Judgment Selection

| Method | Best For | Guardrail |
| --- | --- | --- |
| Situational logic | Unique, one-of-a-kind scenarios. | Trace means-ends and cause-effect relationships explicitly. |
| Theory-driven analysis | Long-range forecasting across repeated cases. | State the generalization and why it fits this case. |
| Comparison / analogy | Generating hypotheses or highlighting differences. | Never use analogy as the sole proof of a conclusion. |

## Complexity Rule

If more than seven material variables are active, externalize state before judging. Use a table, matrix, scratchpad, timeline, entity map, or structured notes. This prevents variables from blending together in the context window.

## Bias Catalog

| Bias | Recognition Pattern | Correction |
| --- | --- | --- |
| Vividness bias | One dramatic or anecdotal report drives the assessment. | Prioritize base rates, aggregate evidence, and source reliability. |
| Absence of evidence | Lack of visible evidence is treated as disproof. | Estimate whether evidence should be observable if the hypothesis were true. |
| Mirror-imaging | Familiar values, reactions, or incentives are projected onto others. | Use red-side cultural logic and actor-specific incentives. |
| Anchoring | Current estimate is a minor update to an old estimate. | Re-evaluate from scratch with current evidence. |
| Incrementalism | Gradual change is missed because early impressions persist. | Reassess the full corpus as one fresh body of evidence. |

For long-running topics, trigger a tabula-rasa reset after more than 50 documents or whenever accumulated evidence materially changes the frame.

## Probability Scale

| Qualifier | Probability |
| --- | ---: |
| Almost certain | 93%-100% |
| Probable / likely | 75%-92% |
| Chances are about even | 40%-60% |
| Unlikely / improbable | 20%-39% |
| Remote | 1%-10% |

Avoid unpaired verbal qualifiers such as "probably", "might", "could", "possibly", or "unlikely" unless the number is included.

## Report Template

```markdown
## Bottom Line
[Judgment with numeric probability and brief so-what.]

## Process Trace
- Frame:
- Evidence considered:
- Weighting logic:
- Internal contention:

## Lenses and Assumptions
- Actor model:
- Cultural / institutional logic:
- Red-side view:
- US-expectation risk:

## Competing Hypotheses
| Hypothesis | Probability | Rationale |
| --- | ---: | --- |

## Evidence and Diagnosticity
| Evidence | Weight | H1 | H2 | H3 | Diagnosticity |
| --- | ---: | --- | --- | --- | --- |

## Rejection Logic
[Why weaker hypotheses were downgraded.]

## Anomalies
[Facts that do not fit the lead model.]

## Linchpin Assumptions
[Assumptions that would collapse or materially change the conclusion.]

## Indicators to Watch
| Indicator | Would Support | Would Weaken |
| --- | --- | --- |
```
