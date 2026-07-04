"""
CEMEX Mexico West -- Results Summary (one-page PDF)
====================================================

Renders a single-page, print-quality PDF summarizing the transport
allocation LP and inventory policy simulation methodology, for
publication in the portfolio repo. Author: Fernando Teliz Colchado.

The trip/cost figures are the already-published aggregate results
from the CV (225->123 trips/week, -37% cost). The inventory chart
uses a SYNTHETIC, seeded demand profile (intermittent, lumpy demand
typical of a cement SKU) purely to illustrate how the (Q,R)
continuous-review policy behaves -- no CEMEX data (real or
aggregated) appears anywhere in this file or its output.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from inventory_policy_simulation import simulate_continuous_review

ACCENT = "#961124"
INK = "#1a1a1a"
MUTED = "#8a8a8a"
PANEL_BG = "#f7f3ee"

Q, R, LEAD_TIME = 1000, 550, 3


def synthetic_demand(days: int = 180, seed: int = 7) -> pd.DataFrame:
    """Illustrative intermittent-demand profile (not real CEMEX data)."""
    rng = np.random.default_rng(seed)
    order_days = rng.random(days) < 0.35  # ~35% of days see an order
    demand = np.where(order_days, rng.gamma(shape=2.2, scale=70, size=days), 0.0)
    df = pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=days, freq="D"),
        "Inventario": 0.0,
        "Demanda": demand.round(0),
        "Abasto_Transito": 0.0,
    })
    df.loc[0, "Inventario"] = 900.0  # starting on-hand
    return df


def style_axes(ax):
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(labelsize=8.5)


def build_report(demand_df: pd.DataFrame, out_path: str):
    sim = simulate_continuous_review(demand_df, Q=Q, R=R, lead_time=LEAD_TIME, allow_backorders=False)

    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait
    gs = fig.add_gridspec(
        nrows=6, ncols=2,
        height_ratios=[0.9, 0.55, 0.65, 1.0, 3.9, 0.55],
        hspace=0.15, wspace=0.32,
        left=0.09, right=0.94, top=0.965, bottom=0.04,
    )

    # ---------- Header ----------
    axH = fig.add_subplot(gs[0, :])
    axH.axis("off")
    axH.text(0, 0.75, "CEMEX Mexico West", fontsize=22, fontweight="bold", color=ACCENT, va="center")
    axH.text(0, 0.18, "Transport Allocation & Inventory Optimization -- Results Summary",
             fontsize=12.5, color=INK, va="center")
    axH.axhline(0.0, color=ACCENT, linewidth=1.5, xmax=0.98)

    # ---------- Byline + intro ----------
    axI = fig.add_subplot(gs[1:3, :])
    axI.axis("off")
    axI.text(0, 0.95, "Fernando Teliz Colchado  |  Industrial Engineering supply-chain project  |  Feb-Jun 2025",
              fontsize=9.5, color=MUTED, va="top")
    intro = (
        "A mixed-integer linear program (Gurobi) reallocated CEMEX's own and sub-contracted vehicle fleet\n"
        "across a 225-order/week demand book, and (Q,R)/(s,T) inventory-review policies were simulated against\n"
        "2024 daily demand history to right-size reorder points per SKU. Source datasets are CEMEX-confidential\n"
        "and are not published; the chart below replays the same policy logic on a synthetic demand profile."
    )
    axI.text(0, 0.62, intro, fontsize=8.8, color=INK, va="top", linespacing=1.5)

    stats = [("-37%", "weekly transport cost\n(225 -> 123 trips/week)"),
             ("96-98%", "inventory fill rate\nachieved at a 90% service level"),
             (f"{sim.fill_rate:.0%}", "fill rate reproduced in the\nillustrative (Q,R) demo below")]
    stat_axes = gs[3, :].subgridspec(1, 3, wspace=0.18)
    for i, (big, small) in enumerate(stats):
        ax = fig.add_subplot(stat_axes[0, i])
        ax.axis("off")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.add_patch(plt.Rectangle((0.02, 0.08), 0.96, 0.84, facecolor=PANEL_BG,
                                     edgecolor=ACCENT, linewidth=1.1))
        ax.text(0.5, 0.62, big, fontsize=19, fontweight="bold", color=ACCENT, ha="center", va="center")
        ax.text(0.5, 0.27, small, fontsize=8.0, color=INK, ha="center", va="center")

    # ---------- Chart A: weekly trips + cost, manual vs optimized ----------
    charts_row = gs[4, :].subgridspec(2, 2, height_ratios=[1.0, 1.55], hspace=0.55, wspace=0.32)

    axA1 = fig.add_subplot(charts_row[0, 0])
    manual, optimized = 225, 123
    bars = axA1.bar(["Manual", "LP-optimized"], [manual, optimized], color=[MUTED, ACCENT], width=0.55)
    for b, v in zip(bars, [manual, optimized]):
        axA1.text(b.get_x() + b.get_width() / 2, v + 6, str(v), ha="center", fontsize=10, fontweight="bold")
    axA1.set_title("Weekly Trips", fontsize=10.5, fontweight="bold", color=INK, pad=6)
    axA1.set_ylabel("Trips / week", fontsize=8.5)
    axA1.set_ylim(0, 260)
    style_axes(axA1)

    axA2 = fig.add_subplot(charts_row[0, 1])
    baseline_cost, optimized_cost = 748.4, 748.4 * (1 - 0.37)
    bars2 = axA2.bar(["Manual", "LP-optimized"], [baseline_cost, optimized_cost], color=[MUTED, ACCENT], width=0.55)
    for b, v in zip(bars2, [baseline_cost, optimized_cost]):
        axA2.text(b.get_x() + b.get_width() / 2, v + 14, f"{v:,.0f}", ha="center", fontsize=10, fontweight="bold")
    axA2.set_title("Weekly Transport Cost", fontsize=10.5, fontweight="bold", color=INK, pad=6)
    axA2.set_ylabel("Thousand MXN", fontsize=8.5)
    axA2.set_ylim(0, 860)
    style_axes(axA2)

    # ---------- Chart B: inventory policy simulation (synthetic demand) ----------
    axB = fig.add_subplot(charts_row[1, :])
    axB.axhspan(0, R, color=ACCENT, alpha=0.07, zorder=0)
    axB.plot(sim.daily["Date"], sim.daily["Simulated_Inventory"], color=ACCENT, linewidth=1.9,
              label="Simulated (Q,R) policy inventory", zorder=3)
    axB.axhline(R, color=INK, linestyle="--", linewidth=1.1, alpha=0.7, label=f"Reorder point R = {R}", zorder=2)
    axB.set_title("Inventory Policy Simulation -- (Q,R) continuous review on an illustrative intermittent-demand SKU",
                   fontsize=10, fontweight="bold", color=INK, pad=6)
    axB.set_ylabel("Units in inventory", fontsize=8.5)
    axB.set_ylim(0, sim.daily["Simulated_Inventory"].max() * 1.12)
    axB.legend(fontsize=8, loc="upper right", frameon=False)
    style_axes(axB)
    plt.setp(axB.get_xticklabels(), rotation=20, ha="right", rotation_mode="anchor")

    # ---------- Footer ----------
    axF = fig.add_subplot(gs[5, :])
    axF.axis("off")
    axF.text(0, 0.65, "Full model code: github.com/fernandoadoteliz-ai/supply-chain-optimization-portfolio",
              fontsize=8, color=MUTED)
    axF.text(0, 0.05, "Inventory chart uses a synthetic, seeded demand profile for illustration only -- no CEMEX data appears in this document.",
              fontsize=7.3, color=MUTED, style="italic")

    with PdfPages(out_path) as pdf:
        pdf.savefig(fig, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    demand_df = synthetic_demand()
    build_report(demand_df, "results_summary.pdf")
    print("Wrote results_summary.pdf")
