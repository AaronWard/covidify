# coronavirus-analysis

![alt text](https://github.com/AaronWard/coronavirus-analysis/blob/master/tableau/spread.gif "Spread of coronavirus 22nd to 29th")



This repo for analysis on the [corona virus](https://www.who.int/health-topics/coronavirus). This includes: <br>

- [X] Script for extracting google sheet data and preprocessing it into a time series dataset
- [X] Do some data exploration using tableau
- [ ] Do some data exploration using pandas
- [ ] Do some time series analysis and apply machine learning to predict the potential confirmed cases in the future.


### Data
- The data come from the **Novel Coronavirus (2019-nCoV) Cases**,  which is a live dataset provided by JHU CSSE. 
- Data available [here](https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w).
- In `data_prep.py` the data extracts the latest entry for each date, and aggregates all the records into a time series dataset.
- The script is reproducible, but you will need to enable Google API Access to run it yourself. Follow [this](https://developers.google.com/sheets/api/quickstart/python) tutorial.


#### News Sources and Materials
- [Live Tracker Map](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
- [How To Stay Safe](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public)
- [Latest Google News Feed](https://www.google.com/search?q=coronavirus&tbm=nws&sxsrf=ACYBGNTsjxRI2IRU0X88bcksb5doQCKzDA:1580388795464&source=lnt&tbs=qdr:d&sa=X&ved=0ahUKEwjiwYqGr6vnAhWYUt4KHQZQB-QQpwUIIA&biw=2133&bih=1052&dpr=0.9)