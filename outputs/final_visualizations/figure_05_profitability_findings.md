# Figure 5: profitability by business model

EDA Software led the pooled ten-year median (40.8%). IDM had the largest 2023 decline (-11.0 percentage points).

## Measures and validation

Company medians and quartiles use operating_margin_pct, the existing operating-margin field. Revenue and operating income are revenue_usd_bn and operating_income_usd_bn. Weighted margins use sum(operating_income_usd_bn) / sum(revenue_usd_bn) * 100 on the same valid observations. No arithmetic mean of company percentages is used for weighting.
372 company-year records, 40 distinct companies, 8 exclusions, no duplicates. The eight exclusions have zero revenue, making income/revenue undefined. Required numeric missing counts: {'revenue_usd_bn': 0, 'operating_income_usd_bn': 0, 'operating_margin_pct': 0}. Numeric conversion failures: {'year': 0, 'revenue_usd_bn': 0, 'operating_income_usd_bn': 0, 'operating_margin_pct': 0}.
0 negative margins are present; no loss observations were deliberately removed. 11 observations are flagged using pooled within-group 1.5-IQR fences and retained.
18 observations differ by more than 1 percentage point between supplied margins and ratios of rounded amounts. These discrepancies are concentrated in small firms. The supplied margin is retained; rounded-dollar weighted measures are reported separately. Source values have not been independently verified.

## Robustness comparison

| group        |   companies |   valid_observations |   ten_year_median |   weighted_margin |   median_2022 |   median_2023 |   median_2024 |   change_2022_2023_pp |
|:-------------|------------:|---------------------:|------------------:|------------------:|--------------:|--------------:|--------------:|----------------------:|
| EDA Software |           2 |                   20 |             40.8  |            40.057 |         40.85 |          38.3 |          39.1 |                 -2.55 |
| Foundry      |           6 |                   60 |             39.65 |            39.898 |         39.35 |          37.9 |          38.8 |                 -1.45 |
| Equipment    |           6 |                   60 |             30.7  |            31.396 |         30.7  |          29.5 |          30.5 |                 -1.2  |
| Fabless      |          12 |                   89 |             26.7  |            34.924 |         23.7  |          17.6 |          24.5 |                 -6.1  |
| IDM          |          14 |                  135 |             26.3  |            26.592 |         33.2  |          22.2 |          27.6 |                -11    |

## Interpretation

EDA Software leads the pooled company-year median at 40.80%. The highest pooled revenue-weighted margin belongs to EDA Software at 40.06%; EDA remains narrowly first under weighting, but Fabless moves above Equipment. The ranking below the leader depends on the weighting method. Large-company influence should not be confused with the typical company.
The fastest represented-group revenue growth over 2015-2024 is Fabless, with a 19.65% CAGR (nine annual intervals). This is different from profitability: EDA Software has the highest median margin. Group revenue growth also reflects changing coverage.
All five group medians declined in 2023. The largest deterioration was IDM, -11.00 percentage points. This coincided with the represented-company revenue downturn; it does not establish causality.
Unlike medians, weighted margins increased in 2023 for Foundry, Fabless and Equipment, while IDM and EDA declined. This shows that the typical-company downturn was not uniform when revenue-weighted. Weighted Equipment margin declined in 2024 despite its median recovery.
All five group medians rose in 2024. EDA Software: +0.80 pp recovery, -1.75 pp versus 2022; Foundry: +0.90 pp recovery, -0.55 pp versus 2022; Equipment: +1.00 pp recovery, -0.20 pp versus 2022; Fabless: +6.90 pp recovery, +0.80 pp versus 2022; IDM: +5.40 pp recovery, -5.60 pp versus 2022.
EDA Software has only two represented companies in each year; its medians are based on limited coverage. Foundry and Equipment each have six per year. Fabless and IDM coverage changes; this is not a balanced-company panel.
Fabless and EDA Software are relatively asset-light; Foundry and IDM require manufacturing investment; Equipment supplies production technology and machinery. These descriptions do not demonstrate that business model caused the observed differences. Product mix, accounting, composition and coverage can also matter.
Operating margin measures operating income per revenue dollar, not absolute operating profit. Revenue growth is a separate metric. Differences between margins are expressed in percentage points. A company median weights observations equally, while the ratio of total operating income to total revenue emphasizes larger firms.

