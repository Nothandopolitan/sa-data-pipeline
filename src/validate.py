import logging
import pandas as pd
from clean import PROVINCES, CATEGORIES

log = logging.getLogger('pipeline')
YEARS = list(range(2015, 2025))


def check(name, ok, detail=''):
    """Log a pass, or log the failure and stop the run."""
    if ok:
        log.info('PASS %s', name)
    else:
        log.error('FAIL %s %s', name, detail)
        raise ValueError(f'Validation failed: {name} {detail}')


def validate_crime(df):
    check('crime: no missing values', not df.isna().any().any())
    check('crime: no duplicate rows',
          not df.duplicated(['Province', 'year', 'Crime_Category']).any())
    check('crime: no negative counts', bool((df['count'] >= 0).all()))
    check('crime: province names match standard list', set(df['Province']) == set(PROVINCES))
    check('crime: years are 2015 to 2024', set(df['year']) == set(YEARS))
    expected = len(PROVINCES) * len(CATEGORIES) * len(YEARS)
    check('crime: row count', len(df) == expected, f'expected {expected}, got {len(df)}')


def validate_unemployment(df):
    check('unemployment: no missing values', not df.isna().any().any())
    check('unemployment: no duplicate rows', not df.duplicated(['Province', 'year']).any())
    check('unemployment: rate between 0 and 100',
          bool(df['unemp_rate'].between(0, 100).all()))
    check('unemployment: population is positive', bool((df['pop_thousand'] > 0).all()))
    check('unemployment: every year has 4 quarters', bool((df['n_quarters'] == 4).all()))
    check('unemployment: province names match standard list',
          set(df['Province']) == set(PROVINCES))
    expected = len(PROVINCES) * len(YEARS)
    check('unemployment: row count', len(df) == expected,
          f'expected {expected}, got {len(df)}')


def validate_all():
    crime = pd.read_csv('data/clean/crime.csv')
    unemp = pd.read_csv('data/clean/unemployment.csv')
    validate_crime(crime)
    validate_unemployment(unemp)
    log.info('All checks passed: %d crime rows, %d unemployment rows', len(crime), len(unemp))
    return crime, unemp


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    validate_all()