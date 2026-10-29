# SA People and Safety Data Pipeline

## 🎥 Demo Video

[Watch the 5-10 minute demo on YouTube (unlisted)](https://youtu.be/eMwdhKq-KJ0)

The video walks through the pipeline end to end: collecting SAPS crime and Stats SA QLFS data, cleaning and validating it, loading it into SQLite, analysing crime against unemployment by province, and re-running everything with `run_pipeline.py`.

## 1. Overview
An end-to-end data pipeline that collects official South African statistics (Stats SA and SAPS), cleans and validates them, stores them in a database, analyses them statistically, and presents the findings in a dashboard. One command rebuilds everything from scratch.

This project is built around three parts of data work:

- **Data engineering**: a reliable, automated pipeline — extract, clean, validate, load — that re-runs end to end with one command and logs every step
- **Data analytics**: descriptive statistics, trend lines and a dashboard that present what the data shows
- **Data science**: correlation testing (Pearson and Spearman) with confidence intervals and p-values, plus an honest account of what the results do and don't prove

## 2. Research questions
1. How have unemployment and selected crime categories changed by province over time?
2. Do provinces with higher unemployment tend to have higher crime rates?

Note: this project measures correlation only. It does not claim unemployment causes crime.

## 3. Data sources
- SAPS: national and provincial crime statistics, financial years 2015/16 to 2024/25
- Stats SA: Quarterly Labour Force Survey, official unemployment rate by province, same period
- Full details and known issues: docs/data-sources.md

## 4. Pipeline stages
1. Extract: downloads the raw files into data/raw/
2. Clean: fixes column names, missing values, types, province names and year mismatches
3. Validate: automatic data quality checks (see section 5)
4. Load: writes cleaned data into a SQLite database with linked tables
5. Analyse: descriptive statistics, trend analysis, correlation testing
6. Visualise: builds the charts
7. Dashboard: builds a self-contained HTML dashboard from the charts and results
8. Automate: run_pipeline.py runs every stage above in order

## 5. Data quality checks
- No missing province or year
- No duplicate rows
- No negative counts or rates
- Province names match one standard list
- Values fall within sensible ranges
- Row counts are compared before and after cleaning
- Failed checks are written to the log and stop the run

## 6. Database design
Tables: provinces, years, unemployment, crime_stats, with province and year as shared keys.

## 7. Statistical methods
- Descriptive statistics (mean, median, spread)
- Trend analysis over time (linear trend per province)
- Correlation (Pearson and Spearman) with confidence intervals and p-values
- Clear limitations: small sample size, multiple comparisons, correlation vs causation (see docs/report.md)

## 8. Logging and re-runnability
- Every run writes a timestamped log (steps done, row counts, checks passed or failed)
- The pipeline can be deleted and rebuilt from scratch with one command
- Re-running never creates duplicate rows

## 9. Tech stack
Python, pandas, SQLite, matplotlib, scipy/statsmodels, Git and GitHub

## 10. Documentation
- docs/data-sources.md: data sources, known issues, and how they changed during the project
- docs/daily-log.md: progress log
- docs/data-dictionary.md: every column, its source, meaning and how it was cleaned
- docs/report.md: findings, method and limitations

## 11. Repo structure
- README.md
- run_pipeline.py
- data/ (raw/, clean/)
- src/ (extract.py, clean.py, validate.py, load.py, analyse.py, visualise.py, dashboard.py)
- outputs/ (charts, tables, dashboard.html) — generated, not committed
- logs/
- docs/

## 12. Deliverables
- Working pipeline with one-command re-run
- SQLite database
- Charts and dashboard
- Data dictionary and final report
- Short demo video
