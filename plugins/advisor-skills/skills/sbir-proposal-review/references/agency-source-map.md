# Agency Source Map

Where to look up live rules, per agency. **URLs and structures below are entry points, not facts.** Program offices, portals, and solicitation numbering all change — several have changed recently. Follow the links, read what's actually there now, and believe the live solicitation over anything written here.

---

## Identifying the agency

| Signal | Agency |
|---|---|
| PA-/PAR-/RFA- number, ASSIST, eRA Commons, SciENcv, "Specific Aims," "Research Strategy," study section, institute names (NIDDK, NCI, NHLBI) | **NIH / HHS** |
| Topic number like `DON26BZ04-NV066`, DSIP, "Volume 1–6," BAA, component names (Army, Navy, AFWERX, DARPA, MDA, SOCOM), "Technical Volume," "Cost Volume" | **DoD** (now also labeled "Department of War"/DOW on sbir.gov) |
| NSF 26-XXX, Research.gov, "Project Pitch," "Intellectual Merit," "Broader Impacts," "Project Description" | **NSF** |
| ConnectWerx, AMP, PAMS (legacy), DE-FOA-XXXXXXX (legacy), topic/subtopic + TPOC | **DOE** |
| NSPIRES, subtopic numbering like H6.22 | **NASA** |
| NIFA, "Grants.gov workspace," USDA topic areas 8.1–8.13 | **USDA** |
| Contract solicitation with a named "Topic" and a technical POC, no research-plan structure | Likely **DHS, DOT, EPA, ED, or Commerce** — all SBIR-only, all contracts except Commerce |

Also note the award instrument. **Contracts** (DoD, NASA, DHS, DOT, EPA, ED, some NIH) mean FAR rules, binding deliverables, cost realism review, and a defined Phase III sole-source path. **Grants** (NIH mostly, NSF, DOE, USDA, Commerce) mean assistance instruments, more technical latitude, and 2 CFR 200 cost principles. Applicants who write a grant-style narrative for a contract solicitation get marked down for it.

---

## Government-wide (check for every review)

| What | Where |
|---|---|
| Participating agencies, which run STTR, award instruments | `sbir.gov/participating-agencies` |
| Current Phase I / Phase II statutory guideline dollar amounts | `sbir.gov/about` — SBA adjusts annually for inflation |
| SBA SBIR/STTR Policy Directive (governs all agencies) | `sbir.gov/about/policies` |
| Performance benchmarks — can bar an experienced firm from submitting for a year | `sbir.gov/performance-benchmarks` |
| Foreign disclosure requirements | `sbir.gov/foreign_disclosures` |
| Company registry / SBC Control ID | `app.www.sbir.gov/company-registration/overview` |
| Statutory text when the Policy Directive lags a new law | `govinfo.gov` — search the public law number. **congress.gov blocks automated fetching; use govinfo instead.** |

⚠️ **Known stale trap:** the SBA Policy Directive is revised infrequently and can lag new legislation by a year or more. When statute and Directive conflict, statute controls. Check whether a reauthorization or amendment has passed since the Directive's date.

⚠️ **Known stale trap:** `sbir.gov/tutorials/agency-solicitations/<AGENCY>` and `sbir.gov/tutorials/individual-agency-requirements/<AGENCY>` pages have been observed carrying award amounts and process descriptions years out of date, including descriptions of processes an agency has since eliminated. **Do not cite these pages.** Use them only as a pointer to the agency's own site.

---

## NIH / HHS

| What | Where |
|---|---|
| The solicitation | `grants.nih.gov/grants/guide/pa-files/<NUMBER>.html` |
| Parent announcements table | `grants.nih.gov/funding/explore-nih-opportunities/parent-announcements` |
| Small business program hub | `seed.nih.gov` — especially the funding opportunities and eligibility pages |
| Policy notices (the thing applicants miss) | `grants.nih.gov/grants/guide/notice-files/NOT-OD-<YY>-<NNN>.html`; search `grants.nih.gov` and `nexus.od.nih.gov` |
| Page limits table | Search `grants.nih.gov` for the table of page limits — solicitations usually defer to it and supersede it where they differ |
| Grants Policy Statement | `grants.nih.gov/grants/policy/nihgps/` |
| Clinical trial policy | See `nih-clinical-trials.md` |

**URL fallback order when the canonical pa-files URL 404s** (common for recently issued announcements):
1. `seed.nih.gov` funding opportunities list — reliable for confirming the current parent announcements and their clinical-trial designations
2. The parent announcements table
3. `simpler.grants.gov/opportunity/<ID>` — the grants.gov record; its full-announcement attachment on `files.simpler.grants.gov` often serves the complete HTML when grants.nih.gov will not
4. Search grants.gov by announcement number to find the opportunity ID

Watch for **"Revised"** in an attachment filename — the amendment governs.

**Highest-yield things to verify at NIH:** current biosketch and Other Support format (format changes here produce submission-blocking errors, not warnings), whether SciENcv and ORCID are mandatory, forms version, late-submission eligibility for the mechanism, per-PI and per-company application caps, which review framework applies to the activity code, whether a Data Management and Sharing Plan is required for that specific announcement.

---

## DoD

