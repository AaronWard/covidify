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
    precondition:
        #Arg1: get a list of countries accross the world that have a current cases of covid-19
        #Arg2: Get a list of all countires with no active cases of covid-19
        #Arg3: Get a list of countires that were hit the most by covid-19 cases
     postcondition:
        #Arg1: display all the countires with active cases of covid-19, countires with no cases and countries with most hit by
    print('Getting available countries...')
    df = github.get()
    df = df[df.confirmed > 0]

    countries = sorted(list(set(df.country.values)))

    for a,b,c in zip(countries[::3],countries[1::3],countries[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))
        
    print('\n\033[1;31mNUMBER OF COUNTRIES/AREAS INFECTED:\033[0;0m', len(countries))
