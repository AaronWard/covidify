import os
import sys
import covidify
import click
from covidify.config import SCRIPT

@click.group()
def cli():
    '''
    ☣ COVIDIFY ☣ \n
     - use the most up-to-date data to generate reports of confirmed cases, fatalities and recoveries. 
    '''
    pass

@cli.command()
def run():

    #get the path of covidify in site-packages
    env = covidify.__path__[0]

    # Run the pipeline.sh and kick off the job
    os.system(env + SCRIPT + ' ' + env)