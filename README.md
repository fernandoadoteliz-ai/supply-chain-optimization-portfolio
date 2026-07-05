# Supply Chain & Operations Analytics Portfolio

Fernando Teliz Colchado — Industrial & Systems Engineering student (Tecnológico de Monterrey / Hochschule Reutlingen exchange).

This repository holds the **original, as-submitted materials** (notebooks, team reports, presentations) from two real-client academic projects, so a reviewer can see the actual work rather than a polished rewrite. Each project folder has its own README labeling every file.

## Projects

### [`cemex-transport-inventory-optimization/`](cemex-transport-inventory-optimization)
Two linked models built for **CEMEX** (Guadalajara distribution / Tepic plant), IN2009B Supply Chain course, Tecnológico de Monterrey, Feb–Jun 2025:
- A Gurobi mixed-integer LP reallocating CEMEX's own + sub-contracted vehicle fleet, cutting weekly transport cost **37%** (748,460 → 469,490 MXN) over the analyzed order week.
- ABC-classified (Q,R) / (S,T) inventory review policies for 9 SKUs, sustaining **96.1–99.6% fill rates** at a 90% target service level.

> **CEMEX data note:** CEMEX granted permission to publish the datasets, notebooks, and results in this repository for portfolio purposes.

### [`driver-performance-evaluation-system/`](driver-performance-evaluation-system)
A multi-criteria driver-ranking and clustering system built for **NextGen Deliveries** (an Amazon Delivery Service Partner, Miami FL), IN2004B Data Analytics course, Tecnológico de Monterrey, Aug–Nov 2024. Ranked 52 drivers across 18 KPIs using the Analytic Hierarchy Process and segmented them into 3 performance tiers via clustering.

> **Privacy note:** individual driver names, IDs, and personal contact emails have been anonymized/redacted in the published copy (see that folder's README for details). Company-level information (NextGen, Amazon DSP context) was already public on the author's CV/LinkedIn.

## Notes

- These are course deliverables, not products: expect Colab-notebook rough edges (`#@param` widgets, manual re-runs per day/product) rather than production code.
- See my [LinkedIn](https://www.linkedin.com/in/fernando-teliz-c/) for project context.
