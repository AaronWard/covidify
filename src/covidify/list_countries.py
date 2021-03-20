'''
This script is for listing countries that have cases of corona virus.
This is so you can decide which country to make a report for. 

'''

import os
import sys
import click
import covidify
import numpy as np
from covidify.covidify_data import DataStore
from config import SCRIPT

def get_countries():
    print('Getting available countries...')
    datastore = DataStore()
    df = datastore.jhu_sources()
    df = df[df.confirmed > 0]

    countries = sorted(list(set(df.country.values)))

    for a,b,c in zip(countries[::3],countries[1::3],countries[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))

    print('\n\033[1;31mNUMBER OF COUNTRIES/AREAS INFECTED:\033[0;0m', len(countries))
