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
