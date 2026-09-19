"""Figure 11 adapted from the updated Best archive."""
import matplotlib
matplotlib.use("Agg")
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()
import matplotlib.ticker as ticker

# Paths
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "figures/final"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
fin = pd.read_csv(DATA_DIR / "processed/financials_features.csv")
fin_hist = fin[fin['year'].between(2010, 2024)].copy()

# Styling

BG_COLOR = '#ffffff'
CARD_BG = '#f8fafc'
CARD_BORDER = '#cbd5e1'
TEXT_MAIN = TEXT
TEXT_SUB = MUTED

COLOR_FABLESS = BUSINESS_COLORS["Fabless"]
COLOR_IDM = BUSINESS_COLORS["IDM"]
COLOR_FOUNDRY = BUSINESS_COLORS["Foundry"]
COLOR_EQUIP = BUSINESS_COLORS["Equipment"]
COLOR_EDA = BUSINESS_COLORS["EDA Software"]

# ==============================================================================
# CHART 1: Value Chain Market Share Dynamics (2010–2025) - 100% Stacked Bar
# ==============================================================================
fin_hist_c1 = fin[fin['year'].between(2010, 2025)].copy()

fig1, ax1 = plt.subplots(figsize=(16, 9), dpi=300, facecolor=BG_COLOR)
fig1.subplots_adjust(top=0.78, bottom=0.12, left=0.06, right=0.96)

# Group revenue by year and compute percentage shares (2010-2025)
group_rev = fin_hist_c1.groupby(['year', 'value_chain_group'])['revenue_usd_bn'].sum().unstack('value_chain_group').fillna(0)
group_shares = group_rev.div(group_rev.sum(axis=1), axis=0) * 100

ordered_groups = ['IDM', 'Foundry', 'Equipment', 'EDA Software', 'Fabless']
palette_shares = {
    'IDM': COLOR_IDM,
    'Foundry': COLOR_FOUNDRY,
    'Equipment': COLOR_EQUIP,
    'EDA Software': COLOR_EDA,
    'Fabless': COLOR_FABLESS
}

group_display_names = {
    'IDM': 'IDM (Intel, Samsung, TI)',
    'Foundry': 'Foundry (TSMC, UMC, GF)',
    'Equipment': 'Equipment (ASML, AMAT, Lam)',
    'EDA Software': 'EDA Software (Synopsys, Cadence)',
    'Fabless': 'Fabless (NVIDIA, Qualcomm, Broadcom, AMD)'
}

years = group_shares.index
bar_width = 0.72
bottoms = np.zeros(len(years))

for grp in ordered_groups:
    vals = group_shares[grp].values
    bars = ax1.bar(years, vals, bottom=bottoms, width=bar_width,
                   color=palette_shares[grp], edgecolor='white', linewidth=1.2,
                   label=group_display_names[grp])
    
    # Text labels inside bars (only for segments with sufficient height >= 4.5%)
    for i, (yr, val, bot) in enumerate(zip(years, vals, bottoms)):
        if val >= 4.5:
            y_pos = bot + val / 2.0
            ax1.text(yr, y_pos, f"{val:.1f}%", ha='center', va='center',
                     color='#ffffff', fontsize=8.6, fontweight='bold')
    
    bottoms += vals

ax1.set_facecolor(CARD_BG)
for spine in ax1.spines.values():
    spine.set_color(CARD_BORDER)
    spine.set_linewidth(1.2)
ax1.grid(True, axis='y', linestyle='--', alpha=0.5, color='#e2e8f0')
ax1.set_axisbelow(True)

ax1.set_xlim(2009.2, 2025.8)
ax1.set_ylim(0, 100)
ax1.set_xticks(years)
ax1.set_xticklabels(years, fontsize=10.8, fontweight='bold', color=MUTED)
ax1.yaxis.set_major_formatter(ticker.PercentFormatter())
ax1.tick_params(colors=TEXT_SUB, labelsize=10.5)
ax1.set_ylabel("Share of Represented Ecosystem Revenue (%)", color=TEXT, fontsize=11.5, fontweight='bold')

# Title & Subtitle
fig1.text(0.06, 0.95, "Figure 11  Revenue Share by Value Chain Group, 2010–2025",
          fontsize=17.5, fontweight='bold', color=TEXT_MAIN, ha='left', va='top')
fig1.text(0.06, 0.905, "100% Stacked Bar Dynamics by Value Chain Role (%) | Transition from IDM Hegemony to Fabless-Foundry Co-Dominance",
          fontsize=11.5, color=TEXT_SUB, ha='left', va='top')

# Milestone Lines & Badges
ax1.axvline(x=2022.5, color='#d97706', ls='--', lw=2.0, alpha=0.85, zorder=3)
ax1.text(2022.5, 101.8, "2022: AI Inflection Point", color="#92400e", fontsize=8.8, fontweight='bold', ha='center',
         bbox=dict(boxstyle="round,pad=0.25", fc="#fef3c7", ec="#d97706", lw=1.1), clip_on=False)

ax1.text(2024.7, 101.8, "Fabless Overtakes IDM (#1)", color=BUSINESS_COLORS["Fabless"], fontsize=8.5, fontweight='bold', ha='center',
         bbox=dict(boxstyle="round,pad=0.25", fc="#E8F0FA", ec=BUSINESS_COLORS["Fabless"], lw=1.1), clip_on=False)

# Legend placed horizontally on top (ordered top-to-bottom as displayed on the stacks)
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1], labels[::-1], loc='lower center', bbox_to_anchor=(0.5, 1.09),
           ncol=5, frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1', fontsize=9.2, framealpha=0.98)

# Save without Key Takeaway Box
finalize_figure(fig1)
fig1.savefig(OUT_DIR / "figure11_value_chain_revenue_share.png", dpi=300, facecolor=BG_COLOR, bbox_inches='tight')
finalize_figure(fig1)
fig1.savefig(OUT_DIR / "figure11_value_chain_revenue_share.pdf", facecolor=BG_COLOR, bbox_inches='tight')
plt.close(fig1)

