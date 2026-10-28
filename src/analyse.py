import logging
import os
import sqlite3

import numpy as np
import pandas as pd
from scipy import stats

log = logging.getLogger('pipeline')
DB = 'data/pipeline.db'
OUT = 'outputs'


def load_data():
    con = sqlite3.connect(DB)
    df = pd.read_sql_query("""
        SELECT p.province_name AS province, c.year, c.crime_category,
               c.count, c.rate_per_100k, u.unemp_rate, u.pop_thousand
        FROM crime_stats c
        JOIN provinces p USING (province_id)
        JOIN unemployment u USING (province_id, year)""", con)
    con.close()
    return df


def descriptives(df):
    unemp = (df.drop_duplicates(['province', 'year'])
               .groupby('province')['unemp_rate']
               .agg(['mean', 'median', 'std', 'min', 'max']).round(2))
    crime = (df.groupby(['crime_category', 'province'])['rate_per_100k']
               .agg(['mean', 'median', 'std']).round(1))
    return unemp, crime


def trends(df):
    """Straight-line trend per province (change per year) with p-value."""
    rows = []
    u = df.drop_duplicates(['province', 'year'])
    for prov, g in u.groupby('province'):
        r = stats.linregress(g['year'], g['unemp_rate'])
        rows.append((prov, 'unemployment rate', r.slope, r.pvalue))
    for (prov, cat), g in df.groupby(['province', 'crime_category']):
        r = stats.linregress(g['year'], g['rate_per_100k'])
        rows.append((prov, cat + ' (per 100k)', r.slope, r.pvalue))
    return pd.DataFrame(rows, columns=['province', 'measure', 'slope_per_year',
                                       'p_value']).round(4)


def corr(x, y, extra_df=0):
    """Correlation with p-value and 95% CI (Fisher z).
    extra_df = number of group means removed beforehand (for the within-province view)."""
    n = len(x)
    r = np.corrcoef(x, y)[0, 1]
    dof = n - 2 - extra_df
    t = r * np.sqrt(dof / (1 - r ** 2))
    p = 2 * stats.t.sf(abs(t), dof)
    se = 1 / np.sqrt(n - 3 - extra_df)
    lo, hi = np.tanh(np.arctanh(r) + np.array([-1.96, 1.96]) * se)
    return r, p, lo, hi


def correlations(df):
    """Unemployment rate vs crime rate, three ways, Pearson and Spearman."""
    cols = ['unemp_rate', 'rate_per_100k']
    rows = []
    for cat, g in df.groupby('crime_category'):
        means = g.groupby('province')[cols].mean()
        demeaned = g[cols] - g.groupby('province')[cols].transform('mean')
        views = {
            'pooled (all province-years)': (g[cols], 0),
            'between provinces (9 averages)': (means, 0),
            'within provinces (over time)': (demeaned, g['province'].nunique()),
        }
        for view, (d, k) in views.items():
            x, y = d['unemp_rate'], d['rate_per_100k']
            for method, (a, b) in {'Pearson': (x, y),
                                   'Spearman': (x.rank(), y.rank())}.items():
                r, p, lo, hi = corr(a.to_numpy(), b.to_numpy(), k)
                rows.append((cat, view, method, len(d), r, p, lo, hi))
    return pd.DataFrame(rows, columns=['crime_category', 'view', 'method', 'n',
                                       'r', 'p_value', 'ci_low', 'ci_high']).round(4)


def run():
    df = load_data()
    os.makedirs(OUT, exist_ok=True)
    d_unemp, d_crime = descriptives(df)
    t = trends(df)
    c = correlations(df)
    d_unemp.to_csv(f'{OUT}/descriptives_unemployment.csv')
    d_crime.to_csv(f'{OUT}/descriptives_crime.csv')
    t.to_csv(f'{OUT}/trends.csv', index=False)
    c.to_csv(f'{OUT}/correlations.csv', index=False)
    log.info('Analysis done: %d trend rows, %d correlation rows', len(t), len(c))
    return c


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    table = run()
    pd.set_option('display.width', 220)
    pd.set_option('display.max_columns', 20)
    print(table[table.method == 'Pearson'].to_string(index=False))