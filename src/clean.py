import re
import pandas as pd

SAPS = 'data/raw/saps/saps_crime_2024_2025.xlsx'
QLFS = 'data/raw/statssa/qlfs_trends_2008_2025.xlsx'
PROVINCES = ['Eastern Cape', 'Free State', 'Gauteng', 'KwaZulu-Natal', 'Limpopo',
             'Mpumalanga', 'North West', 'Northern Cape', 'Western Cape']
CATEGORIES = ['Murder', 'Attempted murder', 'Robbery with aggravating circumstances',
              'Burglary at residential premises', 'Theft of motor vehicle and motorcycle',
              'Contact crime (Crimes against the person)']
QUARTER = re.compile(r'(Jan-Mar|Apr-Jun|Jul-Sep|Oct-Dec)\s+(\d{4})')


def norm(name):
    """Lowercase and treat hyphens and repeated spaces as one space."""
    return re.sub(r'[-\s]+', ' ', str(name)).strip().lower()


PROV_LOOKUP = {norm(p): p for p in PROVINCES}


def province_from_label(label):
    """Return the standard province name if the label is a province header, else None."""
    clean = re.sub(r'[\s\d\*\(\)\[\],.]+$', '', str(label))
    return PROV_LOOKUP.get(norm(clean))


def clean_saps():
    r = pd.read_excel(SAPS, sheet_name='RAW Data', header=2)
    r = r[r['Comp level'] == 'Province'].copy()
    r['Province'] = r['Station'].map(province_from_label)   # province name sits in Station
    r = r[r['Province'].notna() & r['Crime_Category'].isin(CATEGORIES)]
    years = [c for c in r.columns if re.fullmatch(r'\d{4}-\d{4}', str(c))]
    long = r.melt(id_vars=['Province', 'Crime_Category'], value_vars=years,
                  var_name='fy', value_name='count')
    long['year'] = long['fy'].str[:4].astype(int)   # 2015 = Apr 2015 to Mar 2016
    long['count'] = pd.to_numeric(long['count'])
    return long[['Province', 'year', 'Crime_Category', 'count']]


def clean_qlfs():
    t = pd.read_excel(QLFS, sheet_name='Table 2.3', header=None)
    q = t.iloc[1, 1:]
    rows, prov = [], None
    for i in range(len(t)):
        label = t.iloc[i, 0]
        if pd.isna(label):
            continue
        label = str(label).strip()
        low = label.lower()
        p = province_from_label(label)
        if p:                                       # province header, whatever is in its row
            prov = p
            continue
        vals = t.iloc[i, 1:]
        if vals.isna().all():                       # metro block, footnote or section header
            if not low.startswith(('key rates', 'labour underutilization')):
                prov = None
            continue
        if prov and (low.startswith('population') or low.startswith('lu1')):
            name = 'pop_thousand' if low.startswith('population') else 'unemp_rate'
            for qtr, v in zip(q, vals):
                m = QUARTER.match(str(qtr).strip())
                if m and pd.notna(v):
                    yr = int(m.group(2))
                    fy = yr - 1 if m.group(1) == 'Jan-Mar' else yr
                    rows.append((prov, fy, name, float(v)))
    d = pd.DataFrame(rows, columns=['Province', 'year', 'measure', 'value'])
    wide = d.pivot_table(index=['Province', 'year'], columns='measure',
                         values='value', aggfunc='mean')
    wide['n_quarters'] = d[d.measure == 'unemp_rate'].groupby(['Province', 'year']).size()
    return wide.reset_index()


if __name__ == '__main__':
    s, u = clean_saps(), clean_qlfs()
    u = u[(u.year >= 2015) & (u.year <= 2024)]
    print(s.shape, u.shape)                 # expect (540, 4) and (90, 5)
    print(sorted(u.Province.unique()))      # expect all 9 provinces
    print(u.n_quarters.value_counts())      # expect 4 for every row
    print(u[u.Province == 'KwaZulu-Natal'].head(3))
    print(s[(s.Province == 'KwaZulu-Natal') & (s.Crime_Category == 'Murder')].head(3))