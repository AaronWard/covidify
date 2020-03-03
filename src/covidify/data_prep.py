"""
data_prep.py - Extract data from date range and create models
Usage:
    data_prep.py [options]
    data_prep.py -h | --help

Options:
    -h --help             Show this message.
    --output_folder=OUT   Output folder for the data and reports to be saved.
    --data_source=SOURCE  The source to fetch data from. Must be in {github,wikipedia}.
"""
from __future__ import print_function
import pandas as pd
import numpy as np
import re
import os
import docopt
import sys
import pickle
import os.path
from datetime import datetime, date, time
from dateutil.parser import parse
from time import strftime
import pyarrow
import json
import git

import sources # relative import


args = docopt.docopt(__doc__)
out = args['--output_folder']
data_source = args.get('--data_source', 'github') or 'github'

print('********', 'Using output directory', out, '********')

# determine which data source to use
data_source = {
    'github' : sources.github,
    'wikipedia' : sources.wikipedia
}.get(data_source.strip().lower())

if not data_source:
    # XXX: migrate all print statements and sys.stderr.writes to a legit logging library?
    sys.stderr.write('--data_source must be in {github,wikipedia}.\n')
    exit(1)

# let's get this :bread:
df = data_source.get()

# sheets need to be sorted by date value
print('Sorting by datetime...')
current_date = str(datetime.date(datetime.now()))

if df.date.max() == current_date:
    df = df[df.date != df.date.max()]
else:
    df = df[df.date != current_date]

df = df.sort_values('datetime')

'''
Get the difference of the sum totals for each
date and plot them on a trendline graph
'''
def get_new_cases(tmp, col):
    diff_list = []
    tmp_df_list = []
    df = tmp.copy()

    for i, day in enumerate(df.sort_values('date').date.unique()):
        tmp_df = df[df.date == day]
        tmp_df_list.append(tmp_df[col].sum())

        if i == 0:
            diff_list.append(tmp_df[col].sum())
        else:
            diff_list.append(tmp_df[col].sum() - tmp_df_list[i-1])

    return diff_list

def get_moving_average(tmp, col):
    df = tmp.copy()
    return df[col].rolling(window=2).mean()

def get_exp_moving_average(tmp, col):
    df = tmp.copy()
    return df[col].ewm(span=2, adjust=True).mean()


print('Calculating dataframe for new cases...')
daily_cases_df = pd.DataFrame([])
daily_cases_df['new_confirmed_cases'] = get_new_cases(df, 'confirmed')
daily_cases_df['new_deaths'] = get_new_cases(df, 'deaths')
daily_cases_df['new_recoveries'] = get_new_cases(df, 'recovered')
daily_cases_df['date'] = df.date.unique()

#Moving average
daily_cases_df['confirmed_MA'] = get_moving_average(daily_cases_df, 'new_confirmed_cases')
daily_cases_df['deaths_MA'] = get_moving_average(daily_cases_df, 'new_deaths')
daily_cases_df['recovered_MA'] = get_moving_average(daily_cases_df, 'new_recoveries')

#Exponential moving average
daily_cases_df['confirmed_exp_MA'] = get_exp_moving_average(daily_cases_df, 'new_confirmed_cases')
daily_cases_df['deaths_exp_MA'] = get_exp_moving_average(daily_cases_df, 'new_deaths')
daily_cases_df['recovered_exp_MA'] = get_exp_moving_average(daily_cases_df, 'new_recoveries')


'''
Calculate the number of people that are ACTUALLY infected on a given day
currently infected = sum of people date - (recovored + died)
ex: 5 = 10 - (4 - 1)

'''
current_infected = pd.DataFrame([])
current_infected['currently_infected'] = (df.groupby('date').confirmed.sum() - \
                                          (df.groupby('date').deaths.sum() + df.groupby('date').recovered.sum()))
current_infected['delta'] = (current_infected['currently_infected'] - df.groupby('date').confirmed.sum())
daily_cases_df = pd.merge(daily_cases_df, current_infected, how='outer', on='date')


data_folder = str('data/' + str(datetime.date(datetime.now())))

#Create date of extraction folder
save_dir = os.path.join(out, data_folder)

if not os.path.exists(save_dir):
    # XXX: OS code injection
    os.system('mkdir ' + save_dir)


print('Saving to data subdirectory...')
print('...', save_dir)

print('Saving...')
file_name = 'agg_data_{}.parquet.gzip'.format(datetime.date(datetime.now()))
df.astype(str).to_parquet(os.path.join(save_dir, file_name), compression='gzip')
print('...', file_name)


csv_file_name = 'agg_data_{}.csv'.format(datetime.date(datetime.now()))
df.astype(str).to_csv(os.path.join(save_dir, csv_file_name))
print('...', csv_file_name)


daily_cases_file_name = 'trend_{}.csv'.format(datetime.date(datetime.now()))
daily_cases_df.astype(str).to_csv(os.path.join(save_dir, daily_cases_file_name))
print('...', daily_cases_file_name)

print('Done!')
