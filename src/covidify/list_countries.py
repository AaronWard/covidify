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
    print('Getting available countries...')
    df = github.get()
    df = df[df.confirmed > 0]

    countries = sorted(list(set(df.country.values)))

    for a,b,c in zip(countries[::3],countries[1::3],countries[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))
        
    print('\n\033[1;31mNUMBER OF COUNTRIES/AREAS INFECTED:\033[0;0m', len(countries))
#Aggregrate Root    
 def get_top_countires(countries):
    df = github.get(countries)
    df = df[df.countries > 5000] #gets countires that have cases greater then 1,000,000 and returns that top countires 
   
    countries = sorted(list(set(df.country.values)))
    return countries = get_top_countires(df)
    
    
    
