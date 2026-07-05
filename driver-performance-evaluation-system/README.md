# NextGen Deliveries — Driver Performance Evaluation System

**Course:** IN2004B Generation of Value with Data Analytics, Tecnológico de Monterrey (Team 5) — Aug–Nov 2024
**Client:** NextGen Deliveries, an Amazon Delivery Service Partner (Miami, FL)

> **Privacy note:** the original deliverables ranked 52 real, named drivers and included personal emails for teammates, professors, and the project sponsor. Since permission to publish individually identifiable driver data was not obtained, **this published copy has been anonymized**: driver names/IDs are replaced with `Driver 1`...`Driver 52` (ranking order preserved), personal emails are redacted, and five figures/screenshots that displayed real driver names have been removed and replaced with a note in the text. Everything else — methodology, criteria weights, cluster insights, dashboard description — is unchanged from the original submission. Company-level facts (NextGen, Amazon DSP context) were already public on the author's CV/LinkedIn.

## What's in here

| File | What it is |
|---|---|
| [`Report_DriverPerformanceEvaluationSystem.md`](Report_DriverPerformanceEvaluationSystem.md) | Full written team report: project charter, Balanced Scorecard/Strategic Map diagnosis, KPI selection, the Analytic Hierarchy Process (AHP) used to weight 18 KPIs into a single "Net Score," the resulting driver ranking, cluster analysis, and the Power BI dashboard design. Anonymized as noted above; original diagrams that carried no personal data (criteria weighting tables, radar/cluster charts already labeled `Driver 0`/`25`/`51`, the balanced scorecard) are unchanged. |
| [`Poster_DriverPerformanceEvaluationSystem.md`](Poster_DriverPerformanceEvaluationSystem.md) | Condensed scientific-poster version presented at the program's Expoingeniería showcase. Same anonymization applied to the ranking table. |

## Methodology & results (unchanged from the original)

- **Analytic Hierarchy Process (AHP):** pairwise comparisons with the project sponsor produced criteria weights — 80% Amazon-defined criteria, 20% NextGEN-defined criteria — across 18 KPIs (safety, delivery quality, efficiency/attendance).
- **Ranking:** each of the 52 drivers scored against an "ideal driver" benchmark (MinMax-normalized, negative predictors flipped positive) to produce a single **Net Score**; Week 13 scores ranged from 97.6% (best) to 73.0% (worst).
- **Cluster analysis:** drivers segmented into 3 groups — a small high-safety/low-documentation cluster (3 drivers), a mid-sized efficiency-focused-but-often-late cluster (8 drivers), and the largest, punctuality-strong cluster (41 drivers) — each with distinct improvement recommendations.
- **Dashboard:** a Power BI prototype (driver lookup by ID, per-variable line chart with a driver slicer, top/bottom-3 bar charts) to make the Net Score and its underlying KPIs actionable for NextGen managers.

## What was redacted and why

| Removed | Reason |
|---|---|
| Full driver ranking table (top-5/bottom-5 with real names) | Individually identifiable employee performance data |
| Best/median-driver dashboard mockup showing a real name + driver ID | Same |
| Dashboard "compare drivers" line-chart screenshot (slicer panel listed ~15 real driver names) | Same |
| Two "top 3 / bottom 3 drivers" bar-chart screenshots | Same |
| In-text mentions of the #1, #6, #26 (median), and #52 driver by name | Same — replaced with rank-based references |
| Personal emails for the sponsor, both professors, and all 5 teammates | Personal contact info, not needed for a portfolio reference |
| Appendix D/E links to the sponsor's raw score-card files and the full driver-level spreadsheet | Sponsor-provided confidential data, not covered by any publication permission |
