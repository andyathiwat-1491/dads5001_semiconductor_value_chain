"""Figures 12-13 adapted from the updated Best archive."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/processed/financials_features.csv")


years = list(range(2010, 2026))


out_dir = ROOT / "figures/final"
out_dir.mkdir(parents=True, exist_ok=True)

# Prepare revenue data
rev_data = []
for yr in years:
    sub = df[df.year == yr].sort_values(by="revenue_usd_bn", ascending=False).head(3).reset_index(drop=True)
    rev_data.append({
        "year": yr,
        "r1_name": sub.loc[0, "company_name"], "r1_val": sub.loc[0, "revenue_usd_bn"],
        "r2_name": sub.loc[1, "company_name"], "r2_val": sub.loc[1, "revenue_usd_bn"],
        "r3_name": sub.loc[2, "company_name"], "r3_val": sub.loc[2, "revenue_usd_bn"],
        "total": sub["revenue_usd_bn"].sum()
    })
rev_df = pd.DataFrame(rev_data)

x_pos = np.arange(len(years))
bar_width = 0.72

legend_patches = [
    mpatches.Patch(facecolor=COMPANY_COLORS['Intel'], edgecolor=TEXT, label='Intel (IDM)'),
    mpatches.Patch(facecolor=COMPANY_COLORS['Samsung Memory'], edgecolor=TEXT, label='Samsung Memory (IDM)'),
    mpatches.Patch(facecolor=COMPANY_COLORS['TSMC'], edgecolor=TEXT, label='TSMC (Foundry)'),
    mpatches.Patch(facecolor=COMPANY_COLORS['SK Hynix'], edgecolor=TEXT, label='SK Hynix (IDM)'),
    mpatches.Patch(facecolor=COMPANY_COLORS['NVIDIA'], edgecolor=TEXT, label='NVIDIA (Fabless)'),
]

# ==============================================================================
# 1. TOP 3 REVENUE STACKED BAR CHART - FULL SOLID COLOR (NEW 3-ERA DESIGN)
# ==============================================================================
fig1b, ax1b = plt.subplots(figsize=(16.5, 9.2), dpi=300)
fig1b.patch.set_facecolor('#FFFFFF')
ax1b.set_facecolor('#FFFFFF')
fig1b.subplots_adjust(top=0.84, bottom=0.08, left=0.06, right=0.97)

bottoms1b = np.zeros(len(years))

for r in [3, 2, 1]:
    heights = rev_df[f"r{r}_val"].values
    names = rev_df[f"r{r}_name"].values
    colors = [COMPANY_COLORS.get(n, '#94A3B8') for n in names]
    
    bars = ax1b.bar(
        x_pos, heights, bottom=bottoms1b, width=bar_width,
        color=colors, edgecolor=TEXT, linewidth=0.9, zorder=3, alpha=1.0
    )
    
    for i, (b, h, name) in enumerate(zip(bars, heights, names)):
        y_center = bottoms1b[i] + h / 2.0
        if h >= 50:
            fsize = 9.5
        elif h >= 25:
            fsize = 8.5
        elif h >= 14:
            fsize = 7.6
        else:
            fsize = 6.8
            
        lbl = f"${h:.1f}B"
        ax1b.text(
            b.get_x() + b.get_width() / 2, y_center, lbl,
            ha='center', va='center',
            fontsize=fsize, fontweight='heavy', color='#FFFFFF', zorder=6
        )
        
    bottoms1b += heights

# Total labels on top of each bar
for i, tot in enumerate(rev_df['total']):
    lbl = f"${tot:.1f}B"
    ax1b.text(
        x_pos[i], tot + 4.5, lbl,
        ha='center', va='bottom',
        fontsize=8.8, fontweight='heavy', color=TEXT, zorder=6
    )

ax1b.set_xticks(x_pos)
ax1b.set_xticklabels([str(y) for y in years], fontsize=11.5, fontweight='bold', color=TEXT)

ax1b.set_xlim(-0.8, 15.8)
ax1b.set_ylim(0, 440)
ax1b.set_ylabel("Total Top 3 Revenue (USD Billions)", fontsize=12, fontweight='bold', labelpad=10)

# Title & Subtitle via fig.text
fig1b.text(0.06, 0.965, "Figure 12  Top 3 Semiconductor Companies by Annual Revenue, 2010–2025",
           fontsize=17.5, fontweight='bold', color=TEXT, ha='left', va='top')
fig1b.text(0.06, 0.925, "16-Year Industry Transformation: Long-Term Transition from PC/Mobile IDMs to Pure-Play Foundry & AI Fabless Champions",
           fontsize=11.2, fontweight='bold', color='#1E3A8A', ha='left', va='top')

ax1b.grid(axis='y', linestyle='--', alpha=0.35, zorder=1)
for spine in ax1b.spines.values():
    spine.set_color('#CBD5E1')

# Dashed lines dividing the eras
# Era 1 (2010-2016) | Era 2 (2017-2021) | 2022 (Transition) | Era 3 (2023-2025)
ax1b.axvline(x=6.5, color='#64748B', linestyle='--', linewidth=1.8, alpha=0.85, zorder=2)
ax1b.axvline(x=11.5, color='#64748B', linestyle='--', linewidth=1.8, alpha=0.85, zorder=2)
ax1b.axvline(x=12.5, color='#D97706', linestyle='--', linewidth=2.0, alpha=0.9, zorder=2)

# Era Badges inside the plot with precise placement
ax1b.text(
    3.0, 412, "2010–2016: PC & Mobile IDM",
    ha='center', va='center', fontsize=9.6, fontweight='bold', color='#1E3A8A',
    bbox=dict(boxstyle='round,pad=0.35', fc='#EFF6FF', ec='#93C5FD', lw=1.2), zorder=7
)

ax1b.text(
    9.0, 412, "2017–2021: Memory Super-Cycles & Rise of Foundry",
    ha='center', va='center', fontsize=9.2, fontweight='bold', color='#9A3412',
    bbox=dict(boxstyle='round,pad=0.35', fc='#FFF7ED', ec='#FDBA74', lw=1.2), zorder=7
)

ax1b.text(
    12.0, 428, "2022: Transition",
    ha='center', va='center', fontsize=8.6, fontweight='bold', color=MUTED,
    bbox=dict(boxstyle='round,pad=0.28', fc='#F8FAFC', ec='#94A3B8', lw=1.1), zorder=7
)

ax1b.text(
    14.0, 412, "2023–2025: The AI Explosion",
    ha='center', va='center', fontsize=9.6, fontweight='bold', color='#065F46',
    bbox=dict(boxstyle='round,pad=0.35', fc='#ECFDF5', ec='#10B981', lw=1.2), zorder=7
)

# Centered legend above axes
ax1b.legend(
    handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, 1.015),
    ncol=5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=10.2, framealpha=0.98
)

# Clean save: NO pointer annotations, NO footer text, NO source below graph!
finalize_figure(fig1b)
fig1b.savefig(out_dir / "figure12_top3_revenue.png", bbox_inches='tight', dpi=300)
finalize_figure(fig1b)
fig1b.savefig(out_dir / "figure12_top3_revenue.pdf", bbox_inches='tight')
plt.close(fig1b)


# ==============================================================================
# 2. TOP 3 REVENUE STACKED BAR CHART - SPOTLIGHT 2023 (NEW 3-ERA DESIGN)
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(16.5, 9.2), dpi=300)
fig1.patch.set_facecolor('#FFFFFF')
ax1.set_facecolor('#FFFFFF')
fig1.subplots_adjust(top=0.84, bottom=0.08, left=0.06, right=0.97)

bottoms = np.zeros(len(years))

for r in [3, 2, 1]:
    heights = rev_df[f"r{r}_val"].values
    names = rev_df[f"r{r}_name"].values
    colors = [COMPANY_COLORS.get(n, '#94A3B8') for n in names]
    
    bars = ax1.bar(
        x_pos, heights, bottom=bottoms, width=bar_width,
        color=colors, edgecolor=TEXT, linewidth=0.9, zorder=3
    )
    
    # 2023 full vibrant color, other years faded
    for i, (b, h, name) in enumerate(zip(bars, heights, names)):
        yr = years[i]
        is_2023 = (yr == 2023)
        y_center = bottoms[i] + h / 2.0
        
        if is_2023:
            b.set_alpha(1.0)
            b.set_edgecolor(TEXT)
            b.set_linewidth(1.5)
            lbl = f"${h:.1f}B"
            ax1.text(b.get_x() + b.get_width()/2, y_center, lbl, ha='center', va='center',
                     fontsize=9.6, fontweight='heavy', color='#FFFFFF', zorder=6)
        else:
            b.set_alpha(0.28)
            b.set_edgecolor('#94A3B8')
            b.set_linewidth(0.5)
            lbl = f"${h:.1f}B"
            ax1.text(b.get_x() + b.get_width()/2, y_center, lbl, ha='center', va='center',
                     fontsize=7.8, fontweight='bold', color=MUTED, zorder=6)
        
    bottoms += heights

# Total labels on top of each bar
for i, tot in enumerate(rev_df['total']):
    yr = years[i]
    if yr == 2023:
        lbl = f"${tot:.1f}B"
        ax1.text(x_pos[i], tot + 6.0, lbl, ha='center', va='bottom', fontsize=10.8, fontweight='heavy',
                 color='#047857',
                 bbox=dict(boxstyle='round,pad=0.28', facecolor='#ECFDF5', edgecolor='#059669', lw=1.3),
                 zorder=7)
    else:
        lbl = f"${tot:.1f}B"
        ax1.text(x_pos[i], tot + 4.5, lbl, ha='center', va='bottom', fontsize=8.2, fontweight='bold',
                 color='#64748B', zorder=6)

ax1.set_xticks(x_pos)
ax1.set_xticklabels([str(y) for y in years], fontsize=11.5, fontweight='bold')
for tick in ax1.get_xticklabels():
    if tick.get_text() == '2023':
        tick.set_color('#047857')
        tick.set_fontsize(13.5)
        tick.set_fontweight('heavy')
    else:
        tick.set_color('#64748B')

ax1.set_xlim(-0.8, 15.8)
ax1.set_ylim(0, 440)
ax1.set_ylabel("Total Top 3 Revenue (USD Billions)", fontsize=12, fontweight='bold', labelpad=10)

# Title & Subtitle via fig.text
fig1.text(0.06, 0.965, "Figure 13  Spotlight on 2023 Top 3 Revenue Shift, 2010–2025",
          fontsize=17.5, fontweight='bold', color=TEXT, ha='left', va='top')
fig1.text(0.06, 0.925, "Spotlight on 2023: The Generative AI Turning Point & NVIDIA's Historic Entry into the Top 3",
          fontsize=11.2, fontweight='bold', color='#047857', ha='left', va='top')

ax1.grid(axis='y', linestyle='--', alpha=0.35, zorder=1)
for spine in ax1.spines.values():
    spine.set_color('#CBD5E1')

# Dashed lines dividing the eras
# Era 1 (2010-2016) | Era 2 (2017-2021) | 2022 (Transition) | Era 3 (2023-2025)
ax1.axvline(x=6.5, color='#64748B', linestyle='--', linewidth=1.8, alpha=0.85, zorder=2)
ax1.axvline(x=11.5, color='#64748B', linestyle='--', linewidth=1.8, alpha=0.85, zorder=2)
ax1.axvline(x=12.5, color='#D97706', linestyle='--', linewidth=2.0, alpha=0.9, zorder=2)

# Era Badges inside the plot with precise placement
ax1.text(
    3.0, 412, "2010–2016: PC & Mobile IDM",
    ha='center', va='center', fontsize=9.6, fontweight='bold', color='#1E3A8A',
    bbox=dict(boxstyle='round,pad=0.35', fc='#EFF6FF', ec='#93C5FD', lw=1.2), zorder=7
)

ax1.text(
    9.0, 412, "2017–2021: Memory Super-Cycles & Rise of Foundry",
    ha='center', va='center', fontsize=9.2, fontweight='bold', color='#9A3412',
    bbox=dict(boxstyle='round,pad=0.35', fc='#FFF7ED', ec='#FDBA74', lw=1.2), zorder=7
)

ax1.text(
    12.0, 428, "2022: Transition",
    ha='center', va='center', fontsize=8.6, fontweight='bold', color=MUTED,
    bbox=dict(boxstyle='round,pad=0.28', fc='#F8FAFC', ec='#94A3B8', lw=1.1), zorder=7
)

ax1.text(
    14.0, 412, "2023–2025: The AI Explosion",
    ha='center', va='center', fontsize=9.6, fontweight='bold', color='#065F46',
    bbox=dict(boxstyle='round,pad=0.35', fc='#ECFDF5', ec='#10B981', lw=1.2), zorder=7
)

# Centered legend above axes
ax1.legend(
    handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, 1.015),
    ncol=5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=10.2, framealpha=0.98
)

# Clean save: NO pointer annotations, NO footer text, NO source below graph!
finalize_figure(fig1)
fig1.savefig(out_dir / "figure13_top3_revenue_2023.png", bbox_inches='tight', dpi=300)
finalize_figure(fig1)
fig1.savefig(out_dir / "figure13_top3_revenue_2023.pdf", bbox_inches='tight')
plt.close(fig1)

print("Successfully generated updated top3 charts with the 3 eras!")
