# Daily Log

## 12 Oct
- Planned the data pipeline project and wrote the full README
- Chose Stats SA and SAPS as the data sources (still to confirm the files)
- Next: confirm the datasets and set up the notebook environment

## 13 Oct
- Researched and confirmed the data sources (SAPS provincial crime CSV, Stats SA QLFS)
- Chose 2008 to 2015 as the analysis period, where both overlap
- Noted known data issues: financial year vs quarterly data, QLFS break in Q1 2015, small sample
- Next: download the raw data and write the extract script

## 14 Oct
- Added config, logging setup and the pipeline stage files
- Wrote the SAPS download in the extract stage
- Found that Stats SA data comes as PDF release tables, so the plan changed to extracting tables from PDFs
- Next: run the extract stage, then clean the SAPS data
