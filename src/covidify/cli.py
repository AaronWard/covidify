import os
import sys
import covidify
import click
import getpass
from covidify.config import SCRIPT
USER = getpass.getuser()

def check_output_folder(var, msg):
    if not var:
        sys.stdout.write('\033[1;31m')
        print('%sMESSAGE: %s' % (' '*5, msg))
        sys.stdout.write("\033[0;0m")


@click.group()
def cli():
    '''
    ☣ COVIDIFY ☣ \n
     - use the most up-to-date data to generate reports of confirmed cases, fatalities and recoveries. 
    '''
    pass

@cli.command()
@click.option('--output', help='Folder to output data and reports [Default: /Users/' + USER + '/Desktop/covidify-output/', 
                default='/Users/'+ USER +'/Desktop/covidify-output/')
def run(output):
    # #Prompt user to tell them the output reports will be 
    # #saved on Desktop
    # check_output_folder(output, 'No output directory given, defaulting to /Users/$USER/Desktop/covidify-output/')

    #get the path of covidify in site-packages
    env = covidify.__path__[0]
    # Run the pipeline.sh and kick off the job
    os.system(env + SCRIPT + ' ' + env + ' ' + output)