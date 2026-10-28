import argparse
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, 'src')       # so the stage scripts can import each other

log = logging.getLogger('pipeline')


def setup_logging():
    os.makedirs('logs', exist_ok=True)
    path = f"logs/run_{datetime.now():%Y%m%d_%H%M%S}.log"
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    for handler in (logging.FileHandler(path), logging.StreamHandler()):
        handler.setFormatter(fmt)
        log.addHandler(handler)
    log.setLevel(logging.INFO)
    return path


def stage_extract():
    result = subprocess.run([sys.executable, 'src/extract.py'])
    if result.returncode != 0:
        raise RuntimeError('extract.py failed')


def stage_clean():
    import clean
    s, u = clean.run()
    log.info('Cleaned: %d crime rows, %d unemployment rows', len(s), len(u))


def stage_validate():
    import validate
    validate.validate_all()


def stage_load():
    import load
    load.load()


def stage_analyse():
    import analyse
    analyse.run()


def stage_visualise():
    import visualise
    visualise.run()


STAGES = [('extract', stage_extract), ('clean', stage_clean),
          ('validate', stage_validate), ('load', stage_load),
          ('analyse', stage_analyse), ('visualise', stage_visualise)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fresh', action='store_true',
                        help='delete cleaned data and the database first')
    parser.add_argument('--skip-extract', action='store_true',
                        help='reuse the raw files already in data/raw')
    args = parser.parse_args()

    logfile = setup_logging()
    log.info('Pipeline started, log: %s', logfile)

    if args.fresh:
        shutil.rmtree('data/clean', ignore_errors=True)
        if os.path.exists('data/pipeline.db'):
            os.remove('data/pipeline.db')
        log.info('Fresh run: removed data/clean and data/pipeline.db')

    for name, fn in STAGES:
        if name == 'extract' and args.skip_extract:
            log.info('Stage extract: skipped')
            continue
        log.info('Stage %s: start', name)
        try:
            fn()
        except Exception:
            log.exception('Stage %s FAILED, stopping the run', name)
            sys.exit(1)
        log.info('Stage %s: done', name)

    log.info('Pipeline finished successfully')


if __name__ == '__main__':
    main()
