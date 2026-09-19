"""
Figures 6 to 10 for the Section 2 analysis in README.md
(why revenue fell in 2023, and where the fall was concentrated).

Re-runnable: every run overwrites the same files in figures/final/, so there is
never more than one copy of each figure.

    python src/visualize_section2_figures.py

Inputs   data/processed/financials_features.csv
         data/raw/chip_prices.csv
         data/raw/fab_capacity.csv
         data/raw/export_controls.csv
Outputs  figures/final/figure6_value_chain_revenue_decline.{png,pdf}
         figures/final/figure7_idm_segment_change.{png,pdf}
         figures/final/figure8_export_controls_test.{png,pdf}
         figures/final/figure9_dram_capacity_vs_price.{png,pdf}
         figures/final/figure10_supply_demand_mechanism.{png,pdf}
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures" / "final"
FIG.mkdir(parents=True, exist_ok=True)

DPI = 300
NAVY, RED, BLU, ORA = TEXT, "#B3261E", "#1A5FB4", "#E8710A"
GREY, BROWN, PURPLE = MUTED, "#5D4037", "#4A148C"


def save(fig, stem):
    """Write PNG and PDF, overwriting whatever is already there."""
    for ext in ("png", "pdf"):
        finalize_figure(fig)
        fig.savefig(FIG / f"{stem}.{ext}", dpi=DPI, bbox_inches="tight",
                    facecolor="white")
    plt.close(fig)
    print("wrote", stem + ".png /", stem + ".pdf")


fin = pd.read_csv(DATA / "processed" / "financials_features.csv")
prices = pd.read_csv(DATA / "raw" / "chip_prices.csv")
capacity = pd.read_csv(DATA / "raw" / "fab_capacity.csv")
controls = pd.read_csv(DATA / "raw" / "export_controls.csv")
PR = prices.groupby(["product", "year"]).price.mean().unstack(0)
idm = fin[fin.value_chain_group.eq("IDM")]


# ------------------------------------------------------------------ Figure 6
def figure6():
    tab = fin[fin.year <= 2025].pivot_table(
        index="year", columns="value_chain_group", values="revenue_usd_bn",
        aggfunc="sum")
    chg = tab.pct_change() * 100
    fig, ax = plt.subplots(figsize=(11, 6.3))
    for group, colour in zip(
            ["IDM", "Fabless", "Foundry", "Equipment", "EDA Software"],
            [BUSINESS_COLORS[g] for g in ["IDM", "Fabless", "Foundry", "Equipment", "EDA Software"]]):
        s = tab.loc[2010:2025, group]
        ax.plot(s.index, s.values, color=colour, marker="o", markersize=4,
                label=group)
    ax.plot(2023, tab.loc[2023, "IDM"], marker="o", markersize=16,
            markerfacecolor="none", markeredgecolor=NEGATIVE, markeredgewidth=2)
    ax.annotate(f"{chg.loc[2023, 'IDM']:.1f}%", (2023, tab.loc[2023, "IDM"]),
                xytext=(-16, -30), textcoords="offset points", ha="right",
                fontsize=10.5, color=NEGATIVE, fontweight="bold")
    ax.set_title("Figure 6  Revenue by Value Chain Group, 2010-2025", loc="left")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (USD billions)")
    ax.set_xticks(range(2010, 2026, 2))
    ax.set_ylim(0, 470)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    save(fig, "figure6_value_chain_revenue_decline")


# ------------------------------------------------------------------ Figure 7
def figure7():
    names = {"idm_memory": "Memory", "idm_cpu": "CPU",
             "idm_automotive": "Automotive", "idm_analog": "Analog",
             "idm_diversified": "Diversified", "idm_power": "Power",
             "idm_micro": "Microcontroller"}
    g = idm.pivot_table(index="segment", columns="year",
                        values="revenue_usd_bn", aggfunc="sum")
    n = idm[idm.year == 2023].groupby("segment").company_name.nunique()
    d = pd.DataFrame({"chg": g[2023] - g[2022],
                      "pct": (g[2023] / g[2022] - 1) * 100,
                      "n": n}).sort_values("chg")
    fig, ax = plt.subplots(figsize=(11, 5.6))
    y = np.arange(len(d))
    ax.barh(y, d.chg.values, height=0.6,
            color=[NEGATIVE if v < 0 else POSITIVE for v in d.chg])
    ax.axvline(0, color="black", linewidth=1)
    for i, (v, pc) in enumerate(zip(d.chg.values, d.pct.values)):
        ax.text(v + (1.4 if v > 0 else -1.4), i, f"{v:+.2f}   ({pc:+.1f}%)",
                va="center", ha="left" if v > 0 else "right",
                fontsize=10, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(
        [f"{names[i]}  ({d.n[i]} firm{'s' if d.n[i] > 1 else ''})"
         for i in d.index], fontsize=10.5)
    ax.set_xlabel("Revenue change 2022 to 2023 (USD billions)")
    ax.set_xlim(-70, 28)
    ax.set_title("Figure 7  Revenue Change by IDM Segment, 2022 to 2023", loc="left")
    ax.grid(True, axis="x", alpha=0.3)
    save(fig, "figure7_idm_segment_change")


# ------------------------------------------------------------------ Figure 8
def figure8():
    targeted = {"Micron", "Yangtze Memory (YMTC)"}
    fig, (left, right) = plt.subplots(1, 2, figsize=(14.5, 5.4),
                                      gridspec_kw={"wspace": 0.34})
    years = list(range(2019, 2026))
    revenue = fin[fin.year.between(2018, 2025)].groupby("year").revenue_usd_bn.sum()
    growth = (revenue.pct_change() * 100).loc[years]
    events = controls.year.value_counts().reindex(years).fillna(0)

    left.bar(events.index, events.values, color=NEUTRAL,
             label="Export control events (count)")
    left.set_ylabel("Number of events")
    left.set_xlabel("Year")
    left.set_ylim(0, 13)
    left.set_xticks(years)
    twin = left.twinx()
    twin.plot(years, growth.values, color=PERIOD_COLORS["pre_ai"], marker="o", linewidth=2,
              label="Total revenue growth (%)")
    twin.axhline(0, color="gray", linewidth=0.8)
    twin.set_ylabel("Revenue growth (%)")
    twin.set_ylim(-14, 34)
    for yr in years:
        twin.annotate(f"{growth[yr]:+.1f}", (yr, growth[yr]),
                      xytext=(4 if yr == 2019 else -12,
                              -18 if yr == 2023 else 9),
                      textcoords="offset points", fontsize=8.5, color=PERIOD_COLORS["pre_ai"])
    left.set_title("A. More rules did not mean lower revenue", fontsize=11.5)
    h1, l1 = left.get_legend_handles_labels()
    h2, l2 = twin.get_legend_handles_labels()
    left.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5)

    mem = fin[fin.segment.eq("idm_memory")].pivot_table(
        index="company_name", columns="year", values="revenue_usd_bn")
    mem["chg"] = (mem[2023] / mem[2022] - 1) * 100
    mem = mem.sort_values("chg")
    short = {"ChangXin Memory (CXMT)": "CXMT", "Yangtze Memory (YMTC)": "YMTC",
             "Samsung Memory": "Samsung", "SK Hynix": "SK Hynix",
             "Micron": "Micron"}
    y = np.arange(len(mem))
    right.barh(y, mem.chg.values, height=0.58,
               color=[NEGATIVE if i in targeted else NEUTRAL
                      for i in mem.index])
    right.axvline(0, color="black", linewidth=1)
    for i, v in enumerate(mem.chg.values):
        right.text(v + (1.8 if v > 0 else -1.8), i, f"{v:+.1f}%", va="center",
                   ha="left" if v > 0 else "right", fontsize=10,
                   fontweight="bold")
    right.set_yticks(y)
    right.set_yticklabels([short[i] for i in mem.index], fontsize=11)
    right.set_xlabel("Revenue change 2022 to 2023 (%)")
    right.set_xlim(-74, 52)
    right.set_ylim(-0.7, 5.15)
    right.set_title("B. Being targeted did not predict the result", fontsize=11.5)
    right.legend(handles=[
        Patch(facecolor=NEGATIVE, label="Targeted by an export control measure"),
        Patch(facecolor=NEUTRAL, label="Not targeted")],
        loc="upper left", fontsize=9, framealpha=0.95)
    right.grid(True, axis="x", alpha=0.3)
    fig.add_artist(Line2D([0.505, 0.505], [0.04, 0.95], color="#9AA5AE",
                          lw=1.1, transform=fig.transFigure))
    save(fig, "figure8_export_controls_test")


# ------------------------- shared DRAM panel for Figures 9 and 10 -----------
def dram_panel():
    """Capacity of the SAME five DRAM entries in every year, so the yearly
    totals are comparable, plus the yearly mean DDR4 price.
    Capacity is returned in MILLION wafers per month."""
    dram = capacity[capacity.fab_type.eq("memory_DRAM")]
    # the file has no fab id, so a fab is company + node + start year
    key = ["company", "process_node_nm", "fab_type", "fab_started_year"]
    years = list(range(2020, 2026))
    common = set.intersection(
        *[set(map(tuple, dram[dram.year == y][key].values)) for y in years])
    panel = dram[dram.apply(lambda r: tuple(r[key]) in common, axis=1)]
    grouped = panel[panel.year.isin(years)].groupby("year").agg(
        cap=("monthly_wafer_capacity", "sum"), n=("company", "size"))
    assert grouped.n.nunique() == 1, "fab panel is not balanced across years"
    return years, grouped.cap / 1e6, PR["DRAM_DDR4_8Gb"].loc[years]


# ------------------------------------------------------------------ Figure 9
def figure9(years, cap, yearly_price):
    shift = (cap[2023] / cap[2021] - 1) * 100
    fall = (yearly_price[2023] / yearly_price[2021] - 1) * 100

    monthly = prices[prices["product"].eq("DRAM_DDR4_8Gb")].copy()
    monthly["date"] = pd.to_datetime(monthly.year_month + "-01")
    monthly = monthly[monthly.year.between(2020, 2025)].sort_values("date")

    fig, ax = plt.subplots(figsize=(11.2, 6.1))
    for y in years:
        ax.bar(pd.Timestamp(f"{y}-07-01"), cap[y], width=pd.Timedelta(days=318),
               color=CAPACITY, zorder=1,
               label="DRAM capacity, yearly (left axis)" if y == years[0] else None)
        dy = -0.16 if y == 2020 else 0.05
        ax.text(pd.Timestamp(f"{y}-07-01"), cap[y] + dy, f"{cap[y]:.2f}",
                ha="center", va="top" if y == 2020 else "bottom",
                fontsize=9.5, color="#33475B")
    ax.set_ylabel("DRAM capacity (million wafers/month)",
                  fontsize=10.5)
    ax.set_ylim(0, 3.35)
    ax.set_xlim(pd.Timestamp("2019-10-01"), pd.Timestamp("2026-02-01"))

    axp = ax.twinx()
    axp.plot(monthly.date, monthly.price, color=PRODUCT_COLORS["DRAM_DDR4_8Gb"], linewidth=1.9,
             label="DRAM DDR4 8Gb price, monthly (right axis)", zorder=3)
    axp.set_ylabel("DRAM DDR4 8Gb price (USD)", color=PRODUCT_COLORS["DRAM_DDR4_8Gb"])
    axp.set_ylim(0, 9.45)
    axp.tick_params(axis="y", colors=PRODUCT_COLORS["DRAM_DDR4_8Gb"])

    hi = monthly.loc[monthly.price.idxmax()]
    lo = monthly.loc[monthly.price.idxmin()]
    for row, word, dx, dy in [(hi, "highest", 20, 16), (lo, "lowest", 14, -30)]:
        axp.plot(row.date, row.price, marker="o", ms=15, mfc="none",
                 mec=PURPLE, mew=2.4, zorder=8)
        axp.annotate(f"{word}  {row.price:.2f}  ({row.year_month})",
                     (row.date, row.price), xytext=(dx, dy),
                     textcoords="offset points", ha="left", fontsize=9.5,
                     color=PURPLE, fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color=PURPLE, lw=1.1))

    x0, x1 = pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-01")
    mid, ya = pd.Timestamp("2022-06-15"), 2.81
    ax.annotate("", xy=(x1, ya), xytext=(x0, ya),
                arrowprops=dict(arrowstyle="-|>", color="#33475B", linewidth=2.4))
    ax.text(mid, ya + 0.105, f"capacity  +{shift:.1f}%", ha="center",
            fontsize=11.5, color="#33475B", fontweight="bold")
    ax.text(mid, ya - 0.25, f"yearly average price  {fall:.1f}%", ha="center",
            fontsize=11.5, color=PRODUCT_COLORS["DRAM_DDR4_8Gb"], fontweight="bold")
    ax.text(mid, ya - 0.43, "2021  →  2023", ha="center", fontsize=9.5,
            color=GREY)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlabel("Year.  Bars are yearly capacity; the blue line is the raw "
                  "monthly price", fontsize=10.5)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = axp.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=9.5, framealpha=0.95)
    ax.set_title("Figure 9  DRAM capacity against DRAM price, 2020-2025", loc="left",
                 fontsize=12)
    ax.grid(True, axis="y", alpha=0.3)
    save(fig, "figure9_dram_capacity_vs_price")
    return shift, fall


# ----------------------------------------------------------------- Figure 10
def figure10(shift, fall):
    """Schematic. Both axes start at zero so the drawn proportions match the
    data: the S1 to S2 gap is `shift` percent of Q_A, and P_C sits at
    (100 + fall) percent of P_A."""
    qa, pa = 100.0, 100.0
    pc = pa * (1 + fall / 100)
    pb = pa * (qa / (qa + shift))
    slope_d = pa / qa
    slope_s = (pa - pb) / ((qa + shift) - (2 * pa - pb))

    d1 = lambda q: 2 * pa - slope_d * q
    s1 = lambda q: pa + slope_s * (q - qa)
    s2 = lambda q: pa + slope_s * (q - qa - shift)
    s1_inv = lambda p: qa + (p - pa) / slope_s
    s2_inv = lambda p: qa + shift + (p - pa) / slope_s
    qb = 2 * pa - pb
    qc = s2_inv(pc)
    d2 = lambda q: d1(q) - (d1(qc) - pc)

    xmax, ymax = 168.0, 150.0
    fig, ax = plt.subplots(figsize=(10.2, 7.4))

    def curve(fn, colour, style, label, q0, dx=1.5, dy=0.0):
        q = np.linspace(q0, xmax, 1200)
        y = fn(q)
        m = (y >= 0.5) & (y <= ymax)
        ax.plot(q[m], y[m], color=colour, lw=2.9, ls=style, zorder=3,
                solid_capstyle="round", dash_capstyle="round")
        ax.text(q[m][-1] + dx, y[m][-1] + dy, label, color=colour, fontsize=15,
                fontweight="bold", ha="left", va="center")

    curve(s1, RED, "-", "S1", 0, dx=0.5, dy=4.0)
    curve(s2, RED, "--", "S2", 0, dx=0.5, dy=4.0)
    curve(d1, BLU, "-", "D1", 72, dx=1.6, dy=1.5)
    curve(d2, BLU, "--", "D2", 72, dx=1.6, dy=1.5)

    for x, y, tag, colour in [(qa, pa, "A", NAVY), (qb, pb, "B", BLU),
                              (qc, pc, "C", ORA)]:
        ax.plot([0, x], [y, y], color=GREY, lw=0.9, ls=":", zorder=1)
        ax.plot([x, x], [0, y], color=GREY, lw=0.9, ls=":", zorder=1)
        ax.plot(x, y, "o", ms=15, color=colour, mec="white", mew=1.8, zorder=6)
        ax.text(x, y, tag, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color="white", zorder=7)
    for y, lab in [(pa, "P$_A$"), (pb, "P$_B$"), (pc, "P$_C$")]:
        ax.text(-3.0, y, lab, ha="right", va="center", fontsize=13.5,
                fontweight="bold", color=NAVY)
    for x, lab in [(qa, "Q$_A$"), (qc, "Q$_C$"), (qb, "Q$_B$")]:
        ax.text(x, -3.5, lab, ha="center", va="top", fontsize=13.5,
                fontweight="bold", color=NAVY)
    ax.text(-3.0, -3.5, "0", ha="right", va="top", fontsize=12, color=NAVY)

    for j, (tag, txt, colour) in enumerate([
            ("A", "2021 observed", NAVY),
            ("B", "if ONLY the supply curve shifts", BLU),
            ("C", "2023 observed", ORA)]):
        yy = 144.0 - j * 10.0
        ax.plot(6.0, yy, "o", ms=15, color=colour, mec="white", mew=1.6, zorder=6)
        ax.text(6.0, yy, tag, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color="white", zorder=7)
        ax.text(12.5, yy, txt, ha="left", va="center", fontsize=11.5,
                fontweight="bold", color=colour)

    ya = 133.0
    ax.annotate("", xy=(s2_inv(ya), ya), xytext=(s1_inv(ya), ya),
                arrowprops=dict(arrowstyle="-|>", color=BROWN, lw=2.3))
    ax.text(s2_inv(ya) + 2.2, ya, f"capacity  +{shift:.1f}%", ha="left",
            va="center", fontsize=11.5, color=BROWN, fontweight="bold")

    xa = 128.0
    ax.annotate("", xy=(xa, d2(xa)), xytext=(xa, d1(xa)),
                arrowprops=dict(arrowstyle="-|>", color=BLU, lw=2.3))
    ax.text(xa + 2.0, (d1(xa) + d2(xa)) / 2, "demand\nfalls", ha="left",
            va="center", fontsize=11.5, color=BLU, fontweight="bold")

    xb = 34.0
    ax.annotate("", xy=(xb, pa), xytext=(xb, pb),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0))
    ax.text(xb + 2.5, (pa + pb) / 2, "explained by the\ncapacity increase",
            ha="left", va="center", fontsize=11, color=RED, fontweight="bold")
    ax.annotate("", xy=(xb, pb), xytext=(xb, pc),
                arrowprops=dict(arrowstyle="<->", color=BLU, lw=2.0))
    ax.text(xb + 2.5, (pb + pc) / 2, "NOT explained by the\ncapacity increase",
            ha="left", va="center", fontsize=11, color=BLU, fontweight="bold")
    xb2 = 13.0
    ax.annotate("", xy=(xb2, pa), xytext=(xb2, pc),
                arrowprops=dict(arrowstyle="<->", color=NAVY, lw=2.3))
    ax.text(xb2 - 3.2, (pa + pc) / 2, f"observed price fall  {fall:.1f}%",
            ha="center", va="center", fontsize=11.5, color=NAVY,
            fontweight="bold", rotation=90)

    ax.set_xlim(-14, xmax + 16)
    ax.set_ylim(-10, ymax + 8)
    ax.annotate("", xy=(xmax + 12, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.7))
    ax.annotate("", xy=(0, ymax + 6), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.7))
    ax.text(xmax + 12, -4.5, "Quantity", ha="right", va="top", fontsize=14,
            fontweight="bold")
    ax.text(2.5, ymax + 6, "Price", ha="left", va="top", fontsize=14,
            fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Figure 10  Capacity growth alone does not explain the price fall",
                 fontsize=13.5, fontweight="bold", color=NAVY, pad=38)
    fig.text(0.125, 0.925,
             "Illustrative diagram. Both axes start at zero, so the supply "
             "shift and the\nobserved price fall are drawn to scale. "
             "The axes carry no units.",
             ha="left", va="top", fontsize=10.5, color=GREY)
    save(fig, "figure10_supply_demand_mechanism")


def main():
    figure6()
    figure7()
    figure8()
    years, cap, yearly_price = dram_panel()
    shift, fall = figure9(years, cap, yearly_price)
    figure10(shift, fall)
    print(f"\ncapacity shift 2021->2023 : {shift:+.1f}%")
    print(f"DDR4 price change 2021->2023: {fall:+.1f}%")
    print(f"figures written to {FIG}")


if __name__ == "__main__":
    main()
