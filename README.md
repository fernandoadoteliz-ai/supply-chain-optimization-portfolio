# Supply Chain Optimization Portfolio

Python scripts from my industrial engineering optimization coursework and
independent projects, cleaned up and documented for public reference.
Raw notebooks, reports, and datasets live in a private working repo;
this repo hosts the distilled, runnable models.

## Projects

### [`cemex-transport-inventory-optimization/`](cemex-transport-inventory-optimization)
Two linked models built for CEMEX Mexico West's Guadalajara distribution
operation:
- **`transport_allocation_lp.py`** -- a Gurobi mixed-integer LP that
  allocates CEMEX's own + sub-contracted vehicle fleet across daily
  client orders, cutting weekly transportation trips **225 -> 123
  (-37% cost)** versus the carrier's manual allocation.
- **`inventory_policy_simulation.py`** -- (Q,R) continuous-review and
  (s,T) periodic-review replenishment simulations that sustained a
  **96-98% fill rate at a 90% service level** across the analyzed SKUs.

**Stack:** Python, pandas, Gurobi (MILP), linear programming, inventory theory.

## Notes

- Source datasets are CEMEX-confidential and are not included; each
  script documents the expected input schema so the models can be run
  against comparable data.
- See my [LinkedIn](https://www.linkedin.com/in/fernando-teliz-c/) for project context.
