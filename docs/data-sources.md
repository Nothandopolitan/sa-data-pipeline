# Data Sources

## Analysis period
2008 to 2015, where both sources overlap.

## 1. SAPS crime statistics (national and provincial)
- Publisher: South African Police Service (SAPS)
- Copy used: national and provincial crime statistics 2005 to 2015, republished by Code4SA on openAFRICA
- Format: CSV
- Download: https://data.code4sa.org/api/views/pknu-xarf/rows.csv?accessType=DOWNLOAD
- Period: financial years (April to March)
- Licence: not specified on the source page
- To do: spot-check some totals against the official SAPS release

## 2. Stats SA Quarterly Labour Force Survey (QLFS)
- Publisher: Statistics South Africa
- Measure: official unemployment rate by province
- Format: quarterly release PDFs (publication P0211) with a provincial unemployment table. No ready-made download found yet.
- Other route: raw survey data through DataFirst (needs registration, much heavier)
- Period: most series start in 2008 Q1
- Licence: to confirm on statssa.gov.za
- Plan: extract the provincial table from each release, probably one quarter per year (see data/raw/qlfs/README.md)

## Known data issues
- Crime is per financial year, unemployment is quarterly. Quarters are averaged per financial year.
- Q1 2015: Stats SA redesigned the survey sample and unemployment jumped about 2 points. This break is flagged in the analysis.
- Stats SA has changed its unemployment definitions recently. Only the official rate is used.
- Province names may differ between sources and need one standard list.
- Small sample: 9 provinces over 7 to 8 years.
- Crime data ends in 2015, so findings are historical.
