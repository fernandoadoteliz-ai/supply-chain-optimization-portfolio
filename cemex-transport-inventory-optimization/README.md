# CEMEX — Transport Allocation & Inventory Optimization

**Course:** IN2009B Supply Chain, Tecnológico de Monterrey (Team 4) — Feb–Jun 2025
**Client:** CEMEX (Guadalajara distribution operation / Tepic plant)

> **Permission note:** CEMEX authorized the publication of the datasets, notebooks, and results in this folder for portfolio/academic-reference purposes.

These are the **original working files as submitted for the course** — Google Colab notebooks with `#@param` widgets, manual per-day/per-product runs, and a team-written report — not a cleaned-up rewrite. Hardcoded Gurobi license credentials have been redacted and replaced with environment-variable reads; nothing else about the logic was changed.

## What's in here

| File | What it is |
|---|---|
| [`notebooks/01_transport_allocation_lp.ipynb`](notebooks/01_transport_allocation_lp.ipynb) | Original Colab notebook: cleans the raw CEMEX order/fleet export and solves a Gurobi mixed-integer LP that assigns every daily client order to a vehicle type/unit/trip (own fleet first, then sub-contracted). **Credentials redacted** — set `GRB_WLSACCESSID`, `GRB_WLSSECRET`, `GRB_LICENSEID` as environment variables to run it yourself against a free [Gurobi WLS license](https://www.gurobi.com/academia/academic-program-and-licenses/). |
| [`notebooks/02_inventory_QR_policy_simulation.ipynb`](notebooks/02_inventory_QR_policy_simulation.ipynb) | Original notebook simulating a continuous-review **(Q,R)** reorder policy against 2024 daily demand for the B/C-class SKUs (per the ABC + Peterson-Silver classification in the report). |
| [`notebooks/03_inventory_ST_policy_simulation.ipynb`](notebooks/03_inventory_ST_policy_simulation.ipynb) | Original notebook simulating a periodic-review **(S,T)** policy for the A-class (high-demand) SKUs. |
| [`report/Phase2_Team4_IN2009B_Report.md`](report/Phase2_Team4_IN2009B_Report.md) | Full written team report (Phase I — transport LP, and Phase II — inventory/SKU analysis): assumptions, model formulation, KPI analysis, and results tables. This is the authoritative source for the numbers below. |
| [`presentations/CEMEX_Phase1_TransportAllocation_Presentation.pdf`](presentations/CEMEX_Phase1_TransportAllocation_Presentation.pdf) | Team slide deck presented for Phase I (transport allocation). |
| [`presentations/CEMEX_Phase2_InventoryManagement_Presentation.pdf`](presentations/CEMEX_Phase2_InventoryManagement_Presentation.pdf) | Team slide deck presented for Phase II (inventory management). |
| [`data/CEMEX_TransportOrders_VehicleFleet_Dec2024.xlsx`](data/CEMEX_TransportOrders_VehicleFleet_Dec2024.xlsx) | Real CEMEX order book (Dec 9–14, 2024) and vehicle-fleet parameters used by `01_transport_allocation_lp.ipynb`. Published with CEMEX's permission. |
| [`data/CEMEX_SKU_InventoryDemand_2024.csv`](data/CEMEX_SKU_InventoryDemand_2024.csv) | Real 2024 daily inventory/demand history per SKU, used by the two inventory notebooks. Published with CEMEX's permission. |

## Results (verified against the team report)

**Transport allocation (Dec 9–14, 2024 order book):**
- Total transportation cost cut **37%**: 748,460 MXN (current, manual allocation) → 469,490 MXN (LP-optimized), with daily reductions ranging 28%–49%.
- The current operation logged 225 vehicle-trip legs across that week; the model consistently dropped *Trucks* from the fleet mix in favor of higher-capacity *Tortons* and *Trailers*, which cut both trip count and cost.
- Key assumptions: real cargo capacity assumed 2% above nameplate; sub-contracted fleet costs 25% more than owned fleet; no backorders; whole-day demand known in advance. Full assumption list in the report.

**Inventory policy (Tepic plant, 9 SKUs, ABC + Peterson-Silver classified):**
- 2 category-A SKUs on a periodic-review (S,T) policy: 96.1–96.7% fill rate at a 90% target service level.
- 7 category-B/C SKUs on a continuous-review (Q,R) policy: 98.3–99.6% fill rate at a 90% target service level.
- Right-sizing safety stock/reorder points against the recommended policies identified an estimated **MXN 3.16 million** in inventory cost savings across the 9 SKUs (Table 6 in the report).

## Limitations (from the report's own notes)

The team's model assumptions don't perfectly match CEMEX's actual operation (e.g., observed Torton loads exceeded the modeled capacity limit on at least one trip; whether a vehicle was CEMEX-owned or sub-contracted wasn't always known from the raw data). The report treats these as documented limitations, not hidden ones — see "Notes for the Proposed Model" in the report for the full list.
