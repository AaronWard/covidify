'''
This script is for listing countries that have cases of corona virus.
This is so you can decide which country to make a report for. 

'''

import os
import sys
import click
import covidify
import numpy as np

#import/use aggregate root instead of git and wiki itself
from covidify.sources import agg_data_sources as sourceData 

from covidify.config import SCRIPT

def get_countries():
    print('Getting available countries...')
    #use reference dataFetch to access root to fetch Git data
    dataFetch = sourceData.getDataGit()
    dataFetch = dataFetch[dataFetch.confirmed > 0]

    countries = sorted(list(set(dataFetch.country.values)))

    for a,b,c in zip(countries[::3],countries[1::3],countries[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))
        
    print('\n\033[1;31mNUMBER OF COUNTRIES/AREAS INFECTED:\033[0;0m', len(countries))