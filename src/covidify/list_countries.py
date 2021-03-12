'''
This script is for listing countries that have cases of corona virus.
This is so you can decide which country to make a report for. 
'''

import os
import sys
import click
import covidify
import numpy as np
from covidify.sources import github
from covidify.config import SCRIPT

def get_countries():
    """PRINTS LIST OF COUNTRIES WITH CONFIRMED COVID CASES

    precondition:
       # none

    postcondition:
       # obtains sorted list of all the countries with more than 0 confirmed cases 
       # number of infected countries is less than or equal to total number of countries globally
       # prints number of areas and countries affected
    """
    print('Getting available countries...')
    df = github.get()
    df = df[df.confirmed > 0]

    countries = sorted(list(set(df.country.values)))

    for a,b,c in zip(countries[::3],countries[1::3],countries[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))
        
    print('\n\033[1;31mNUMBER OF COUNTRIES/AREAS INFECTED:\033[0;0m', len(countries))