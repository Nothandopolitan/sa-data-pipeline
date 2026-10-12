# SA People and Safety Data Pipeline

## 1. Overview
An end-to-end data pipeline that collects official South African statistics (Stats SA and SAPS), cleans and validates them, stores them in a database, analyses them statistically, and presents the findings in charts and a dashboard. One command re-runs everything from scratch.

## 2. Goals
- Data engineering: build a reliable, automated pipeline
- Data analytics: explore the data and present clear findings
- Statistics: test relationships properly and state the limits of the results
- Quality: validate the data, document it, and log every run
- 
## 3. Research questions
1. How have unemployment and selected crime categories changed by province over time?
2. Do provinces with higher unemployment tend to have higher crime rates?
3. What does a simple forecast say about the next period?

Note: this project measures correlation only. It does not claim unemployment causes crime.

## 4. Data sources
- Stats SA: unemployment and population by province
- SAPS: crime statistics by province
- (Confirm exact files, formats and licences on day 1)

## 5. Pipeline stages
1. Extract: script downloads and loads the raw files into data/raw/
2. Clean: fix column names, missing values, types, province names and year mismatches
3. Validate: automatic data quality checks (see section 6)
4. Load: write cleaned data into a SQLite database with linked tables
5. Analyse: exploration, statistics, forecast
6. Visualise: charts and a dashboard
7. Automate: run_pipeline.py runs stages 1-6 in order

## 6. Data quality checks
- No missing province or year
- No duplicate rows
- No negative counts or rates
- Province names match one standard list
- Values fall within sensible ranges
- Row counts are compared before and after cleaning
- Failed checks are written to the log and stop the run

## 7. Database design
Tables: provinces, years, unemployment, crime_stats, with province and year as shared keys. Schema diagram stored in docs/.

## 8. Statistical methods
- Descriptive statistics (mean, median, spread)
- Trend analysis over time
- Correlation (Pearson and Spearman) with p-values
- Simple forecast (linear regression or moving average)
- Confidence intervals on key results
- Clear limitations (small sample, other factors, reporting differences)

## 9. Logging and re-runnability
- Every run writes a timestamped log (steps done, row counts, checks passed or failed)
- The pipeline can be deleted and rebuilt from scratch with one command
- Re-running never creates duplicate rows

## 10. Tech stack
Python, pandas, SQLite, matplotlib, scipy/statsmodels, Google Colab or Codespaces, Git and GitHub

## 11. Timeline
| Date | Task |
|---|---|
| Tue 13 Oct | Create repo, README, find and confirm datasets |
| Wed 14 Oct | Download raw data, write the extract script |
| Thu 15 Oct | Inspect raw data, list the problems found |
| Fri 16 Oct | Clean the Stats SA data |
| Sat 17 Oct | Clean the SAPS data, standardise province names |
| Sun 18 Oct | Write the data quality checks |
| Mon 19 Oct | Design the database and load the data |
| Tue 20 Oct | Add logging, build run_pipeline.py |
| Wed 21 Oct | Exploratory analysis |
| Thu 22 Oct | Correlation and trend statistics |
| Fri 23 Oct | Forecast and confidence intervals |
| Sat 24 Oct | Build the charts |
| Sun 25 Oct | Build the dashboard |
| Mon 26 Oct | Data dictionary and limitations section |
| Tue 27 Oct | Full re-run from scratch test, write the report |
| Wed 28 Oct | Polish README, record demo, submit |
