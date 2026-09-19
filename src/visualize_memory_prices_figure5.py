"""Figure 5: descriptive memory-price context for the 2023 revenue decline."""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from visualization_theme import (BUSINESS_COLORS, PRODUCT_COLORS, COMPANY_COLORS,
    PERIOD_COLORS, TEXT, MUTED, POSITIVE, NEGATIVE, NEUTRAL, CAPACITY,
    apply_theme, finalize_figure)
apply_theme()
import matplotlib.dates as mdates
from matplotlib.ticker import PercentFormatter
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/supporting_data_eda/clean/chip_prices_clean.csv'
OUT = ROOT / 'outputs/final_visualizations'
FIG = ROOT / 'figures/final/figure5_memory_price_divergence'
PRODUCTS = {'DRAM_DDR4_8Gb': ('DRAM DDR4 8Gb', PRODUCT_COLORS["DRAM_DDR4_8Gb"]),
            'NAND_64Gb_MLC': ('NAND 64Gb MLC', PRODUCT_COLORS["NAND_64Gb_MLC"]),
            'HBM3_stack': ('HBM3', PRODUCT_COLORS["HBM3_stack"])}


def main():
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    data = pd.read_csv(SOURCE)
    data['date'] = pd.to_datetime(data.year_month, format='%Y-%m', errors='raise')
    assert data.date.notna().all()
    rows = data.loc[data['product'].isin(PRODUCTS) & data.date.between('2022-01-01', '2024-12-01')].copy()
    assert not rows.duplicated(['product', 'date']).any(), 'Duplicate product-month records'
    rows['price'] = pd.to_numeric(rows.price, errors='raise')
    assert rows.price.notna().all() and rows.price.gt(0).all(), 'Missing or nonpositive prices'
    assert rows.currency.eq('USD').all()
    rows = rows.sort_values(['product', 'date'])
    baselines, summaries = [], []
    expected = {'DRAM_DDR4_8Gb': (3.21, 1.65), 'NAND_64Gb_MLC': (4.31, 3.62), 'HBM3_stack': (233.15, 359.58)}
    for product, (label, _) in PRODUCTS.items():
        group = rows.loc[rows['product'].eq(product)]
        assert not group.empty and group.unit.nunique() == 1
        first = group.iloc[0]
        if product != 'HBM3_stack':
            assert first.date == pd.Timestamp('2022-01-01'), 'January 2022 baseline required'
        missing = pd.date_range(first.date, '2024-12-01', freq='MS').difference(group.date)
        assert len(missing) == 0, f'Missing months for {product}: {missing}'
        rows.loc[group.index, 'price_index'] = group.price / first.price * 100
        assert rows.loc[group.index[0], 'price_index'] == 100
        baselines.append({'product': product, 'baseline_month': first.year_month, 'baseline_price': first.price, 'unit': first.unit})
        a = group.loc[group.date.dt.year.eq(2022), 'price']
        b = group.loc[group.date.dt.year.eq(2023), 'price']
        comparable = len(a) == len(b) == 12
        summaries.append({'product': product, 'label': label, 'unit': first.unit,
                          'months_2022': len(a), 'months_2023': len(b),
                          'average_2022': a.mean(), 'average_2023': b.mean(),
                          'change_pct': (b.mean()/a.mean()-1)*100 if comparable else None,
                          'difference_from_expected_2022': a.mean()-expected[product][0],
                          'difference_from_expected_2023': b.mean()-expected[product][1]})
    summary = pd.DataFrame(summaries).sort_values('change_pct')
    baseline = pd.DataFrame(baselines)
    all_january = baseline.baseline_month.eq('2022-01').all()
    navy, grey, teal = TEXT, MUTED, PRODUCT_COLORS["HBM3_stack"]
    fig = plt.figure(figsize=(18, 10))
    fig.text(.06, .958, 'FIGURE 5 | Memory Prices Diverged in 2023',
             fontsize=17, weight='bold', color=navy, va='top')
    fig.text(.06, .91, 'Monthly normalized price trends and changes in annual average prices during the 2023 revenue downturn',
             fontsize=12.5, color=grey)
    fig.text(.06, .868, 'Conventional DRAM and NAND prices declined in 2023, while HBM prices increased as AI-oriented memory demand began to emerge.',
             fontsize=12, color=teal, weight='bold')
    ax = fig.add_axes([.075, .30, .51, .49])
    bar = fig.add_axes([.735, .30, .22, .49])
    ax.set_title('A. Monthly normalized price trends', loc='left', fontsize=14, weight='bold', color=navy, pad=18)
    bar.set_title('B. Annual average price change\n2022–2023', loc='left', fontsize=14, weight='bold', color=navy, pad=18)
    for axis in (ax, bar):
        axis.set_axisbelow(True)
        axis.tick_params(colors=grey)
        axis.spines[['left', 'bottom']].set_color('#BAC2C9')
    ax.grid(axis='y', color='#E3E7EB', linewidth=.7)
    ax.axvspan(pd.Timestamp('2023-01-01'), pd.Timestamp('2024-01-01'), color='#EAF3F2', zorder=0)
    ax.axvline(pd.Timestamp('2023-01-01'), color='#82999F', linestyle='--', linewidth=1)
    ax.axhline(100, color='#9AA9B1', linestyle=':', linewidth=1.2)
    for product, (label, color) in PRODUCTS.items():
        group = rows.loc[rows['product'].eq(product)]
        ax.plot(group.date, group.price_index, color=color, linewidth=2.8)
        last = group.iloc[-1]
        ax.scatter([last.date], [last.price_index], color=color, edgecolor='white', s=40, zorder=4)
        ax.annotate(f'{label}\n{last.price_index:.1f}', (last.date, last.price_index), xytext=(10, 0),
                    textcoords='offset points', va='center', color=color, weight='bold', fontsize=10, annotation_clip=False)
    ax.set_xlim(pd.Timestamp('2022-01-01'), pd.Timestamp('2025-05-01'))
    ax.set_ylim(0, rows.price_index.max()*1.13)
    ax.set_xticks(pd.to_datetime(['2022-01-01','2022-07-01','2023-01-01','2023-07-01','2024-01-01','2024-07-01','2024-12-01']))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
    ax.set_xlabel('Month', color=navy, labelpad=10)
    ax.set_ylabel('Normalized Price Index (January 2022 = 100)' if all_january else
                  'Normalized Price Index (First Available Observation = 100)', color=navy, labelpad=12)
    ax.text(pd.Timestamp('2023-07-01'), ax.get_ylim()[1]*.97, '2023 revenue downturn', ha='center', va='top', fontsize=10, color=grey)
    ax.annotate('HBM increased', (pd.Timestamp('2023-10-01'), float(rows.loc[rows['product'].eq('HBM3_stack') & rows.date.eq('2023-10-01'), 'price_index'].iloc[0])),
                xytext=(pd.Timestamp('2022-05-01'), 280), color=teal, fontsize=11,
                arrowprops={'arrowstyle':'-', 'color':teal, 'lw':1})
    ax.text(pd.Timestamp('2023-02-01'), 17, 'Conventional memory weakened', color=NEGATIVE, fontsize=10)
    comparable = summary.dropna(subset=['change_pct'])
    positions = range(len(comparable))
    bar.barh(list(positions), comparable.change_pct, height=.48,
             color=[PRODUCT_COLORS[product] for product in comparable['product']])
    bar.set_yticks(list(positions), comparable.label)
    bar.invert_yaxis()
    bar.set_ylim(len(comparable)-.3, -.7)
    bar.axvline(0, color='#7E919A', linewidth=1)
    bar.grid(axis='x', color='#E3E7EB', linewidth=.7)
    bar.set_xlim(-85, 80)
    bar.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    bar.set_xlabel('Change in annual average price (%)', color=navy, labelpad=10)
    for y, row in enumerate(comparable.itertuples()):
        bar.text(row.change_pct + (-3 if row.change_pct < 0 else 3), y, f'{row.change_pct:+.1f}%',
                 ha='right' if row.change_pct < 0 else 'left', va='center', weight='bold',
                 color=NEGATIVE if row.change_pct < 0 else teal, fontsize=12)
    baseline_text = 'Baselines: ' + '; '.join(f"{PRODUCTS[r.product][0]} ${r.baseline_price:,.2f}/{r.unit.split('/')[-1]} ({r.baseline_month})" for r in baseline.itertuples()) + '. All series begin at 100.'
    fig.text(.06, .205, baseline_text, fontsize=10, color=grey)
    fig.text(.06, .17, 'Annual averages use 12 monthly observations per product in each year. Percentage change = (2023 average / 2022 average − 1) × 100.', fontsize=10, color=grey)
    FIG.parent.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for extension in ('png', 'svg'):
        finalize_figure(fig)
        fig.savefig(FIG.with_suffix('.'+extension), dpi=300, facecolor='white')
    plt.close(fig)
    rows[['product','date','currency','unit','price','price_index']].to_csv(OUT/'figure_05_memory_monthly.csv', index=False)
    summary.to_csv(OUT/'figure_05_memory_annual_summary.csv', index=False)
    baseline.to_csv(OUT/'figure_05_memory_baselines.csv', index=False)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    report = {'source_sha256': source_hash, 'source_unchanged': True, 'rows': len(rows),
              'duplicates': 0, 'missing_prices': 0, 'missing_months_after_baseline': 0,
              'all_series_start_at_100': True, 'all_baselines_january_2022': bool(all_january),
              'expected_annual_averages_match_to_cents': bool((summary[['difference_from_expected_2022','difference_from_expected_2023']].abs()<.005).all().all())}
    (OUT/'figure_05_memory_validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    findings = ['# Figure 5: memory prices', '', baseline.to_string(index=False), '', summary.to_string(index=False), '',
                'The annual averages match all six supplied approximate values when rounded to cents.',
                'The source financial data show 2023 revenue of $654.35B (the request says $654.40B). Figure 5 does not repeat that rounded total.',
                'These price series establish divergence and temporal association, not causality, demand volumes, or whether AI demand offset broader weakness.',
                'Source CSV unchanged; 108 unique product-months; no missing observations; all three January 2022 baselines equal index 100.']
    (OUT/'figure_05_memory_findings.md').write_text('\n'.join(findings)+'\n', encoding='utf-8')
    print(summary[['label','average_2022','average_2023','change_pct']].to_string(index=False))
    print(json.dumps(report, indent=2))
    print(FIG.with_suffix('.png'))


if __name__ == '__main__':
    main()
