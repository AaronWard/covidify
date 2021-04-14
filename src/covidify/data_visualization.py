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
from abc import ABCMeta, abstractmethod

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

PRODUCT = Director.construct()

# Dynamic parameters
data_dir  = os.path.join(out, 'data', str(datetime.date(datetime.now())))
agg_file  = 'agg_data_{}.csv'.format(datetime.date(datetime.now()))
trend_file  = 'trend_{}.csv'.format(datetime.date(datetime.now()))
log_file  = 'log_{}.csv'.format(datetime.date(datetime.now()))
report  = Builder.create_report_name(country)

# import data
print('Importing Data...')
agg_df = pd.read_csv(os.path.join(data_dir, agg_file))
daily_df = pd.read_csv(os.path.join(data_dir, trend_file))
log_df = pd.read_csv(os.path.join(data_dir, log_file))

# Create place to save diagrams
image_dir =  os.path.join(out,'reports', 'images')
reports_dir =  os.path.join(out,'reports')

if not os.path.exists(image_dir):
    print('Creating reports folder...')
    os.system('mkdir -p ' + image_dir)

# Convert types
for col in ['confirmed', 'deaths', 'recovered']:
    agg_df[col] = agg_df[col].replace('', 0).astype(int)   

##### Create Graphs #####
print('Creating graphs...')
print('... Time Series Trend Line')
# Time Series Data Plots
Builder.create_trend_line(agg_df, 'file_date', 'confirmed', 'deaths', 'recovered', 'Accumulative trend', country)


print('... Daily Figures')
# Daily Figures Data Plots
daily_figures_cols = ['new_confirmed_cases', 'new_deaths', 'new_recoveries', 'currently_infected']
for col, rgb in zip(daily_figures_cols, ['tomato', 'lightblue', 'mediumpurple', 'green']):
    Builder.create_bar(daily_df, col, rgb, country)

# Trend line for new cases
Builder.create_trend_line(daily_df, 'date', 'new_confirmed_cases', 'new_deaths', 'new_recoveries', 'Daily trendline', country)


print('... Daily New Infections Differences')
new_df = pd.DataFrame([])
new_df['date'] = daily_df['date']
new_df['confirmed_cases'] = agg_df.groupby(['file_date']).confirmed.sum().values - daily_df.new_confirmed_cases
new_df['new_confirmed_cases'] = daily_df.new_confirmed_cases
#Builder.create_stacked_bar(new_df, 'new_confirmed_cases', 'confirmed_cases', "Stacked bar of confirmed and new cases by day", country)


print('... Logarithmic plots')
#Builder.log_plot(log_df, 'confirmed', 'Logarithmic plots for top {} most infected countries\nStarting from days since first 500 confirmed cases.'.format(top))

### Create Excel Spreadsheet ###
print('Creating excel spreadsheet report...')
workbook_writer = pd.ExcelWriter(os.path.join(reports_dir, report), engine='xlsxwriter')

# Add daily summary to spreadsheet
daily_df.to_excel(workbook_writer, sheet_name='daily figures')  
workbook = workbook_writer.book

#image_types = Builder.get_image_types(image_dir)

padding = 1 # Set padding for images in spreadsheet
for types in set(Builder.get_image_types(image_dir)): # set(image_types)
    print('... reading images for:', types)
    type_dict = Builder.read_images(image_dir, types)
    
    # Add image to the worksheet
    worksheet = workbook.add_worksheet(name='{}_graphs'.format(types))
    for image in type_dict[types]:
        worksheet.insert_image('A' +str(padding), image) 
        padding += 50
    padding = 1
    
workbook.close()
print('Done!')

class IBuilder(metaclass=ABCMeta):
    @staticmethod
    def create_report_name(self, country):
        "Change report name if country specified, otherwise default"

    @staticmethod
    def create_title(fig_title, country):
        "Change title to new country, otherwise create default title"

    @staticmethod
    def create_save_file(col, country, graph_type):
        "Change file name to new country, otherwise create default file name"

    @staticmethod
    def create_trend_line(tmp_df, date_col, col, col2, col3, fig_title, country):
        "Plot and save trendline graph"

    @staticmethod
    def create_bar(tmp_df, col, rgb, country):
        "Plot and save bar graph"

    @staticmethod
    def create_stacked_bar(tmp_df, col1, col2, fig_title, country):
        "Plot and save stacked graph"

    @staticmethod
    def log_plot(tmp, col, fig_title):
        "Plot logarithmic scale to compare countries infection rates"

    @staticmethod
    def get_image_types(path):
        "Get types for all images"

    @staticmethod
    def read_images(path, graph_type):
        "Get all images for each type"