| What | Where |
|---|---|
| Portal and current BAAs | `dodsbirsttr.mil` (DSIP) |
| Opportunities overview and release calendar | `defensesbirsttr.mil/SBIR-STTR/Opportunities/` |
| Foreign Risk Evaluation program documents | `defensesbirsttr.mil` — search for the Foreign Risk Evaluation Common Decision Matrix |
| Component instructions — **read in addition to the DoD-wide BAA** | Navy `navysbir.com` · Army `armysbir.army.mil` and `xtech.army.mil` · Air Force `afwerx.com/get-funded` · DARPA `darpa.mil` small business pages |

**DoD is a layered read.** The DoD-wide BAA preface plus the component's own instructions plus the topic itself. Component instructions override on page limits, award amounts, period of performance, and sometimes criteria weighting. Reviewing against only the DoD-wide document will miss the rules that actually reject proposals.

⚠️ **Access note:** `dodsbirsttr.mil` blocks automated fetching via robots.txt and may be unreachable. When it is, component sites (`navysbir.com` especially) republish the current instructions and are usually reachable. Say which source you used.

**Structural things to verify:** the current release calendar and which release is open, the topic Q&A window and its cutoff, the volume structure and per-component page limits, the exact evaluation criteria and their stated order of importance, component-specific award ceilings and period of performance, whether the topic is conventional Phase I or Direct to Phase II.

**Rejection mechanics worth checking every time:** proposal left in a non-submitted status at deadline, missing foreign-disclosure attachment, undisclosed organizational conflict of interest, page limit exceeded, period of performance not matching the exact required length, cost volume exceeding base or option ceilings, work-percentage below threshold, encrypted or password-protected files, not certified by the corporate official before close.

---

## NSF

| What | Where |
|---|---|
| Program hub | `seedfund.nsf.gov` |
| Current solicitation | `nsf.gov/funding/opportunities/` — find the current SBIR/STTR solicitation number |
| Project Pitch requirements and limits | `seedfund.nsf.gov/project-pitch/` |
| Deadlines and transition rules | `seedfund.nsf.gov/solicitations/` and `seedfund.nsf.gov/critical-information/` |
| Merit review criteria | `seedfund.nsf.gov/solicitation-merit-review/` |
| Page limits by section | `seedfund.nsf.gov/solicitation-project-description/` and `/solicitation-documents/` |
| Formatting rules (return without review) | `nsf.gov/policies/pappg/` — PAPPG proposal preparation section |
| Topic list and scope exclusions | `seedfund.nsf.gov` topics document |

**Check first:** whether the applicant has a **valid, unexpired Project Pitch invitation**. NSF reviews only invited proposals, invitations expire after a defined number of deadlines, and there are caps on pitches per company and per project. No valid invitation means there is no proposal to review — surface this before anything else.

**Also check:** NSF publishes explicit scope exclusions (categories of work it will not fund at all). A proposal in an excluded category is returned regardless of quality. And `seedfund.nsf.gov` hosts static PDFs that have been observed contradicting the live solicitation on award amounts — prefer live pages.

---

## DOE

| What | Where |
|---|---|
| Program home | `energy.gov/technologycommercialization` — SBIR/STTR pages |
| Current opportunities and portal | `sbir-sttr.connectwerx.org` |
| Required registrations | `energy.gov/technologycommercialization/required-sbirsttr-registrations` |
| Security risk management / due diligence | `energy.gov/technologycommercialization/security-risk-management-sbirsttr` |

⚠️ **Known stale trap, severe.** DOE restructured this program — moving it out of the Office of Science, changing portals, and eliminating a previously mandatory pre-application step. `science.osti.gov/sbir/FAQs` and the sbir.gov DOE tutorial have been observed still instructing applicants to use the retired portal and submit the retired pre-application, **with no disclaimer**. Both are official sources and both are wrong. Verify DOE's current process from `energy.gov` and the live opportunity page only.

⚠️ **Naming collision.** DOE runs themed initiatives that appear under both SBIR/STTR and separate Office of Science funding announcements with unrelated eligibility, dollar amounts, and portals. Confirm the opportunity is the SBIR/STTR one before advising on it.

**Verify each time:** whether a pitch or pre-application stage is currently required and its deadline relative to the full application, whether applications must map to a specific topic and subtopic, whether contacting a technical point of contact is required or merely advised, the current merit review criteria and whether they are equally or differentially weighted, award ceilings and period of performance.

---

## NASA, USDA, and the SBIR-only agencies

| Agency | Entry point | Notes |
|---|---|---|
| NASA | `sbir.nasa.gov`, portal NSPIRES | Contracts; subtopic-bound |
| USDA | `nifa.usda.gov` SBIR pages | Grants; broad topic areas; combined SBIR/STTR RFA |
| DHS | `dhs.gov/science-and-technology/sbir` | Contracts, SBIR only |
| DOT | `volpe.dot.gov` SBIR pages | Contracts, SBIR only |
| EPA | `epa.gov/sbir` | Contracts, SBIR only |
| Education | `ies.ed.gov/sbir` | Contracts, SBIR only |
| Commerce (NIST/NOAA) | `nist.gov/tpo/small-business-innovation-research-program` and `techpartnerships.noaa.gov` | Grants, SBIR only |

For these, go to the agency's own program page and find the current solicitation. Do not rely on aggregator summaries.

---

## Recording what you couldn't verify

Keep a running list of anything you could not confirm — a solicitation served only from a mirror, a page limit stated differently in two places, a requirement that appears changed but whose notice you could not find, a portal you could not reach.

Surface it in the deliverable and tell the applicant to confirm those specific items with the program officer or technical point of contact. That contact is normal and expected; applicants are often reluctant to make it and shouldn't be.
