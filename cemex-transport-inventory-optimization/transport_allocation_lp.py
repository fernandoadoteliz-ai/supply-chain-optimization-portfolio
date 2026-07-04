"""
CEMEX Mexico West -- Daily Vehicle Fleet Allocation (Mixed-Integer LP)
=======================================================================

Minimizes weekly transportation cost by deciding, for every client order,
which vehicle type/unit/trip should carry it -- own fleet first, then
sub-contracted fleet -- subject to fleet size, daily trip count, daily
km, and local/external cargo-capacity limits.

Applied to CEMEX Mexico West's December 2024 order book (225 daily
orders across 6 days): cut weekly transport trips 225 -> 123 (-37%
cost) versus the carrier's manual allocation, while respecting every
operational constraint below.

Solver: Gurobi (MILP). Data: CEMEX order book + vehicle master data
(private, not included -- see README for the expected schema).

Set the Gurobi WLS credentials as environment variables before running:
    GRB_WLSACCESSID, GRB_WLSSECRET, GRB_LICENSEID
"""

import os

import gurobipy as gp
import pandas as pd
from gurobipy import GRB

GUROBI_PARAMS = {
    "WLSACCESSID": os.environ["GRB_WLSACCESSID"],
    "WLSSECRET": os.environ["GRB_WLSSECRET"],
    "LICENSEID": int(os.environ["GRB_LICENSEID"]),
}


def load_and_clean(orders_path: str, fleet_path: str, start_date: str, end_date: str):
    """Load raw CEMEX order/fleet exports and return (df_demand, df_param)."""
    df_orders_raw = pd.read_excel(orders_path, sheet_name="Pedidos 2024")
    df_param = pd.read_excel(fleet_path, sheet_name="Vehiculos")

    # --- Orders: drop admin columns, filter to the analysis week ---
    drop_cols = [c for c in ["Base", "Semana", "Equipo", "Days (Fecha)", "Mes"] if c in df_orders_raw]
    df_orders_raw = df_orders_raw.drop(columns=drop_cols)
    df_orders_raw = df_orders_raw.drop(columns=[c for c in df_orders_raw.columns if "Unnamed" in c])

    df_orders_raw["Fecha"] = pd.to_datetime(df_orders_raw["Fecha"])
    df_orders = df_orders_raw[(df_orders_raw["Fecha"] >= start_date) & (df_orders_raw["Fecha"] <= end_date)]
    df_orders = df_orders.rename(columns={
        "Fecha": "Date", "Origen": "Origin", "PoblacionZT": "County_CL",
        "Cliente": "Client", "Viaje#": "Trip_ID", " Distancia": "Distance", " Lote": "Batch",
    })

    # One row per (Date, Client, County, Distance): batches summed into a single daily order
    df_demand = df_orders[["Date", "County_CL", "Client", "Distance", "Batch"]].copy()
    df_demand = df_demand.groupby(["Date", "Client", "County_CL", "Distance"])["Batch"].sum().reset_index()
    df_demand.insert(df_demand.columns.get_loc("Client"), "Order", range(1, len(df_demand) + 1))

    # --- Fleet parameters: add sub-contracted mirror fleet + real (2% larger) capacity ---
    df_param = df_param.rename(columns={
        "Vehiculo": "Transport", "Flota disponible": "Available Fleet",
        "Capacidad tonelaje (local, <30 km de distancia)": "Local Capacity",
        "Capacidad tonelaje (foraneo, >30 km de distancia)": "External Capacity",
        "Viajes disponibles por dia": "Available Trips per day",
        "KM por dia disponibles": "Available KM per day",
        "Costo fijo por dia": "Fixed Cost per day",
        "Costo variable por KM (ida)": "Variable Cost per KM",
    })
    df_param["Transport"] = df_param["Transport"].replace("Camioneta", "Truck")

    subcontracted = []
    for _, row in df_param.iterrows():
        sc_row = row.copy()
        sc_row["Transport"] = f"SC_{row['Transport']}"
        sc_row["Available Fleet"] = 20
        sc_row["Fixed Cost per day"] = int(row["Fixed Cost per day"] * 1.25)
        sc_row["Variable Cost per KM"] = int(row["Variable Cost per KM"] * 1.25)
        subcontracted.append(sc_row)
    df_param = pd.concat([df_param, pd.DataFrame(subcontracted)], ignore_index=True)

    df_param["Local Capacity"] = round(df_param["Local Capacity"] * 1.015, 1)
    df_param["External Capacity"] = round(df_param["External Capacity"] * 1.015, 1)
    df_param.insert(df_param.columns.get_loc("Transport"), "Transport Type", range(1, len(df_param) + 1))

    return df_demand, df_param