## Annual statistics and coverage

| group        |   year |   companies |   valid_observations |   median_margin |   weighted_margin |    q25 |    q75 |
|:-------------|-------:|------------:|---------------------:|----------------:|------------------:|-------:|-------:|
| Foundry      |   2015 |           6 |                    6 |           39.85 |            40.907 | 39.225 | 40.55  |
| Foundry      |   2016 |           6 |                    6 |           40.25 |            41.725 | 38.8   | 40.65  |
| Foundry      |   2017 |           6 |                    6 |           38.15 |            38.205 | 37.025 | 39.8   |
| Foundry      |   2018 |           6 |                    6 |           38.9  |            38.769 | 38.425 | 40.95  |
| Foundry      |   2019 |           6 |                    6 |           40.25 |            40.075 | 39.925 | 41.7   |
| Foundry      |   2020 |           6 |                    6 |           40.05 |            38.974 | 38.275 | 42.5   |
| Foundry      |   2021 |           6 |                    6 |           40.4  |            40.366 | 39.55  | 42.6   |
| Foundry      |   2022 |           6 |                    6 |           39.35 |            39.413 | 38.075 | 42.125 |
| Foundry      |   2023 |           6 |                    6 |           37.9  |            39.955 | 37.275 | 38.825 |
| Foundry      |   2024 |           6 |                    6 |           38.8  |            40.574 | 37.075 | 41.05  |
| Fabless      |   2015 |           7 |                    7 |           27.9  |            29.952 | 27     | 30.6   |
| Fabless      |   2016 |           7 |                    7 |           28.6  |            32.268 | 26.95  | 31.2   |
| Fabless      |   2017 |           7 |                    7 |           29.4  |            31.224 | 26.35  | 30     |
| Fabless      |   2018 |           7 |                    7 |           29.7  |            32.305 | 26.25  | 32.3   |
| Fabless      |   2019 |           9 |                    7 |           28.9  |            32.489 | 24.9   | 31.35  |
| Fabless      |   2020 |          12 |                    7 |           26.2  |            30.43  | 24.1   | 30.25  |
| Fabless      |   2021 |          12 |                   11 |           25.6  |            34.218 | 12.45  | 29.85  |
| Fabless      |   2022 |          12 |                   12 |           23.7  |            31.654 | 11.825 | 30.025 |
| Fabless      |   2023 |          12 |                   12 |           17.6  |            36.122 |  8.2   | 24.625 |
| Fabless      |   2024 |          12 |                   12 |           24.5  |            41.812 | 10.45  | 28.175 |
| IDM          |   2015 |          12 |                   12 |           20.5  |            21.147 | 18.25  | 30.3   |
| IDM          |   2016 |          12 |                   12 |           20.95 |            21.951 | 18.85  | 30.65  |
| IDM          |   2017 |          13 |                   13 |           24.1  |            22.19  | 19.9   | 26.9   |
| IDM          |   2018 |          14 |                   14 |           30.3  |            27.539 | 19.15  | 33.1   |
| IDM          |   2019 |          14 |                   14 |           34.1  |            32.193 | 22.625 | 39.2   |
| IDM          |   2020 |          14 |                   14 |           35.4  |            30.158 | 20.65  | 40.425 |
| IDM          |   2021 |          14 |                   14 |           37.05 |            31.691 | 20.025 | 41.475 |
| IDM          |   2022 |          14 |                   14 |           33.2  |            28.836 | 18.775 | 42.125 |
| IDM          |   2023 |          14 |                   14 |           22.2  |            21.582 | 13.925 | 26.65  |
| IDM          |   2024 |          14 |                   14 |           27.6  |            24.673 | 21.95  | 31.2   |
| Equipment    |   2015 |           6 |                    6 |           29.9  |            31.037 | 26.675 | 34.7   |
| Equipment    |   2016 |           6 |                    6 |           30.8  |            28.494 | 24.075 | 33.775 |
| Equipment    |   2017 |           6 |                    6 |           34.8  |            34.239 | 33.05  | 35.275 |
| Equipment    |   2018 |           6 |                    6 |           30.35 |            31.118 | 28.825 | 34.275 |
| Equipment    |   2019 |           6 |                    6 |           29.8  |            30.32  | 27.9   | 31.25  |
| Equipment    |   2020 |           6 |                    6 |           33.45 |            33.814 | 28.4   | 35.65  |
| Equipment    |   2021 |           6 |                    6 |           31.45 |            32.352 | 29.3   | 35.325 |
| Equipment    |   2022 |           6 |                    6 |           30.7  |            30.146 | 25.6   | 33.025 |
| Equipment    |   2023 |           6 |                    6 |           29.5  |            32.048 | 29     | 34.2   |
| Equipment    |   2024 |           6 |                    6 |           30.5  |            30.305 | 23.375 | 32.75  |
| EDA Software |   2015 |           2 |                    2 |           40.5  |            40.648 | 40.45  | 40.55  |
| EDA Software |   2016 |           2 |                    2 |           42    |            42.13  | 41.75  | 42.25  |
| EDA Software |   2017 |           2 |                    2 |           38.9  |            38.608 | 38.35  | 39.45  |
| EDA Software |   2018 |           2 |                    2 |           40.1  |            40.421 | 39.2   | 41     |
| EDA Software |   2019 |           2 |                    2 |           41.5  |            41.297 | 41.25  | 41.75  |
| EDA Software |   2020 |           2 |                    2 |           40.9  |            40.625 | 39.9   | 41.9   |
| EDA Software |   2021 |           2 |                    2 |           40.7  |            40.808 | 40.5   | 40.9   |
| EDA Software |   2022 |           2 |                    2 |           40.85 |            41.487 | 39.125 | 42.575 |
| EDA Software |   2023 |           2 |                    2 |           38.3  |            37.782 | 36.65  | 39.95  |
| EDA Software |   2024 |           2 |                    2 |           39.1  |            38.825 | 38     | 40.2   |

