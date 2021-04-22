"""
data_visualization.py - Extract data from date range and create models
Usage:
    data_visualization.py [options]
    data_visualization.py -h | --help

Options:
    -h --help             Show this message.
    --output_folder=OUT   Output folder for the data and reports to be saved.
    --country=CNT         Arg for filtering by a specific country
    --top=top             Top number of countries in the log plot
"""
from __future__ import print_function
import os
import glob
import docopt
import pickle
import os.path
import pyarrow
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from covidify.utils.utils import replace_arg_score
import abc

# plt settings
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font', **font)
plt.style.use('ggplot')

args = docopt.docopt(__doc__)
out = args['--output_folder']
country = args['--country']
top = int(args['--top'])


if '_' in country:
    country = replace_arg_score(country)

if country == 'Global':
    country = None

#Create instance of Country class
context_country = Country(country)

# Dynamic parameters
data_dir  = os.path.join(out, 'data', str(datetime.date(datetime.now())))
agg_file  = 'agg_data_{}.csv'.format(datetime.date(datetime.now()))
trend_file  = 'trend_{}.csv'.format(datetime.date(datetime.now()))
log_file  = 'log_{}.csv'.format(datetime.date(datetime.now()))
report  = context_country.create_report_name(country)


# import data
print('Importing Data...')
agg_df = pd.read_csv(os.path.join(data_dir, agg_file))
daily_df = pd.read_csv(os.path.join(data_dir, trend_file))
log_df = pd.read_csv(os.path.join(data_dir, log_file))

#Create place to save diagrams
image_dir =  os.path.join(out,'reports', 'images')
reports_dir =  os.path.join(out,'reports')

if not os.path.exists(image_dir):
    print('Creating reports folder...')
    os.system('mkdir -p ' + image_dir)

# Convert types
for col in ['confirmed', 'deaths', 'recovered']:
    agg_df[col] = agg_df[col].replace('', 0).astype(int)



class State(metaclass=abc.ABCMeta):
'''
State interface
'''
    def __init__(self):
        pass

    #Creates title used for graphs
    @abc.abstractmethod
    def create_title(self):
        pass

    #Creates safe file name for graphs
    @abc.abstractmethod
    def create_save_file(self):
        pass

    #Creates report name
    @abc.abstractmethod
    def create_report_name(self):
        pass



class CountryGivenState(State):
'''
State to be used if user gives a country
'''
    def __init__(self):
        pass

    def create_title(self, fig_title, country):
        return fig_title + ' for ' + country

    def create_save_file(self, col, country, graph_type):
        return '{}_{}_{}.png'.format(country, col, graph_type)

    def create_report_name(self, country):
        return '{}_report_{}.xlsx'.format(country, datetime.date(datetime.now()))

class GlobalCountryState(State):
'''
State to be used if no country was specifed and in that case we include all countries
'''

    def __init__(self):
        pass

    def create_title(self, fig_title, country):
        return fig_title

    def create_save_file(self, col, country, graph_type):
        return '{}_{}_{}.png'.format(col, graph_type)

    def create_report_name(self, country):
        return 'report_{}.xlsx'.format(datetime.date(datetime.now()))

class Country:
'''
Context class for the different states
This class should be the one that is instantied and called upon
'''
    def __init__(self, country):
        if country:
            self._state = CountryGivenState()
        else
            self._state = GlobalCountryState()

    def create_title(self, fig_title, country):
        self._state.create_title(self, fig_title, country)

    def create_save_file(self, col, country, graph_type):
        self._state.create_save_file(self, col, country, graph_type)

    def create_report_name(self, country):
        self._state.create_report_name(self, country)

    def change_state(self, country):
        if country:
            self._state = CountryGivenState()
        else
            self._state = GlobalCountryState()

# Plot and save trendline graph
def create_trend_line(tmp_df, date_col, col, col2, col3, fig_title, country):
    fig, ax = plt.subplots(figsize=(20,10))
    tmp_df.groupby([date_col])[[col, col2, col3]].sum().plot(ax=ax, marker='o')
    ax.set_title(context_country.create_title(fig_title, country))
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, context_country.create_save_file(col, country, 'trendline')))

