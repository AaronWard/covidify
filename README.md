# covid-19-analysis

![alt text](https://github.com/AaronWard/coronavirus-analysis/blob/master/tableau/spread.gif "Spread of coronavirus 22nd to 29th")

This repo is for analysis on the [corona virus / covid-19](https://www.who.int/health-topics/coronavirus) that will extract the latest data and generate reporting visualizations and information sheets. This repo will will be <u>updated daily</u>.

#### Data:
- The data come from the **Novel Coronavirus (COVID-19) Cases**, which is a live dataset provided by JHU CSSE. 
- Data available [here](https://github.com/CSSEGISandData/2019-nCoV).

#### How to run:
- `git clone covid-19-analysis` and `cd` into repository
- run `pip install -r requirements.txt` to install dependencies
- run `./pipeline.sh`
- Results will be saved to `reports` folder. 

#### To-Do List:

- checkout the [kanban boards](https://github.com/AaronWard/covid-19-analysis/projects) to see future work on this project

## Visualization of data:

This plots will be updated <u>daily</u> to visualize the trend in accumalitive sums and the daily counts for 3 attributes: 
- **<i>Confirmed Cases</i>**
- **<i>Deaths</i>**
- **<i>Recoveries.</i>**

Last updated: `2020-02-11`

**Trend Line**

This is an accumalitive sum trendline for all the confirmed cases, deaths and recoveries.
![alt text](./reports/images/confirmed_trendline.jpg)

**Daily Trend Line**

This is an daily sum trendline for all the confirmed cases, deaths and recoveries.
![alt text](./reports/images/new_confirmed_cases_trendline.jpg)

**Stacked Daily Confirmed Cases**

This stacked bar chart shows a daily sum of people who are currently confirmed (<i>red</i>) and the number of people who have been been confirmed on that day (<i>blue</i>)

![alt text](./reports/images/confirmed_cases_stacked_bar.jpg "Number of people actually with the virus for each day")


**Daily Confirmed Cases**

A count for new cases recorded on that given date, does not take past confirmations into account. 
![alt text](./reports/images/new_confirmed_cases_bar.jpg)

**Daily Deaths**

A count for deaths due to the virus recorded on that given date, does not take past deaths into account. 
![alt text](./reports/images/new_deaths_bar.jpg)

**Daily Recoveries**

A count for new recovories recorded on that given date, does not take past recoveries into account. 
![alt text](./reports/images/new_recoveries_bar.jpg)


## Additional information and thanks
- All code written by me (Aaron Ward  - https://www.linkedin.com/in/aaronjward/)
- A special thank you to the [JHU CSSE](https://systems.jhu.edu/) team for maintaining the data