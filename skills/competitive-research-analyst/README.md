# Competitive Research Analyst

Version: v1.0

## Purpose

This skill helps small business owners, advisors, and consultants generate structured competitive intelligence from a short business description and optional uploaded materials.

It is designed for repeatable tasks such as:
- competitor analysis
- market trend review
- pricing comparison
- positioning advice
- benchmark snapshots
- swot analysis
- document-informed market assessment

## Typical inputs

- short description of the business
- industry and niche
- target customers
- competitors the user already knows
- uploaded business plan, business model canvas, market report, or competitor notes

## Typical outputs

- concise strategic brief
- market trends summary
- competitive landscape analysis
- pricing and revenue insights
- benchmark comparison
- competitor swot
- prioritized next steps

## Design choices

This skill is web-first for competitor analysis. Current competitor facts should be gathered from public sources at runtime rather than assumed from background knowledge.

The skill is intentionally lightweight:
- minimal-friction intake
- dynamic follow-up questions
- document-aware synthesis
- mandatory osint-style web research for competitor findings
- structured outputs
- emphasis on practical next steps

## Recommended future enhancements

- add a reference file with industry-specific osint checklists
- add a reference file with benchmark templates for common business types
- add consultant-ready output templates for client-facing briefs
- add a reusable competitor monitoring workflow or alert template
