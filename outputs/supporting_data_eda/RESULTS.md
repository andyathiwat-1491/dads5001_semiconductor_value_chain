# Supporting datasets: cleaning, EDA, and visualization

Completed analysis of all four supporting files. No rows removed, no raw files modified, and original numeric values preserved.

## Dataset audit

| Dataset | Rows | Years | Missing original cells | Duplicate keys |
|---|---:|---|---:|---:|
| ai_chip_market | 120 | 2020–2026 | 0 | 0 |
| chip_prices | 405 | 2014–2026 | 0 | 0 |
| fab_capacity | 313 | 2011–2026 | 0 | 0 |
| export_controls | 34 | 2018–2026 | 0 | 0 |

## What was done

| Dataset | Cleaning and structure | EDA and charts |
|---|---|---|
| AI chips | Explicit day/month/year launch-date parsing; zero-price, zero-memory, pre-launch and revenue-reconciliation flags; safe performance ratios. | Annual shipments/revenue, vendor shares, coverage, and exact-name financial context. Market values are estimates. |
| Prices | Parse year-month, verify year, order each product series, check monthly gaps, calculate consecutive-month changes and indexes. | Original-unit panels, common October 2024 price index, annual averages with month counts. |
| Capacity | Verify unique company/country/node/type/year records; separate fabrication from packaging; flag zero capacity and pre-start years. | Annual, company and country summaries within factory type; type-specific trend panels. |
| Export controls | Parse explicit day/month/year dates; compare date components and country flags; retain undocumented severity scores with a review flag. | Recorded event counts and timeline; aligned financial context without causal claims. |

## Your periods and coverage

2010–2021 = Smart automobile expansion; 2022 = Transition Year; 2023–2026 = AI expansion. Coverage is not assumed to span each full period. See tables/period_coverage.csv. Prices run only through April 2026; product launches also produce partial first years. Annual price means are not full-year means unless full_year_coverage is true.

## Review flags

| Dataset | Flag | Rows |
|---|---|---:|
| ai_chip_market | before_launch_year_flag | 0 |
| ai_chip_market | zero_asp_flag | 7 |
| ai_chip_market | zero_memory_flag | 3 |
| ai_chip_market | revenue_review_flag | 0 |
| chip_prices | year_mismatch_flag | 0 |
| chip_prices | consecutive_month_flag | 400 |
| chip_prices | nonpositive_price_flag | 0 |
| fab_capacity | zero_capacity_flag | 38 |
| fab_capacity | before_start_year_flag | 0 |
| fab_capacity | wafer_basis_unverified | 313 |
| export_controls | date_components_review_flag | 0 |
| export_controls | severity_definition_unverified | 34 |
| export_controls | country_indicator_review_flag | 0 |

## Integration and interpretation

- Annual financial, AI, and policy tables are joined one-to-one by year. Missing out-of-coverage values remain missing.
- Vendor/company joins use exact names and many-to-one validation. Unmatched names are documented; no guessed subsidiary mappings.
- AI estimated revenue and total financial revenue have different scopes and must not be added or interpreted as reconciled components.
- Monthly wafer capacity is a capacity measure, not actual output. Factory IDs and wafer-equivalence definitions are absent; within-type sums are descriptive sums of supplied records, not verified industry totals. Packaging and fabrication are never pooled.
- Policy counts represent events listed in this file; zero means none recorded. Severity scores and administration indicators are not externally verified or used as causal exposure measures.
- Cross-chip performance ratios are nominal descriptors, not comparable benchmark results: architectures, precision conventions, and system boundaries differ. These ratios are not used to rank products in charts.
- 2025–2026 remain source-review years. All underlying source claims are unverified; this workflow is a data-quality and descriptive analysis, not external factual validation.

## Files

- clean/: four cleaned CSVs.
- tables/: audit, coverage, review flags, annual summaries and validated links.
- figures/: eight PNG charts.
- Notebook: notebooks/06_supporting_data_eda.ipynb.
- Re-run: python src/supporting_data_analysis.py

Source provenance recorded in docs/data_sources.txt: Kaggle Global Semiconductor Industry 2010–2026. Source contents were not independently verified.

## Descriptive findings

- 2022: AI-chip dataset estimated revenue was USD 2.28 billion across 8 products. Changing product coverage contributes to comparability limits.
- 2023: AI-chip dataset estimated revenue was USD 23.61 billion across 15 products. Changing product coverage contributes to comparability limits.
- 2024: AI-chip dataset estimated revenue was USD 109.82 billion across 26 products. Changing product coverage contributes to comparability limits.
- DRAM_DDR4_8Gb: price changed +4.3% from October 2024 to April 2026 in the common-window index; 2025–2026 require source review.
- HBM3_stack: price changed +22.5% from October 2024 to April 2026 in the common-window index; 2025–2026 require source review.
- NAND_64Gb_MLC: price changed +4.9% from October 2024 to April 2026 in the common-window index; 2025–2026 require source review.
- NVIDIA_B200: price changed -28.1% from October 2024 to April 2026 in the common-window index; 2025–2026 require source review.
- NVIDIA_H100: price changed -34.2% from October 2024 to April 2026 in the common-window index; 2025–2026 require source review.
- Packaging records cover only [np.int64(2026)]; a packaging time trend cannot be inferred from one observed year.
- Recorded event counts were 4 in 2022, 7 in 2023, and 6 in 2024. These are dataset event counts, not calibrated policy severity or causal effects.
