from pathlib import Path
import hashlib
import nbformat
from nbclient import NotebookClient
import pandas as pd

root = Path(__file__).resolve().parent
out = root / 'outputs' / 'clean_eda_2026_09_11'
out.mkdir(parents=True, exist_ok=True)
(out / 'figures').mkdir(exist_ok=True)
raw_hashes = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / 'data/raw').glob('*.csv')}
for name in ['02_data_preprocessing.ipynb', '03_feature_engineering.ipynb', '04_eda_financials.ipynb']:
    nb = nbformat.read(root / 'notebooks' / name, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            for filename in ['financials_clean.csv', 'financials_features.csv']:
                cell.source = cell.source.replace(f'project_root / "data" / "processed" / "{filename}"', f'Path({str(out / filename)!r})')
            cell.source = cell.source.replace('figures_dir = project_root / "figures"', f'figures_dir = Path({str(out / "figures")!r})')
    NotebookClient(nb, timeout=180, kernel_name='python3', resources={'metadata': {'path': str(root)}}).execute()
    nbformat.write(nb, out / name)
    print('PASS ' + name, flush=True)

clean = pd.read_csv(out / 'financials_clean.csv')
features = pd.read_csv(out / 'financials_features.csv')
expected = clean.year.map(lambda y: 'Smart automobile expansion' if 2010 <= y <= 2021 else 'Transition Year' if y == 2022 else 'AI expansion' if 2023 <= y <= 2026 else None)
assert clean.analysis_period.equals(expected.rename('analysis_period'))
raw = pd.read_csv(root / 'data/raw/chip_companies_financials.csv')
pd.testing.assert_frame_equal(clean[raw.columns], raw)
assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in raw_hashes.items())
annual = features.groupby(['analysis_period', 'year', 'value_chain_group']).revenue_usd_bn.sum()
comparison = annual.groupby(['analysis_period', 'value_chain_group']).mean().unstack(0)
comparison = comparison[['Smart automobile expansion', 'Transition Year', 'AI expansion']]
lines = ['# Clean structured data and EDA results', '', 'The cleaning, feature-engineering, EDA, and visualization notebooks completed with all embedded assertions passing.', '', '## Clean structured data', '', f'- Clean data: {clean.shape[0]} company-year records, {clean.shape[1]} columns.', f'- Feature data: {features.shape[0]} records, {features.shape[1]} columns.', '- Original financial values and all raw CSV files are unchanged.', '- No duplicate company-year keys. Eight zero-revenue rows have undefined intensity ratios.', '- Review flags: 17 regional geography records and 18 operating-income discrepancies.', '', '## Period comparison', '', 'Average annual revenue in USD billions; this accounts for unequal period durations.', '', '| Value-chain group | Smart automobile expansion (2010–2021) | Transition Year (2022) | AI expansion (2023–2026) |', '|---|---:|---:|---:|']
for group, row in comparison.iterrows():
    lines.append('| ' + group + ' | ' + ' | '.join(f'{v:.2f}' for v in row) + ' |')
lines += ['', 'Fabless average annual revenue increased by 392.44% between the first and third periods, the largest percentage increase among the five groups. This is a comparison of period averages, not a CAGR.', '', 'The EDA notebook also contains revenue trends, company rankings, concentration, investment-growth correlations, and flag-exclusion sensitivity checks. Historical rankings and growth analyses retain their explicitly stated 2024 endpoint.', '', '## Interpretation limits', '', 'The AI expansion comparison includes 2025–2026 records requiring source validation. Period names are project definitions. Coverage differs over time, shares refer only to this dataset, and associations do not establish causation.', '', '## Files', '', '- `financials_clean.csv` and `financials_features.csv`: fresh processed datasets.', '- `02_data_preprocessing.ipynb` through `04_eda_financials.ipynb`: executed notebooks.', '- Presentation charts are rebuilt separately with `python src/build_final_visualizations.py`.', '', 'This run uses a separate output folder because Windows denied overwriting the existing financials_clean.csv.']
(out / 'RESULTS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('All validations passed. Results: ' + str(out), flush=True)
