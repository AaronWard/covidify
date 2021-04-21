#behavioural design pattern on cli.py
#chain of handlers

#---------------------------------------------------------------------------------------------------------------------------------------------------
#pseudo code
#the handler interface declares a method for building a chain of
#handlers.it also declares a method for executing a request
#interface compo_help is
    #method show help()
#the base class for simple components




#---------------------------------------------------------------------------------------------------------------------------------------------------

import os
import sys
import click
import getpass
import covidify
from covidify.config import SCRIPT, LOG_TOP_N_COUNTRIES, DAYS_IN_FUTURE
from covidify.utils.utils import replace_arg_space
from covidify.list_countries import get_countries
from abc import ABC,abstractmethod #include abstract method
#------------this code is chaned with observer behavioural design pattern-----------------------------------
USER = getpass.getuser()
#get the path of covidify in site-packages
env = covidify.__path__[0]
class U:
    '''represents what is being observed'''
    def __init__(self):
        '''create an empty observer list'''
        self._observer=[]
    def notify(self,modifier=none):
        '''alerts the observers'''
        for observer in self._observers:
            if modifier!=observer:
                observer.update(self)
    def attach(self,observer):
        '''if the observer is not in the list,append it into the list'''
        if observer not in self._observers:
            self._observers.append(observer)
            
    
#-------------------------------------------------------------
class P_country(U):
    ''' monitor the object'''
    def __init__(self,name=''):
        U.__init__(self)
        self.name=name
        
    def check_output_folder(var, country_str,  msg):
        '''
        Check if the output folder is valid, if not
        just default to dekstop 
        '''
        self.notify()
        if not var:
             print('%sMESSAGE: %s' % (' '*5, msg))
            if country_str == 'Global':
                return os.path.join('/Users', USER, 'Desktop', 'covidify-output')
            else:
                return os.path.join('/Users', USER, 'Desktop', 'covidify-output-{}'.format(country_str))
        else:
            return var
    
    def check_forecast_days(var, msg):
        '''
        Default days for forecasting
        '''
        self.notify()
        if not var:
            return DAYS_IN_FUTURE
        else:
            return var

    def check_top_countries(var, msg):
        '''
        Check number of countries for the log plot
        '''
        self.notify()
        if not var:
            print('%sMESSAGE: %s' % (' '*5, msg))
            return LOG_TOP_N_COUNTRIES
        else:
            return var
    
    def check_source_arg(var, msg):
        '''
        Check if the datasource is valid, if not then just
        default to the john hopkin github repo
        '''
        self.notify()
        if var is None:
            print('%sMESSAGE: %s' % (' '*5, msg))
            return 'JHU'
        elif 'wiki' in var or 'JHU' in var:
            return var
        else:
            print('%sMESSAGE: %s' % (' '*5, 'invalid source given'))
            sys.exit()
        
    def check_country(country, msg):
        '''
        Do some regex work on passed country string
        because multi word args are not supported
        '''
        self.notify()
        if not country:
            print('%sMESSAGE: %s' % (' '*5, msg))
            return 'Global'
        else:
            country_str = replace_arg_space(country[0])
            return country_str

    def check_list_flag(flag, msg):
        self.notify()
        if not flag:
            print('%sMESSAGE: %s' % (' '*5, msg))
            sys.exit(1)
        else:
            return flag

############################################################

@click.group()
def cli():
    '''
    ☣  COVIDIFY ☣ \n
     - use the most up-to-date data to generate reports of confirmed cases, fatalities and recoveries. 
    '''
    pass

@cli.command()
@click.option('--output',  help='Folder to output data and reports [Default: /Users/' + USER + '/Desktop/covidify-output/]')
@click.option('--source',  help='There are two datasources to choose from, John Hopkins github repo or wikipedia -- options are JHU or wiki respectively [Default: JHU]')
@click.option('--country', help='Filter reports by a country', multiple=True, type=str)
@click.option('--top',     help='Top N infected countries for log plot. [Default: '+ str(LOG_TOP_N_COUNTRIES) + ']')
@click.option('--forecast',help='Number of days to forecast cumulative cases in the future. [Default: ' + str(DAYS_IN_FUTURE) + ']')
def run(output, source, country, top, forecast):
    '''
    Generate reports for global cases or refine by country.
    '''
    
    #Do checks on args
    #here mulltiple observer on user can be used
    #observer checke any changes in user and the executes all other related functions which depends on user.
   
U_1=P_country('USER')
country_str = check_country(country, '\033[1;31m No country specified, defaulting to global cases \033[0;0m')    
output   = check_output_folder(output, country_str, '\033[1;31m No output directory given, defaulting to /Users/' + USER + '/Desktop/ \033[0;0m')
source   = check_source_arg(source, '\033[1;31m No source given, defaulting to John Hopkin CSSE github repo \033[0;0m')
top      = check_top_countries(top, '\033[1;31m No top countries given, defaulting to top ' + str(LOG_TOP_N_COUNTRIES) + ' \033[0;0m')
forecast = check_forecast_days(forecast, '\033[1;31m No days for forecasting given, defaulting to ' + str(DAYS_IN_FUTURE) + ' \033[0;0m')
    
os.system(env + SCRIPT + ' ' + env + ' ' + output + ' ' + source + ' ' + country_str + ' ' + str(top) + ' ' + str(forecast))
U_1.attach(country_str)
U_1.attach(output)
U_1.attach(source)
U_1.attach(top)
U_1.attach(forecast)
    
@click.option('--countries', help='List countries that have had confirmed cases.', is_flag=True)
@cli.command()

def list(countries):
    '''
    List all the countries that have confirmed cases.
    '''
    countries = check_list_flag(countries, '\033[1;31m Invalid flag passed. Make sure to use --countries\033[0;0m')

    if countries:
        get_countries()
