import base64
import logging
from datetime import datetime

import pandas as pd

from analyse import load_data

log = logging.getLogger('pipeline')
CHARTS = 'outputs/charts'
OUT = 'outputs/dashboard.html'

CSS = """
body { font-family: Arial, sans-serif; max-width: 1000px; margin: 2rem auto; padding: 0 1rem;
       color: #222; line-height: 1.5; }
h1 { margin-bottom: 0; } h2 { margin-top: 2.5rem; border-bottom: 2px solid #ddd; }
.sub { color: #666; margin-top: 0.2rem; }
.cards { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0; }
.card { flex: 1; min-width: 150px; background: #f4f6f8; border-radius: 8px; padding: 1rem; }
.card b { display: block; font-size: 1.8rem; }
img { max-width: 100%; margin: 1rem 0; }
table { border-collapse: collapse; font-size: 0.85rem; width: 100%; overflow-x: auto; }
th, td { border: 1px solid #ddd; padding: 4px 8px; text-align: right; }
th { background: #f4f6f8; } td:first-child, th:first-child { text-align: left; }
.note { background: #fff8e1; border-left: 4px solid #f2b705; padding: 0.6rem 1rem; }
"""


def img(name):
    with open(f'{CHARTS}/{name}.png', 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{data}" alt="{name}">'


def table(df, **kw):
    return df.to_html(index=False, border=0, **kw)


def build():
    df = load_data()
    unemp = df.drop_duplicates(['province', 'year'])
    corr = pd.read_csv('outputs/correlations.csv')
    trends = pd.read_csv('outputs/trends.csv')

    last = unemp.year.max()
    latest = (df[(df.year == last) & (df.crime_category == 'Murder')]
              [['province', 'unemp_rate', 'count', 'rate_per_100k']]
              .sort_values('unemp_rate', ascending=False).round(1))
    latest.columns = ['Province', 'Unemployment rate (%)', 'Murders', 'Murders per 100k']

    pear = corr[corr.method == 'Pearson'][['crime_category', 'view', 'n', 'r',
                                           'ci_low', 'ci_high', 'p_value']]
    pear.columns = ['Crime category', 'View', 'n', 'r', 'CI low', 'CI high', 'p-value']

    unemp_trend = (trends[trends.measure == 'unemployment rate']
                   [['province', 'slope_per_year', 'p_value']].round(3))
    unemp_trend.columns = ['Province', 'Change per year (points)', 'p-value']

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>SA People and Safety Dashboard</title><style>{CSS}</style></head><body>
<h1>SA People and Safety Dashboard</h1>
<p class="sub">Unemployment (Stats SA QLFS) and crime (SAPS) by province,
financial years {unemp.year.min()}/{str(unemp.year.min() + 1)[2:]} to
{last}/{str(last + 1)[2:]}. Built {datetime.now():%Y-%m-%d %H:%M}.</p>

<div class="cards">
  <div class="card"><b>{df.province.nunique()}</b>provinces</div>
  <div class="card"><b>{unemp.year.nunique()}</b>financial years</div>
  <div class="card"><b>{df.crime_category.nunique()}</b>crime categories</div>
  <div class="card"><b>{len(df)}</b>crime rows analysed</div>
</div>

<h2>1. How have unemployment and crime changed?</h2>
{img('unemployment_trend')}
{img('murder_trend')}
<h3>Unemployment trend per province (straight-line fit)</h3>
{table(unemp_trend)}
<h3>Murder and unemployment, {last}/{str(last + 1)[2:]}</h3>
{table(latest)}

<h2>2. Do higher-unemployment provinces have higher crime?</h2>
{img('murder_vs_unemployment')}
{img('correlations')}
{table(pear)}
<p class="note"><b>Reading this:</b> the "between provinces" view compares the 9 provinces'
averages and answers the research question directly. The "within provinces" view asks
whether a province's crime moves with its own unemployment over time. Intervals that
include 0 mean no detectable relationship.</p>

<h2>3. Limits of these results</h2>
<ul>
<li>Correlation only: nothing here shows that unemployment causes crime.</li>
<li>Small sample: 9 provinces over 10 years, and consecutive years are not independent,
so p-values are optimistic. 36 tests were run, so a few "significant" results are expected
by chance.</li>
<li>Shared national trends and the COVID-19 year (2020/21) can create correlations
between series that are not related.</li>
<li>Rates use the working-age population (15 to 64) as the denominator, not total
population, so they differ from published SAPS rates.</li>
<li>Crime is per financial year (April to March); unemployment is the average of the four
quarters in the same year. Only the official unemployment rate is used.</li>
<li>SAPS counts are reported crime, which depends on reporting and policing practice.</li>
</ul>
</body></html>"""
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    log.info('Dashboard written to %s', OUT)


def run():
    build()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    run()
