# CEMEX Mexico West -- Transport & Inventory Optimization

Two models built during an industrial engineering supply-chain course
project, applied to CEMEX Mexico West's Guadalajara distribution
operation (Dec 2024 order book, 225 daily orders across 6 days).

## `transport_allocation_lp.py`
Mixed-integer linear program (Gurobi) that assigns every client order
to a vehicle type, fleet unit, and trip -- own fleet first, then
sub-contracted -- minimizing fixed + variable transport cost subject
to fleet size, daily trip count, daily km, and local (<=30km) vs.
external cargo-capacity limits.

**Result:** weekly trips cut from 225 to 123 (-37% transport cost)
vs. the carrier's manual allocation.

Requires a Gurobi license (WLS credentials via env vars `GRB_WLSACCESSID`,
`GRB_WLSSECRET`, `GRB_LICENSEID`) and the CEMEX order/fleet Excel exports
(not included -- confidential).

## `inventory_policy_simulation.py`
Simulates (Q,R) continuous-review and (s,T) periodic-review
replenishment policies against 2024 daily demand history, to size
reorder quantities/points and review intervals per SKU.

**Result:** 96-98% fill rate sustained at a 90% service level across
the simulated SKUs.

Requires a CSV with `Date`, `Inventario`, `Demanda`, and (for the
continuous-review model) `Abasto_Transito` columns (not included --
confidential).
