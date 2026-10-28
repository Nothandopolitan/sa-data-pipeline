import logging
import os
import sqlite3
import pandas as pd

log = logging.getLogger('pipeline')
DB = 'data/pipeline.db'

SCHEMA = """
CREATE TABLE provinces (
    province_id   INTEGER PRIMARY KEY,
    province_name TEXT NOT NULL UNIQUE
);
CREATE TABLE years (
    year           INTEGER PRIMARY KEY,   -- start year of the financial year
    financial_year TEXT NOT NULL          -- e.g. 2015-2016 (April to March)
);
CREATE TABLE unemployment (
    province_id  INTEGER NOT NULL REFERENCES provinces(province_id),
    year         INTEGER NOT NULL REFERENCES years(year),
    unemp_rate   REAL NOT NULL,           -- % (official rate, averaged over 4 quarters)
    pop_thousand REAL NOT NULL,           -- working age 15-64, thousands, averaged
    n_quarters   INTEGER NOT NULL,
    PRIMARY KEY (province_id, year)
);
CREATE TABLE crime_stats (
    province_id   INTEGER NOT NULL REFERENCES provinces(province_id),
    year          INTEGER NOT NULL REFERENCES years(year),
    crime_category TEXT NOT NULL,
    count         INTEGER NOT NULL,
    rate_per_100k REAL NOT NULL,          -- per 100,000 working-age people (15-64)
    PRIMARY KEY (province_id, year, crime_category)
);
"""


def load():
    crime = pd.read_csv('data/clean/crime.csv')
    unemp = pd.read_csv('data/clean/unemployment.csv')

    if os.path.exists(DB):
        os.remove(DB)                       # rebuild from scratch, so no duplicates
    con = sqlite3.connect(DB)
    con.execute('PRAGMA foreign_keys = ON')
    con.executescript(SCHEMA)

    provinces = pd.DataFrame({'province_name': sorted(unemp['Province'].unique())})
    provinces.insert(0, 'province_id', range(1, len(provinces) + 1))
    provinces.to_sql('provinces', con, if_exists='append', index=False)
    pid = dict(zip(provinces['province_name'], provinces['province_id']))

    yrs = sorted(unemp['year'].unique())
    years = pd.DataFrame({'year': yrs,
                          'financial_year': [f'{y}-{y + 1}' for y in yrs]})
    years.to_sql('years', con, if_exists='append', index=False)

    u = unemp.copy()
    u['province_id'] = u['Province'].map(pid)
    u[['province_id', 'year', 'unemp_rate', 'pop_thousand', 'n_quarters']] \
        .to_sql('unemployment', con, if_exists='append', index=False)

    c = crime.merge(unemp[['Province', 'year', 'pop_thousand']], on=['Province', 'year'])
    c['province_id'] = c['Province'].map(pid)
    c['rate_per_100k'] = c['count'] / c['pop_thousand'] * 100   # pop is in thousands
    c = c.rename(columns={'Crime_Category': 'crime_category'})
    c[['province_id', 'year', 'crime_category', 'count', 'rate_per_100k']] \
        .to_sql('crime_stats', con, if_exists='append', index=False)

    con.commit()
    counts = {t: con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
              for t in ('provinces', 'years', 'unemployment', 'crime_stats')}
    log.info('Loaded %s', counts)
    if counts['crime_stats'] != len(crime) or counts['unemployment'] != len(unemp):
        raise ValueError(f'Row count mismatch after load: {counts}')
    con.close()
    return counts


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    print(load())
    con = sqlite3.connect(DB)
    print(pd.read_sql_query("""
        SELECT p.province_name, c.year, c.count, ROUND(c.rate_per_100k, 1) AS rate_per_100k,
               u.unemp_rate
        FROM crime_stats c
        JOIN provinces p USING (province_id)
        JOIN unemployment u USING (province_id, year)
        WHERE c.crime_category = 'Murder' AND p.province_name = 'Gauteng'
        ORDER BY c.year""", con))
    con.close()