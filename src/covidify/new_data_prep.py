"""
data_prep.py - Extract data from date range and create models
Usage:
    data_prep.py [options]
    data_prep.py -h | --help

Options:
    -h --help             Show this message.
    --output_folder=OUT   Output folder for the data and reports to be saved.
    --source=SRC          Datasource for where the data will be downloaded from.
    --country=CNT         Arg for filtering by a specific country
    --top=top             Top number of countries in the log plot
"""
from __future__ import print_function
import os
import sys
import docopt
import numpy as np
import pandas as pd

from string import capwords
from difflib import get_close_matches
from datetime import datetime, date, time 

from covidify.sources import github, wiki
from covidify.config import REPO, TMP_FOLDER, TMP_GIT, DATA
from covidify.utils.utils import replace_arg_score
from covidify.aggregates import Case, Country, Report

args = docopt.docopt(__doc__)
out = args['--output_folder']
country = args['--country']
source = args['--source']
top = int(args['--top'])

############ COUNTRY SELECTION ############

def get_similar_countries(c, country_list):
    pos_countries = get_close_matches(c, country_list)
    
    if len(pos_countries) > 0:
        print('\033[1;31m'+c, 'was not listed. did you mean', pos_countries[0].capitalize() + '?\033[0;0m')
        
        #Only delete if its a covidify generated folder
        if 'Desktop/covidify-output-' in out:
            os.system('rm -rf ' + out)
        sys.exit(1)
    else:
        print('\033[1;31m'+c, 'was not listed.\033[0;0m')
        if 'Desktop/covidify-output-' in out:
            os.system('rm -rf ' + out)
        sys.exit(1)
        
def check_specified_country(df, country):
    '''
    let user filter reports by country, if not found
    then give a option if the string is similar
    '''
    
    # Get all unique countries in the data
    country_list = list(map(lambda x:x.lower().strip(), set(df.country.values)))

    if country:
        print('Country specified!')
        if country.lower() == 'Mainland China': #Mainland china and china doesn't come up as similar
            print(country, 'was not listed. did you mean China?')
            sys.exit(1)
        # give similar option if similarity found
        if country.lower() not in country_list:
            get_similar_countries(country, country_list)
            
        else:
            #Return filtered dataframe
            print('... filtering data for', country)
            if len(country) == 2:
                df = df[df.country == country.upper()]
            else:
                df = df[df.country == capwords(country)]
            return df
    else:
        print('... No specific country specified')
        return df

'''
Get the difference of the sum totals for each
date and plot them on a trendline graph
'''
def get_new_cases(tmp, col):
    diff_list = []
    tmp_df_list = []
    df = tmp.copy()

    for i, day in enumerate(df.sort_values('file_date').file_date.unique()):
        tmp_df = df[df.file_date == day]
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

def get_top_countries(data):
    # Get top N infected countries
    tmp_df = data.copy()
    tmp_df = tmp_df[tmp_df.file_date == df.file_date.max()]
    return tmp_df.groupby(['country']).agg({'confirmed': 'sum'}).sort_values('confirmed',ascending=False).head(top).index 
        
def create_new_case(name, df, col):
    return Case(name, get_new_cases(df, col))

def create_new_country(df, country):
  if country == None:
    return Country('global', check_specified_country(df, country))
  else:
    return Country(country, check_specified_country(df, country))

############ DATA SELECTION ############

if '_' in country:
    country = replace_arg_score(country)

if country == 'Global':
    country = None

if source == 'JHU':
    df = github.get()
    
elif source == 'wiki':
    print('Apologies, the wikipedia source is not ready yet - getting github data')
    df = github.get()
    

country_ = create_new_country(df, country)

# df = check_specified_country(df, country)

############ DAILY CASES ############

# sheets need to be sorted by date value
# print('Sorting by datetime...')

df = df.sort_values('datetime')

daily_cases_df = pd.DataFrame([])

current_date = str(datetime.date(datetime.now()))

print('... Calculating dataframe for new cases')

country_.add(Case('date', df.file_date.unique()))
country_.add(create_new_case('new_confirmed_cases', df, 'confirmed'))
country_.add(create_new_case('new_deaths', df, 'deaths'))
country_.add(create_new_case('new_recoveries', df, 'recovered'))

r = Report(str(datetime.date(datetime.now())), 'trend')

r.add(country_)

r.combine()

r.save(out)