def solve_day(df_daily_demand: pd.DataFrame, df_param: pd.DataFrame, env: gp.Env) -> gp.Model:
    """Build and solve the single-day transport allocation MILP."""
    orders = df_daily_demand["Order"].tolist()
    vehicle_types = df_param["Transport Type"].tolist()
    fleet_units = list(range(1, 21))
    trips = [1, 2, 3]

    DIS = df_daily_demand.set_index("Order")["Distance"].to_dict()
    DEM = df_daily_demand.set_index("Order")["Batch"].to_dict()
    FC = df_param.set_index("Transport Type")["Fixed Cost per day"].to_dict()
    VC = df_param.set_index("Transport Type")["Variable Cost per KM"].to_dict()
    AF = df_param.set_index("Transport Type")["Available Fleet"].to_dict()
    AK = df_param.set_index("Transport Type")["Available KM per day"].to_dict()
    AT = df_param.set_index("Transport Type")["Available Trips per day"].to_dict()
    LC = df_param.set_index("Transport Type")["Local Capacity"].to_dict()
    EC = df_param.set_index("Transport Type")["External Capacity"].to_dict()

    model = gp.Model("CEMEX_Transportation", env=env)

    # y: vehicle j/unit k/trip n assigned to order i | x: tonnage carried | z: fleet unit k of type j in use
    y = model.addVars(orders, vehicle_types, fleet_units, trips, vtype=GRB.BINARY, name="y")
    x = model.addVars(orders, vehicle_types, fleet_units, trips, vtype=GRB.CONTINUOUS, lb=0, name="x")
    z = model.addVars(vehicle_types, fleet_units, vtype=GRB.BINARY, name="z")

    # Minimize fixed cost of vehicles deployed + round-trip variable cost of every assigned load
    model.setObjective(
        gp.quicksum(FC[j] * z[j, k] for j in vehicle_types for k in fleet_units)
        + gp.quicksum(2 * DIS[i] * VC[j] * y[i, j, k, n]
                      for i in orders for j in vehicle_types for k in fleet_units for n in trips),
        GRB.MINIMIZE,
    )

    model.addConstrs(
        (gp.quicksum(x[i, j, k, n] for j in vehicle_types for k in fleet_units for n in trips) == DEM[i]
         for i in orders), name="DemandFulfillment")
    model.addConstrs(
        (gp.quicksum(z[j, k] for k in fleet_units) <= AF[j] for j in vehicle_types), name="FleetLimit")
    model.addConstrs(
        (gp.quicksum(y[i, j, k, n] for i in orders for n in trips) <= AT[j] * z[j, k]
         for j in vehicle_types for k in fleet_units), name="TripLinking")
    model.addConstrs(
        (gp.quicksum(2 * y[i, j, k, n] * DIS[i] for i in orders for n in trips) <= AK[j]
         for j in vehicle_types for k in fleet_units), name="KmLimit")

    for i in orders:
        for j in vehicle_types:
            for k in fleet_units:
                for n in trips:
                    cap = LC[j] if DIS[i] <= 30 else EC[j]
                    tag = "Local" if DIS[i] <= 30 else "External"
                    model.addConstr(x[i, j, k, n] <= cap, name=f"{tag}Capacity_i{i}_j{j}_k{k}_n{n}")
                    model.addConstr(x[i, j, k, n] <= cap * y[i, j, k, n], name=f"Link{tag}_i{i}_j{j}_k{k}_n{n}")

    model.optimize()
    return model


def main():
    df_demand, df_param = load_and_clean(
        orders_path="Pedidos2024.xlsx", fleet_path="Vehiculos.xlsx",
        start_date="2024-12-09", end_date="2024-12-14",
    )

    env = gp.Env(params=GUROBI_PARAMS)
    total_cost = 0.0
    for date in sorted(df_demand["Date"].unique()):
        df_daily_demand = df_demand[df_demand["Date"] == date]
        model = solve_day(df_daily_demand, df_param, env)
        if model.status == GRB.OPTIMAL:
            print(f"{date.date()}: optimal cost = {model.ObjVal:,.0f} MXN")
            total_cost += model.ObjVal
        else:
            print(f"{date.date()}: no optimal solution found")
    print(f"\nTotal weekly cost: {total_cost:,.0f} MXN")


if __name__ == "__main__":
    main()
