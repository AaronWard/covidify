# covidify  [![PyPi Version](https://img.shields.io/pypi/v/covidify.svg)](https://pypi.python.org/pypi/covidify/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/covidify) ![PyPI - License](https://img.shields.io/pypi/l/covidify?color=yellow) [![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/covidify/)
![logo](./resources/cov_logo.png "logo")

<p align="center">
  <a href="#features">Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Installation</a> •
  <a href="#download">Data Source</a> •
  <a href="#credits">Credits</a> •
</p>
<hr>


## Features
Covidify downloads the latest [covid-19](https://www.who.int/health-topics/coronavirus) data for confirmed cases, deaths and recoveries. 
- Creates a time series dataset
- Creates a daily stats dataset 
- Generate visualizations
- Filter reports by country
- List all countries affected
- Generates an excel report including all of the above 

![logo](./resources/run.gif "logo")


<hr>


## Installation

- ```pip install covidify```

## How to use

```powershell
$ covidify
Usage: covidify [OPTIONS] COMMAND [ARGS]...

  ☣  COVIDIFY ☣

   - use the most up-to-date data to generate reports of 
     confirmed cases, fatalities and recoveries.

Options:
  --help  Show this message and exit.

Commands:
  list  List all the countries that have confirmed cases.
  run   Generate reports for global cases or refine by country.
```

```powershell
$ covidify run --help
Usage: covidify run [OPTIONS]

Options:
  --output TEXT   Folder to output data and reports [Default:
                  /Users/award40/Desktop/covidify-output/]
  --source TEXT   There are two datasources to choose from, John Hopkins
                  github repo or wikipedia -- options are git or wiki
                  respectively [Default: git]
  --country TEXT  Filter reports by a country [Default: Global cases]
  --help          Show this message and exit.
```


**Example Commands:**
```powershell
# Will default to desktop folder 
# for output and github for datasource
covidify run 
```


```powershell
# Specify output folder and source
covidify run --output=/Users/award40/Documents/projects-folder --source=git
```

```powershell
# Filter reports by country
covidify run --country="South Korea"
```

```powershell
# List all countries affected 
covidify list --countries
```

<hr>

### Visualization of data
This plots will be updated daily to visualize stats 3 attributes: 
- ```confirmed cases```
- ```deaths```
- ```recoveries```


##### Trend Line

This is an accumulative sum trendline for all the confirmed cases, deaths and recoveries.
![alt text](./reports/images/confirmed_trendline.png)

##### Daily Trend Line

This is a daily sum trendline for all the confirmed cases, deaths and recoveries.
![alt text](./reports/images/new_confirmed_cases_trendline.png)

##### Stacked Daily Confirmed Cases

This stacked bar chart shows a daily sum of people who are currently confirmed (<i>red</i>) and the number of people who have been been confirmed on that day (<i>blue</i>)

![alt text](./reports/images/confirmed_cases_stacked_bar.png "Number of people actually with the virus for each day")


##### Daily Confirmed Cases

A count for new cases recorded on that given date, does not take past confirmations into account. 
![alt text](./reports/images/new_confirmed_cases_bar.png)

##### Daily Deaths

A count for deaths due to the virus recorded on that given date, does not take past deaths into account. 
![alt text](./reports/images/new_deaths_bar.png)

##### Daily Recoveries

A count for new recoveries recorded on that given date, does not take past recoveries into account. 
![alt text](./reports/images/new_recoveries_bar.png)

##### Currently Infected

A count for all the people who are currently infected for a given date (confirmed cases - (recoveries + deaths))
![alt text](./reports/images/currently_infected_bar.png)


<hr>

### Data Source
- The data comes from the **Novel Coronavirus (COVID-19) Cases**, which is a live dataset provided by JHU CSSE. 
- Data available [here](https://github.com/CSSEGISandData/2019-nCoV).


### Credits
- Written by me (Aaron Ward  - https://www.linkedin.com/in/aaronjward/)
- A special thank you to the [JHU CSSE](https://systems.jhu.edu/) team for maintaining the data
- Also a special thank you to @ajaymaity for bug fixes 🎉



#### To-do list
- checkout the [kanban boards](https://github.com/AaronWard/covidify/projects) to see work in progress