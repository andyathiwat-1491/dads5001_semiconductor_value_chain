"""Figure 2: dataset geography and business-type revenue, using 2025 records.

Boundaries: Natural Earth, public domain, 1:50m admin-0 countries.
https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_0_countries.geojson
"""
import json
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2025
COLORS = BUSINESS_COLORS
def main():
    source = ROOT / 'data/processed/financials_features.csv'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    data = pd.read_csv(source)
    rows = data.loc[data.year.eq(YEAR)].copy()
    assert not rows.duplicated(['company_name', 'year']).any()
    assert rows[['country_iso3', 'value_chain_group', 'revenue_usd_bn']].notna().all().all()
    assert (rows.revenue_usd_bn >= 0).all()
    codes = rows.groupby('country_iso3').revenue_usd_bn.sum().sort_values(ascending=False).index.tolist()
    assert len(codes) <= 9, 'The requested 3x3 layout supports at most nine geographies.'
    assert set(rows.value_chain_group).issubset(COLORS), 'Assign a display color for new categories.'
    assert not rows.empty
    totals = rows.groupby(['country_iso3', 'value_chain_group']).agg(
        revenue_usd_bn=('revenue_usd_bn', 'sum'), companies=('company_name', 'nunique')).reset_index()
    assert np.isclose(totals.revenue_usd_bn.sum(), rows.revenue_usd_bn.sum())
    winners = {}
    for code, group in totals.groupby('country_iso3'):
        leaders = group.loc[group.revenue_usd_bn.eq(group.revenue_usd_bn.max())]
        assert len(leaders) == 1, f'Tied leaders need explicit display: {code}'
        winners[code] = leaders.iloc[0]

    fig = plt.figure(figsize=(18, 18), facecolor='white')
    fig.text(.045, .970, 'FIGURE 2', color='#168c86', weight='bold', fontsize=11)
    fig.text(.045, .940, 'Semiconductor Industry Landscape by Country/Region', color=TEXT, weight='bold', fontsize=20)
    fig.text(.045, .915, 'Geographic specialization across the semiconductor value chain', fontsize=14, color=MUTED)
    fig.text(.045, .885, f'{YEAR}  |  {len(codes)} countries/regions  |  {rows.company_name.nunique()} companies  |  '
             f'Total revenue: ${rows.revenue_usd_bn.sum():,.2f}B', fontsize=13, weight='bold', color=TEXT)
    fig.text(.045, .862, 'Top 3 categories by revenue  |  Donut labels: share of Top 3 revenue  |  Table shares: share of total geography revenue',
             fontsize=10.8, color=MUTED)
    geo = json.loads((ROOT / 'data/reference/ne_50m_admin_0_countries.geojson').read_text(encoding='utf-8'))
    features = {f['properties']['ADM0_A3']: f for f in geo['features']}
    # Each independent close-up uses its own scale. Mainland US is shown for legibility.
    bounds = {'USA': (-127, -65, 23, 51), 'GBR': (-9, 3, 49, 60),
              'NLD': (3, 8, 50, 54), 'DEU': (5, 16, 47, 56),
              'CHN': (72, 136, 17, 55), 'KOR': (125, 130, 33, 39),
              'JPN': (128, 147, 29, 46), 'TWN': (119, 123, 21, 26)}
    exported = []
    for i, code in enumerate(codes):
        col, row = i % 3, i // 3
        x, y, w, h = .045 + col * .31, .595 - row * .25, .29, .235
        card = fig.add_axes([x, y, w, h])
        card.set_xlim(0, 1); card.set_ylim(0, 1); card.axis('off')
        card.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor='#f5f8fa', edgecolor='#dce5eb', lw=1))
        group = totals.loc[totals.country_iso3.eq(code)].sort_values(
            ['revenue_usd_bn', 'value_chain_group'], ascending=[False, True]).set_index('value_chain_group')
        leader = winners[code]
        total = group.revenue_usd_bn.sum()
        count = rows.loc[rows.country_iso3.eq(code), 'company_name'].nunique()
        top = group.head(3).copy()
        top_total = top.revenue_usd_bn.sum()
        assert top_total > 0
        top['rank'] = np.arange(1, len(top) + 1)
        top['share_of_geography_pct'] = top.revenue_usd_bn / total * 100
        top['share_of_top3_pct'] = top.revenue_usd_bn / top_total * 100
        top['country_iso3'] = code
        top['year'] = YEAR
        exported.append(top.reset_index())
        assert np.isclose(top.share_of_top3_pct.sum(), 100)
        assert len(top) == min(3, len(group)) and top.revenue_usd_bn.is_monotonic_decreasing
        name = features[code]['properties']['NAME_EN'] if code in features else {'EUR': 'Europe (region)' }[code]
        card.text(.045, .94, name, fontsize=16, weight='bold', color=TEXT)
        card.text(.045, .865, f'{count} compan' + ('y' if count == 1 else 'ies') + f' | Total revenue: ${total:,.2f}B', fontsize=10.5, color=MUTED)
        if code in features or code == 'EUR':
            ax = fig.add_axes([x + .012, y + .101, .118, .090])
            if code not in bounds:
                if code == 'EUR':
                    bounds[code] = (-14, 38, 34, 71)
                else:
                    geom = features[code]['geometry']
                    polygons = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
                    pts = np.concatenate([np.asarray(p[0]) for p in polygons])
                    bounds[code] = (pts[:, 0].min()-1, pts[:, 0].max()+1, pts[:, 1].min()-1, pts[:, 1].max()+1)
            west, east, south, north = bounds[code]
            for fcode, feature in features.items():
                geom = feature['geometry']
                polygons = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
                for polygon in polygons:
                    points = np.asarray(polygon[0])
                    if (points[:, 0].max() < west or points[:, 0].min() > east
                            or points[:, 1].max() < south or points[:, 1].min() > north):
                        continue
                    highlighted = fcode == code or (code == 'EUR' and feature['properties']['CONTINENT'] == 'Europe')
                    ax.add_patch(Polygon(polygon[0], facecolor=COLORS[leader.value_chain_group] if highlighted else '#dce4e9',
                                         edgecolor='white', linewidth=.6))
            west, east, south, north = bounds[code]
            ax.set_xlim(west, east); ax.set_ylim(south, north)
            ax.set_aspect(1 / np.cos(np.radians((south + north) / 2)))
            ax.axis('off')
            caption = 'Region locator only' if code == 'EUR' else ('Mainland view' if code == 'USA' else 'Country close-up')
            card.text(.055, .405, caption, fontsize=8, color='#687c88')
        pie = fig.add_axes([x + .140, y + .093, .14, .108])
        pie.pie(top.revenue_usd_bn, colors=[COLORS[g] for g in top.index],
                startangle=90, counterclock=False,
                wedgeprops=dict(edgecolor='white', linewidth=1.4, width=.50),
                autopct=lambda pct: f'{pct:.1f}%',
                textprops=dict(color='white', fontsize=9, weight='bold'), pctdistance=.73)
        pie.text(0, .10, 'Top 3', ha='center', va='center', color=TEXT, fontsize=11, weight='bold')
        pie.text(0, -.18, 'by revenue', ha='center', va='center', color=MUTED, fontsize=8)
        assert np.isclose((group.revenue_usd_bn / total).sum(), 1)
        card.text(.045, .355, f'Top: {leader.value_chain_group} | ${leader.revenue_usd_bn:,.2f}B',
                  fontsize=11, color=COLORS[leader.value_chain_group], weight='bold')
        for xx, label, ha in [(.045, 'Category', 'left'), (.65, 'Share', 'right'), (.95, 'Revenue (B USD)', 'right')]:
            card.text(xx, .278, label, fontsize=9, color=MUTED, weight='bold', ha=ha)
        card.plot([.045, .95], [.258, .258], color='#d5dfe6', lw=.8)
        for j, (business, values) in enumerate(top.iterrows()):
            yy = .212 - j * .066
            card.plot(.058, yy, 's', color=COLORS[business], ms=6)
            card.text(.095, yy, business, fontsize=9.5, va='center', color='#354751', weight='bold' if j == 0 else 'normal')
            card.text(.65, yy, f'{values.share_of_geography_pct:.1f}%', fontsize=9.5, va='center', ha='right', color='#354751')
            card.text(.95, yy, f'{values.revenue_usd_bn:,.2f}',
                      fontsize=9.5, va='center', ha='right', color='#354751')
    out = ROOT / 'figures/final/figure2_country_business_map'
    for ext in ['png', 'svg']:
        finalize_figure(fig)
        fig.savefig(out.with_suffix('.' + ext), dpi=220, facecolor='white')
    plt.close(fig)
    totals.to_csv(ROOT / 'outputs/final_visualizations/figure_02_country_business_inputs.csv', index=False)
    pd.concat(exported, ignore_index=True).to_csv(ROOT / 'outputs/final_visualizations/figure_02_top3.csv', index=False)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash, 'Source dataset changed.'
    print(totals.to_string(index=False))
    print(f'Validated {len(codes)} countries/regions, {rows.company_name.nunique()} companies, total revenue ${rows.revenue_usd_bn.sum():,.2f}B; source unchanged.')


if __name__ == '__main__':
    main()