def create_bar(tmp_df, col, rgb, country):
    tmp_df = tmp_df.tail(120)
    fig, ax = plt.subplots(figsize=(20,10))
    tmp = tmp_df.groupby(['date'])[[col]].sum()
    ax.set_title(context_country.create_title(col, country))
    tmp.plot.bar(ax=ax, rot=90, color=rgb)
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, context_country.create_save_file(col, country, 'bar')))

def create_stacked_bar(tmp_df, col1, col2, fig_title, country):
    tmp_df = tmp_df.tail(120)
    tmp_df = tmp_df.set_index('date')
    fig, ax = plt.subplots(figsize=(20,10))
    ax.set_title(context_country.create_title(fig_title, country))
    tmp_df[[col2, col1]].plot.bar(ax=ax,
                                  rot=90,
                                  stacked=True)
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, context_country.create_save_file(col2, country, 'stacked_bar')))

def log_plot(tmp, col, fig_title):
    '''
    Plot on a logarithmic scale for comparing
    countries infection rates

    '''
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure(figsize = (20,10))
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', [cm(1.*i/top) for i in range(top)])
    for country in tmp.country.unique():
        new_col = country.lower() + '_' + col
        tmp[country.lower() + '_' + col] = tmp[[col]]
        tmp.rename(columns={col: new_col})
        tmp[tmp.country == country].groupby(['day'])[[new_col]].sum().plot(ax=ax)
        ax.set_yscale('log', basey=10)
    ax.set_title(fig_title)
    fig = ax.get_figure()
    context_country.change_state(None)
    fig.savefig(os.path.join(image_dir, context_country.create_save_file(col, country=, graph_type='log')))

##### Create Graphs #####
print('Creating graphs...')
print('... Time Series Trend Line')
# Time Series Data Plots
create_trend_line(agg_df, 'file_date', 'confirmed', 'deaths', 'recovered', 'Accumulative trend', country)


print('... Daily Figures')
# Daily Figures Data Plots
daily_figures_cols = ['new_confirmed_cases', 'new_deaths', 'new_recoveries', 'currently_infected']
for col, rgb in zip(daily_figures_cols, ['tomato', 'lightblue', 'mediumpurple', 'green']):
    create_bar(daily_df, col, rgb, country)

# Trend line for new cases
create_trend_line(daily_df, 'date', 'new_confirmed_cases', 'new_deaths', 'new_recoveries', 'Daily trendline', country)


print('... Daily New Infections Differences')
new_df = pd.DataFrame([])
new_df['date'] = daily_df['date']
new_df['confirmed_cases'] = agg_df.groupby(['file_date']).confirmed.sum().values - daily_df.new_confirmed_cases
new_df['new_confirmed_cases'] = daily_df.new_confirmed_cases
create_stacked_bar(new_df, 'new_confirmed_cases', 'confirmed_cases', "Stacked bar of confirmed and new cases by day", country)


print('... Logarithmic plots')
log_plot(log_df, 'confirmed', 'Logarithmic plots for top {} most infected countries\nStarting from days since first 500 confirmed cases.'.format(top))

### Create Excel Spreadsheet ###
print('Creating excel spreadsheet report...')
workbook_writer = pd.ExcelWriter(os.path.join(reports_dir, report), engine='xlsxwriter')

# Add daily summary to spreadsheet
daily_df.to_excel(workbook_writer, sheet_name='daily figures')
workbook = workbook_writer.book

def get_image_types(path):
    '''
    get all the possible types of images in
    the passed directory path
    '''
    types = []
    for fn in glob.glob(os.path.join(path, '*.png')):
        types.append(fn.split('_',)[-1].split('.')[0])

    return types

# Get all images for each type
def read_images(path, graph_type):
    image_list = []
    for fn in glob.glob(os.path.join(path, '*_{}.png'.format(graph_type))):
        image_list.append(fn)
    images = {graph_type : image_list}
    return dict(images)

image_types = get_image_types(image_dir)

padding = 1 # Set padding for images in spreadsheet
for types in set(image_types):
    print('... reading images for:', types)
    type_dict = read_images(image_dir, types)

    # Add image to the worksheet
    worksheet = workbook.add_worksheet(name='{}_graphs'.format(types))
    for image in type_dict[types]:
        worksheet.insert_image('A' +str(padding), image)
        padding += 50
    padding = 1

workbook.close()
print('Done!')
