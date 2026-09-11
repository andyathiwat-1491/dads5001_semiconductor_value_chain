# Clean structured data and EDA results

The cleaning, feature-engineering, EDA, and visualization notebooks completed with all embedded assertions passing.

## Clean structured data

- Clean data: 617 company-year records, 20 columns.
- Feature data: 617 records, 38 columns.
- Original financial values and all raw CSV files are unchanged.
- No duplicate company-year keys. Eight zero-revenue rows have undefined intensity ratios.
- Review flags: 17 regional geography records and 18 operating-income discrepancies.

## Period comparison

Average annual revenue in USD billions; this accounts for unequal period durations.

| Value-chain group | Smart automobile expansion (2010–2021) | Transition Year (2022) | AI expansion (2023–2026) |
|---|---:|---:|---:|
| EDA Software | 4.42 | 8.34 | 11.26 |
| Equipment | 44.43 | 97.26 | 114.61 |
| Fabless | 65.40 | 154.83 | 322.04 |
| Foundry | 52.64 | 119.96 | 139.51 |
| IDM | 209.59 | 317.07 | 322.98 |

Fabless average annual revenue increased by 392.44% between the first and third periods, the largest percentage increase among the five groups. This is a comparison of period averages, not a CAGR.

The EDA notebook also contains revenue trends, company rankings, concentration, investment-growth correlations, and flag-exclusion sensitivity checks. Historical rankings and growth analyses retain their explicitly stated 2024 endpoint.

## Interpretation limits

The AI expansion comparison includes 2025–2026 records requiring source validation. Period names are project definitions. Coverage differs over time, shares refer only to this dataset, and associations do not establish causation.

## Files

- `financials_clean.csv` and `financials_features.csv`: fresh processed datasets.
- `02_data_preprocessing.ipynb` through `05_visualization.ipynb`: executed notebooks.
- `figures/`: seven regenerated charts.

This run uses a separate output folder because Windows denied overwriting the existing financials_clean.csv.