class Builder(IBuilder):
    def __init__(self):
        self.product = Product()

    #change report name if country specified
    def create_report_name(self, country):
        if country:
            self.report = '{}_report_{}.xlsx'.format(country, datetime.date(datetime.now()))
            self.country = country
            # return '{}_report_{}.xlsx'.format(country, datetime.date(datetime.now()))
            return self
        else:
            return self #'report_{}.xlsx'.format(datetime.date(datetime.now()))

    def create_title(self, fig_title, country):
        if country:
            self.fig_title = fig_title
            self.country = country
            return fig_title + ' for ' + country
        else:
            return fig_title 
    
    def create_save_file(self, col, country, graph_type):
        if country:
            self.col = col
            self.country = country
            self.graph_type = graph_type
            return '{}_{}_{}.png'.format(country, col, graph_type)
        else:
            return '{}_{}.png'.format(col, graph_type)

    # Plot and save trendline graph
    def create_trend_line(self, tmp_df, date_col, col, col2, col3, fig_title, country):
        fig, ax = plt.subplots(figsize=(20,10))
        tmp_df.groupby([date_col])[[col, col2, col3]].sum().plot(ax=ax, marker='o')
        ax.set_title(create_title(fig_title, country))
        fig = ax.get_figure()
        fig.savefig(os.path.join(image_dir, create_save_file(col, country, 'trendline')))

    def create_bar(self, tmp_df, col, rgb, country):
        tmp_df = tmp_df.tail(120)
        fig, ax = plt.subplots(figsize=(20,10))
        tmp = tmp_df.groupby(['date'])[[col]].sum()
        ax.set_title(create_title(col, country))
        tmp.plot.bar(ax=ax, rot=90, color=rgb)
        fig = ax.get_figure()
        fig.savefig(os.path.join(image_dir, create_save_file(col, country, 'bar')))

    def create_stacked_bar(self, tmp_df, col1, col2, fig_title, country):
        tmp_df = tmp_df.tail(120)
        tmp_df = tmp_df.set_index('date')
        fig, ax = plt.subplots(figsize=(20,10))
        ax.set_title(create_title(fig_title, country))
        tmp_df[[col2, col1]].plot.bar(ax=ax, rot=90, stacked=True)
        fig = ax.get_figure()
        fig.savefig(os.path.join(image_dir, create_save_file(col2, country, 'stacked_bar')))

    def log_plot(self, tmp, col, fig_title):
        #Plot on a logarithmic scale for comparing countries infection rates
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
        fig.savefig(os.path.join(image_dir, create_save_file(col, country=None, graph_type='log')))

    def get_image_types(self, path):
        # get all the possible types of images in the passed directory path
        types = []
        for fn in glob.glob(os.path.join(path, '*.png')):
            types.append(fn.split('_',)[-1].split('.')[0])
        return types

    # Get all images for each type
    def read_images(self, path, graph_type):
        image_list = []
        for fn in glob.glob(os.path.join(path, '*_{}.png'.format(graph_type))):
            image_list.append(fn)    
        images = {graph_type : image_list}
        return dict(images)

class Product():
    def __init__(self):
        "initialize as empty"
        self.tmp = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)
        self.tmp_df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)
        self.report = 'report_{}.xlsx'.format(datetime.date(datetime.now()))
        self.country = self.fig_title = self.col = self.graph_type = ""

class Director():
    @staticmethod
    def construct():
        return Builder()\
        .create_report_name(country)\
        .create_title(Product.fig_title, country)\
        .create_save_file(col, country, 'log')\
        .create_stacked_bar(new_df, 'new_confirmed_cases', 'confirmed_cases', "Stacked bar of confirmed and new cases by day", country)\
        .log_plot(log_df, 'confirmed', 'Logarithmic plots for top {} most infected countries\nStarting from days since first 500 confirmed cases.'.format(top))