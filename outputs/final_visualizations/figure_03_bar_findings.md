# Figure 3: profitability across three periods

EDA Software had the highest eleven-year median (40.5%); IDM changed most in 2023-2025 (-9.15 percentage points versus 2022).

Operating margin measures the proportion of revenue remaining after operating expenses, before interest and taxes. Higher margin indicates greater operating profitability per revenue dollar, not necessarily the largest absolute operating profit.
Existing operating_margin_pct is used for company medians. revenue_usd_bn and operating_income_usd_bn are used for validity checks and revenue weighting. Supplied margins are retained rather than reconstructed from rounded dollar amounts. Each bar is the direct median of all valid company-year observations in the period, not an average of annual medians.
EDA Software leads the overall pooled eleven-year median. Equipment has the smallest range across the three period medians (1.00 percentage points). This is stability of period medians, not proof of company-level or annual stability.
The largest absolute change is IDM: -9.15 percentage points from 2022 to 2023-2025. These pooled-period comparisons do not isolate the 2023 downturn from the 2024-2025 recovery.
Weighted margin leaders by period: 2015-2021: EDA Software (40.66%); 2022: EDA Software (41.49%); 2023-2025: Fabless (42.54%). Weighting favors larger firms and can change rankings.
The dataset has no missing revenue or operating-income values in this window and no duplicate company-years. Eight zero-revenue rows are flagged and excluded. There are no negative margins among valid observations. 13 within-group IQR extremes are flagged and retained.
EDA Software has only two companies in each period. Group composition and observation counts differ across periods. Company-year pooling gives more weight to companies with more observed years. Period medians are descriptive, not global industry estimates or evidence that business models caused the differences.

## Validation table

| group        | period    |   companies |   valid_observations |   median_operating_margin |
|:-------------|:----------|------------:|---------------------:|--------------------------:|
| EDA Software | 2015-2021 |           2 |                   14 |                     40.8  |
| EDA Software | 2022      |           2 |                    2 |                     40.85 |
| EDA Software | 2023-2025 |           2 |                    6 |                     39.3  |
| Foundry      | 2015-2021 |           6 |                   42 |                     39.95 |
| Foundry      | 2022      |           6 |                    6 |                     39.35 |
| Foundry      | 2023-2025 |           6 |                   18 |                     38.9  |
| Equipment    | 2015-2021 |           6 |                   42 |                     31.5  |
| Equipment    | 2022      |           6 |                    6 |                     30.7  |
| Equipment    | 2023-2025 |           6 |                   18 |                     30.5  |
| Fabless      | 2015-2021 |          12 |                   53 |                     28.4  |
| Fabless      | 2022      |          12 |                   12 |                     23.7  |
| Fabless      | 2023-2025 |          12 |                   36 |                     20.35 |
| IDM          | 2015-2021 |          14 |                   93 |                     26.3  |
| IDM          | 2022      |          14 |                   14 |                     33.2  |
| IDM          | 2023-2025 |          14 |                   42 |                     24.05 |

## Weighted robustness table

| group        | period    |   weighted_operating_margin |
|:-------------|:----------|----------------------------:|
| EDA Software | 2015-2021 |                      40.659 |
| EDA Software | 2022      |                      41.487 |
| EDA Software | 2023-2025 |                      38.664 |
| Foundry      | 2015-2021 |                      39.82  |
| Foundry      | 2022      |                      39.413 |
| Foundry      | 2023-2025 |                      39.96  |
| Equipment    | 2015-2021 |                      31.823 |
| Equipment    | 2022      |                      30.146 |
| Equipment    | 2023-2025 |                      31.408 |
| Fabless      | 2015-2021 |                      32.064 |
| Fabless      | 2022      |                      31.654 |
| Fabless      | 2023-2025 |                      42.543 |
| IDM          | 2015-2021 |                      27.261 |
| IDM          | 2022      |                      28.836 |
| IDM          | 2023-2025 |                      23.303 |

## Dispersion and coverage

| group        | period    |   companies |   valid_companies |   valid_observations |   median_operating_margin |   weighted_operating_margin |   company_year_iqr |
|:-------------|:----------|------------:|------------------:|---------------------:|--------------------------:|----------------------------:|-------------------:|
| EDA Software | 2015-2021 |           2 |                 2 |                   14 |                     40.8  |                      40.659 |              1.725 |
| EDA Software | 2022      |           2 |                 2 |                    2 |                     40.85 |                      41.487 |              3.45  |
| EDA Software | 2023-2025 |           2 |                 2 |                    6 |                     39.3  |                      38.664 |              3.35  |
| Foundry      | 2015-2021 |           6 |                 6 |                   42 |                     39.95 |                      39.82  |              2.825 |
| Foundry      | 2022      |           6 |                 6 |                    6 |                     39.35 |                      39.413 |              4.05  |
| Foundry      | 2023-2025 |           6 |                 6 |                   18 |                     38.9  |                      39.96  |              3.875 |
| Equipment    | 2015-2021 |           6 |                 6 |                   42 |                     31.5  |                      31.823 |              7.65  |
| Equipment    | 2022      |           6 |                 6 |                    6 |                     30.7  |                      30.146 |              7.425 |
| Equipment    | 2023-2025 |           6 |                 6 |                   18 |                     30.5  |                      31.408 |              9.575 |
| Fabless      | 2015-2021 |          12 |                11 |                   53 |                     28.4  |                      32.064 |              5.8   |
| Fabless      | 2022      |          12 |                12 |                   12 |                     23.7  |                      31.654 |             18.2   |
| Fabless      | 2023-2025 |          12 |                12 |                   36 |                     20.35 |                      42.543 |             20.675 |
| IDM          | 2015-2021 |          14 |                14 |                   93 |                     26.3  |                      27.261 |             20.8   |
| IDM          | 2022      |          14 |                14 |                   14 |                     33.2  |                      28.836 |             23.35  |
| IDM          | 2023-2025 |          14 |                14 |                   42 |                     24.05 |                      23.303 |              8.4   |
