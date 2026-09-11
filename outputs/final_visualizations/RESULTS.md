# Final visualization conclusions

Project: From Automotive AI to Generative AI: The Changing Semiconductor Value Chain.

Seven additional figures numbered 8-14. Each is saved in PNG (300 DPI) and PDF in figures/final/. Figure 13 is the explicitly requested October 2024-April 2026 source-review exception; financial conclusions end in 2024.

| Figure | Main finding | Business implication | Possible action | Limitation |
|---|---|---|---|---|
| 8 | Revenue increased from $235.00bn in 2010 to $828.51bn in 2024; entity coverage increased from 33 to 40. | Aggregate growth includes a changing set of represented entities. | Compare the aggregate with a fixed-company panel before attributing changes to company performance. | Dataset coverage changes; period labels do not establish causation. |
| 9 | Fabless average annual revenue increased 252.8% between the first and third periods. | Value-chain roles had different revenue trajectories. | Compare group margins and R&D/CapEx intensity alongside revenue; check a fixed-company comparison. | Unequal periods are addressed with annual averages, but changing entity coverage and long-run trends remain. |
| 10 | NVIDIA led absolute growth, rising from $26.12bn to $130.48bn. | A large company can drive aggregate dollar growth even when smaller firms grow faster in percentage terms. | Separate absolute contribution from percentage-growth rankings in the project presentation. | Positive-endpoint eligibility and dataset coverage define this ranking; the chart does not establish causes. |
| 11 | The top five represented 48.63% in 2024. Excluding NVIDIA reduces the total from $828.51bn to $698.03bn. | Headline totals can be sensitive to a dominant entity. | Present aggregate and largest-company-excluded results together when discussing breadth of growth. | A 2024 exclusion alone does not quantify growth contributions across time or establish causation. |
| 12 | Estimated revenue rose from $2.28bn to $109.82bn; products increased from 8 to 26. NVIDIA represented 76.0% of 2024 estimated dataset revenue. | Estimated growth reflects a widening observed product set as well as changes in estimates. | Validate estimates and compare a fixed-product cohort before making demand projections. | AI revenue is estimated, zero-price records remain, and coverage changes. Do not interpret these as verified global market shares. |
| 13 | HBM3 increased 22.5%; H100 and B200 changed -34.2% and -28.1%, respectively. | Product price cycles differ; a single semiconductor price trend can conceal opposing movements. | Track product-specific price indexes and verify later-year source values before using them for planning. | 2025-2026 are unverified source-review years; 2026 is partial, and product specifications and price bases differ. |
| 14 | Leading-edge logic records sum to 459.1k in 2022 and 709.9k wafers/month in 2024. Recorded events number 4, 7 and 6 in 2022-2024. | Capacity and policy provide distinct context for financial results. | Validate capacity additions, wafer definitions and event details before drawing supply or policy-impact conclusions. | Capacity record coverage changes and wafer equivalence is unverified. Counts are neither policy severity nor causal estimates. |

## Findings supported by supplied data

Revenue, entity/product coverage, rankings, concentration, prices, reported capacity and event counts are calculated from the supplied data. Computation checks passed; these are not independent factual verification.

## Associations that do not establish causation

Analytical period labels, contemporaneous policy events, and capacity movements do not prove automotive AI or Generative AI caused financial changes. The largest-company exclusion is a descriptive sensitivity check.

## Values requiring independent verification

AI-chip revenue is estimated. Figure 13 includes source-review years 2025-2026 and partial-year 2026 prices. Capacity totals are sums of reported records; wafer equivalence and global coverage are unverified. Policy counts are not severity scores.

## Library use

Pandas: reading processed CSVs, filtering, groupby/aggregation, pivoting, validated joins, shares, ranking, coverage, and tables. Matplotlib: all seven plots, subplots, annotations, tables, legends, date/number formatting, and high-resolution PNG/PDF export. No Seaborn, NumPy or Plotly is used in this notebook, following the supplied instructions.

## Validation

Seven PNGs and seven PDFs generated; financial charts end in 2024; protected CSVs and previous notebooks unchanged; unique company-year keys and join cardinality checked; yearly revenue shares reconcile to 100%; no infinite chart inputs; titles, axis labels and notes checked. PNG opacity and resolution checked programmatically. PDF exports request opaque white backgrounds; rendered PDF pages are reviewed separately.

## Saved files

- figures\final\figure_08_financial_revenue_coverage.png
- figures\final\figure_08_financial_revenue_coverage.pdf
- figures\final\figure_09_value_chain_periods.png
- figures\final\figure_09_value_chain_periods.pdf
- figures\final\figure_10_company_absolute_growth.png
- figures\final\figure_10_company_absolute_growth.pdf
- figures\final\figure_11_concentration_sensitivity.png
- figures\final\figure_11_concentration_sensitivity.pdf
- figures\final\figure_12_estimated_ai_revenue_coverage.png
- figures\final\figure_12_estimated_ai_revenue_coverage.pdf
- figures\final\figure_13_product_price_index.png
- figures\final\figure_13_product_price_index.pdf
- figures\final\figure_14_capacity_policy_context.png
- figures\final\figure_14_capacity_policy_context.pdf
