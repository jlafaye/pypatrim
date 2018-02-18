import argparse
import pandas as pd
import numpy as np
import logging
import os

from patrim.pdf import read_pdf
from patrim.gmaps import fill_locations

def merge_dfs(dfs):
    df = pd.concat(dfs).drop_duplicates(subset=['CAD']) \
                       .set_index('CAD')
    return df

def reshape_df(df):
    for column in ['LATITUDE', 'LONGITUDE']:
        if column not in df.columns:
            df[column] = np.nan
    return df

def run_pdf_to_csv():
    parser = argparse.ArgumentParser(description='Convert a Patrim pdf to a csv file')
    parser.add_argument('input', nargs='+', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Activate debugging')
    parser.add_argument('--no-gmaps', action='store_true',
                        help='Do not query google maps to retrieve GPS coordinates')

    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)

    if args.output and \
        os.path.exists(args.output):
        logging.info('Loading existing file {}'.format(args.output))
        df = pd.read_csv(args.output)
        dfs = [df]
    else:
        dfs = []

    for fname in args.input:
        df = read_pdf(fname)
        logging.debug('{} {}'.format(fname, len(df)))
        dfs.append(df)

    # remove duplicates
    df = merge_dfs(dfs)
    reshape_df(df)

    # retrieve locations
    if not args.no_gmaps:
        fill_locations(df)

    if args.output:
        logging.info('Writing %d transaction(s) to %s' % (len(df), args.output))
        df.to_csv(args.output)
    else:
        print(df.to_string())

