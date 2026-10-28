import logging
import os
import textwrap

import matplotlib
matplotlib.use('Agg')                      # draw to files, no window needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analyse import load_data

log = logging.getLogger('pipeline')
OUT = 'outputs/charts'


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.tight_layout()
    fig.savefig(f'{OUT}/{name}.png', dpi=150)
    plt.close(fig)


def fy_labels(years):
    return [f'{y}/{str(y + 1)[2:]}' for y in years]


def lines(df, col, title, ylabel, name):
    wide = df.pivot(index='year', columns='province', values=col)
    fig, ax = plt.subplots(figsize=(9, 5))
    for p in wide.columns:
        ax.plot(wide.index, wide[p], marker='o', markersize=3, label=p)
    ax.axvspan(2019.5, 2020.5, color='grey', alpha=0.15)
    ax.text(2020, ax.get_ylim()[1], 'COVID-19\n2020/21', ha='center', va='top', fontsize=8)
    ax.set_xticks(wide.index)
    ax.set_xticklabels(fy_labels(wide.index), rotation=45)
    ax.set_title(title)
    ax.set_xlabel('Financial year (April to March)')
    ax.set_ylabel(ylabel)
    ax.legend(fontsize=7, ncol=3)
    save(fig, name)


def scatter_between(df, category, name):
    d = df[df.crime_category == category]
    m = d.groupby('province')[['unemp_rate', 'rate_per_100k']].mean()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(m.unemp_rate, m.rate_per_100k)
    for p, row in m.iterrows():
        ax.annotate(p, (row.unemp_rate, row.rate_per_100k), fontsize=8,
                    xytext=(4, 4), textcoords='offset points')
    slope, intercept = np.polyfit(m.unemp_rate, m.rate_per_100k, 1)
    xs = np.linspace(m.unemp_rate.min(), m.unemp_rate.max(), 10)
    ax.plot(xs, slope * xs + intercept, color='grey', linestyle='--')
    r = np.corrcoef(m.unemp_rate, m.rate_per_100k)[0, 1]
    ax.set_title(f'{category}: province averages 2015/16 to 2024/25 (r = {r:.2f}, n = 9)')
    ax.set_xlabel('Average unemployment rate (%)')
    ax.set_ylabel('Average rate per 100,000 working-age people')
    save(fig, name)


def forest(corr, name):
    c = corr[corr.method == 'Pearson']
    cats = sorted(c.crime_category.unique())
    views = list(c.view.unique())
    fig, ax = plt.subplots(figsize=(9, 6))
    for j, v in enumerate(views):
        d = c[c.view == v].set_index('crime_category').loc[cats]
        y = [i + (j - 1) * 0.25 for i in range(len(cats))]
        ax.errorbar(d.r, y, xerr=[d.r - d.ci_low, d.ci_high - d.r],
                    fmt='o', capsize=3, label=v)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(['\n'.join(textwrap.wrap(x, 28)) for x in cats], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel('Pearson correlation with unemployment rate (95% confidence interval)')
    ax.set_title('Unemployment vs crime rate: three views')
    ax.legend(fontsize=8)
    save(fig, name)


def run():
    df = load_data()
    unemp = df.drop_duplicates(['province', 'year'])
    corr = pd.read_csv('outputs/correlations.csv')
    lines(unemp, 'unemp_rate', 'Unemployment rate by province',
          'Unemployment rate (%)', 'unemployment_trend')
    lines(df[df.crime_category == 'Murder'], 'rate_per_100k',
          'Murder rate by province', 'Murders per 100,000 working-age people',
          'murder_trend')
    scatter_between(df, 'Murder', 'murder_vs_unemployment')
    forest(corr, 'correlations')
    log.info('Charts saved to %s', OUT)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    run()
