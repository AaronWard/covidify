'''
This script is for listing countries that have cases of corona virus.
This is so you can decide which country to make a report for. 

'''

import os
import sys
import click
import numpy as np
import covidify
from tabulate import tabulate
from covidify.sources import github
from covidify.config import SCRIPT

def get_countries():
    print('Getting available countries...')
    df = github.get()
    df = df[df.confirmed > 0]

    countries = sorted(list(set(df.country.values)))

    for a,b,c in zip(countries[::3],countries[1::3],countries[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))