## Period and growth summary

| group        |   companies |   valid_observations |   ten_year_median |   weighted_margin |    q25 |    q75 |    iqr |   average_median_2015_2019 |   average_median_2020_2022 |   median_2022 |   median_2023 |   median_2024 |   change_2022_2023_pp |   recovery_2023_2024_pp |   revenue_cagr_2015_2024_pct |   revenue_change_2022_2023_pct |
|:-------------|------------:|---------------------:|------------------:|------------------:|-------:|-------:|-------:|---------------------------:|---------------------------:|--------------:|--------------:|--------------:|----------------------:|------------------------:|-----------------------------:|-------------------------------:|
| EDA Software |           2 |                   20 |             40.8  |            40.057 | 38.75  | 41.675 |  2.925 |                      40.6  |                     40.817 |         40.85 |          38.3 |          39.1 |                 -2.55 |                     0.8 |                       11.146 |                         16.787 |
| Foundry      |           6 |                   60 |             39.65 |            39.898 | 38     | 41.15  |  3.15  |                      39.48 |                     39.933 |         39.35 |          37.9 |          38.8 |                 -1.45 |                     0.9 |                       12.257 |                        -11.871 |
| Equipment    |           6 |                   60 |             30.7  |            31.396 | 27.225 | 35.175 |  7.95  |                      31.13 |                     31.867 |         30.7  |          29.5 |          30.5 |                 -1.2  |                     1   |                       13.753 |                          7.701 |
| Fabless      |          12 |                   89 |             26.7  |            34.924 | 18.2   | 30.5   | 12.3   |                      28.9  |                     25.167 |         23.7  |          17.6 |          24.5 |                 -6.1  |                     6.9 |                       19.655 |                         14.577 |
| IDM          |          14 |                  135 |             26.3  |            26.592 | 19.6   | 40.2   | 20.6   |                      25.99 |                     35.217 |         33.2  |          22.2 |          27.6 |                -11    |                     5.4 |                        6.37  |                        -19.027 |
