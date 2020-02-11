from __future__ import print_function
import pandas as pd
import numpy as np
import re
import os
import pickle
import os.path
from datetime import datetime, date, time 
from dateutil.parser import parse
from time import strftime
import pyarrow
import json
import git

REPO = 'https://github.com/CSSEGISandData/2019-nCoV.git'
TMP_FOLDER = '/tmp/corona/'
TMP_GIT = os.path.join(TMP_FOLDER, '2019-nCoV')
DATA = os.path.join(TMP_GIT, 'daily_case_updates')


def clean_sheet_names(new_ranges):
    '''
    Get rid of the duplicate sheets, only take the sheets from the 
    latest point in the day
    '''
    indices = []
    # Remove all sheets that dont have a numeric header
    new_ranges = [x for x in new_ranges if re.search(r'\d', x)]
        
    #split the names to just get the date
    clean_new_ranges = new_ranges.copy()
    for i, x in enumerate(clean_new_ranges):
        clean_new_ranges[i] = x.split('_')[0]    
    
    #Get the index of the latest tab for each date
    for item in set(clean_new_ranges):
        indices.append(clean_new_ranges.index(item))

    clean_new_ranges = []
    # Return wanted tabs for the sheet extraction
    for index in sorted(indices):
        clean_new_ranges.append(new_ranges[index])
        
    for sheet_name in clean_new_ranges:
        print('...', sheet_name.split('_')[0])
        
    return clean_new_ranges

def clone_repo(TMP_FOLDER, REPO):
    print('Cloning Data Repo...')
    git.Git(TMP_FOLDER).clone(REPO)

# Create Tmp Folder
if not os.path.isdir(TMP_FOLDER):
    print('Creating folder...')
    print('...', TMP_FOLDER)
    os.mkdir(TMP_FOLDER)

#Check if repo exists
if not os.path.isdir(TMP_GIT):
    clone_repo(TMP_FOLDER, REPO)
else:
    #get up to date repo
    print('Deleting out of date repo...')
    os.system('rm -rf ' + str(TMP_GIT))
    clone_repo(TMP_FOLDER, REPO)
    
sheets = os.listdir(DATA)

# Clean the result to the sheet tabs we want
print('Cleaning sheets...')
cleaned_sheets = clean_sheet_names(sheets)


'''
For assigning date by the time sheet name
'''
def fix_dates(tmp_df, file_name):
    file_name = file_name.split('_')[0]
    tmp_df['Last Update'] = file_name
    return tmp_df

keep_cols = ['Confirmed', 'Country/Region', 'Deaths', 'Last Update', 'Province/State', 'Recovered']
numeric_cols = ['Confirmed', 'Deaths', 'Recovered']

def get_data(cleaned_sheets):
    all_csv = []
    # Import all CSV's
    for file in sorted(cleaned_sheets):
        tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, header=0)
        tmp_df = tmp_df[keep_cols]
        tmp_df[numeric_cols] = tmp_df[numeric_cols].fillna(0)
        tmp_df[numeric_cols] = tmp_df[numeric_cols].astype(int)
        tmp_df[['Country/Region', 'Province/State']] = tmp_df[['Country/Region', 'Province/State']].fillna('')
        tmp_df = fix_dates(tmp_df, file)
        all_csv.append(tmp_df)

    tmp_df = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)
    return tmp_df


df = get_data(cleaned_sheets)

# Now that we have all the data we now need to clean it 
# - Fill null values
# - remore suspected values
# - change column names
def clean_data(tmp_df):
    if 'Demised' in tmp_df.columns:
        tmp_df.rename(columns={'Demised':'Deaths'}, inplace=True)

    if 'Country/Region' in tmp_df.columns:
        tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)
    
    if 'Province/State' in tmp_df.columns:
        tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
        
    if 'Last Update' in tmp_df.columns:
        tmp_df.rename(columns={'Last Update':'date'}, inplace=True)
        
    if 'Suspected' in tmp_df.columns:
        tmp_df = tmp_df.drop(columns='Suspected')

    for col in tmp_df.columns:
        tmp_df[col] = tmp_df[col].fillna(0)
    
    #Lower case all col names
    tmp_df.columns = map(str.lower, tmp_df.columns)    
    
    return tmp_df

print('Cleaning dataframes...')
df  = clean_data(df)

# sheets need to be sorted by date value
print('Sorting by date...')
df['date'] = df['date'].astype(str)
df = df.sort_values('date')


'''
Get the difference of the sum totals for each
date and plot them on a trendline graph
'''
def get_new_cases(tmp, col):
    diff_list = []
    tmp_df_list = []
    df = tmp.copy()
    
    for column in ['confirmed', 'deaths', 'recovered']:
        df[column] = df[column].replace('', 0).astype(int)

    for i, day in enumerate(df.date.unique()):    
        tmp_df = df[df.date == day]
        tmp_df_list.append(tmp_df[col].sum())
        
        if i == 0:
            diff_list.append(tmp_df[col].sum())
        else:
            diff_list.append(tmp_df[col].sum() - tmp_df_list[i-1])
        
    return diff_list

print('Calculating dataframe for new cases...')
daily_cases_df = pd.DataFrame([])
daily_cases_df['new_confirmed_cases'] = get_new_cases(df, 'confirmed')
daily_cases_df['new_deaths'] = get_new_cases(df, 'deaths')
daily_cases_df['new_recoveries'] = get_new_cases(df, 'recovered')
daily_cases_df['date'] = df.date.unique()



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

#Create date of extraction folder
save_dir  = './data/' + str(datetime.date(datetime.now()))

print('Saving to data subdirectory...')
print('...', save_dir)

if not os.path.exists(save_dir):
    os.mkdir(save_dir)
    
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