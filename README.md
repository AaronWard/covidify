# covid-19-analysis

![alt text](https://github.com/AaronWard/coronavirus-analysis/blob/master/tableau/spread.gif "Spread of coronavirus 22nd to 29th")

This repo is for analysis on the [corona virus / covid-19](https://www.who.int/health-topics/coronavirus) that will extract the latest data and generate reports. This repo will be <u>updated daily</u>.

<hr>

#### <u>Data</u>
- The data comes from the **Novel Coronavirus (COVID-19) Cases**, which is a live dataset provided by JHU CSSE. 
- Data available [here](https://github.com/CSSEGISandData/2019-nCoV).

#### <u>How to run</u>

- `git clone covid-19-analysis` and `cd` into repository
- run `pip install -r requirements.txt` to install dependencies
- run `./pipeline.sh`
- Results will be saved to `reports` folder. 


#### <u>To-do list</u>

- checkout the [kanban boards](https://github.com/AaronWard/covid-19-analysis/projects) to see work in progress

<hr>


### <u>Visualization of data</u>

This plots will be updated daily to visualize stats 3 attributes: 
- ```confirmed cases```
- ```deaths```
- ```recoveries```

Last updated: `2020-02-23`


##### Trend Line

This is an accumalitive sum trendline for all the confirmed cases, deaths and recoveries.
![alt text](./reports/images/confirmed_trendline.jpg)

##### Daily Trend Line

This is an daily sum trendline for all the confirmed cases, deaths and recoveries.
![alt text](./reports/images/new_confirmed_cases_trendline.jpg)

##### Stacked Daily Confirmed Cases

This stacked bar chart shows a daily sum of people who are currently confirmed (<i>red</i>) and the number of people who have been been confirmed on that day (<i>blue</i>)

![alt text](./reports/images/confirmed_cases_stacked_bar.jpg "Number of people actually with the virus for each day")


##### Daily Confirmed Cases

A count for new cases recorded on that given date, does not take past confirmations into account. 
![alt text](./reports/images/new_confirmed_cases_bar.jpg)

##### Daily Deaths

A count for deaths due to the virus recorded on that given date, does not take past deaths into account. 
![alt text](./reports/images/new_deaths_bar.jpg)

##### Daily Recoveries

A count for new recovories recorded on that given date, does not take past recoveries into account. 
![alt text](./reports/images/new_recoveries_bar.jpg)

##### Currently Infected

A count for all the people who are currently infected for a given date (confirmed cases - (recoveries + deaths))
![alt text](./reports/images/currently_infected_bar.jpg)


### Appendix
- All code written by me (Aaron Ward  - https://www.linkedin.com/in/aaronjward/)
- A special thank you to the [JHU CSSE](https://systems.jhu.edu/) team for maintaining the data
