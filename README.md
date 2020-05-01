# covid-19-analysis

![alt text](https://github.com/AaronWard/coronavirus-analysis/blob/master/tableau/spread.gif "Spread of coronavirus 22nd to 29th")

This repo is for analysis on the [corona virus / covid-19](https://www.who.int/health-topics/coronavirus) that will extract the latest data and generate reports. This repo will be <u>updated daily</u>.

## NOTICE
- I am currently working on some significant updates to this repo, including making this an installable package so some of the results be delayed. 


<hr>

#### <u>Data</u>
- The data comes from the **Novel Coronavirus (COVID-19) Cases**, which is a live dataset provided by JHU CSSE. 
- Data available [here](https://github.com/CSSEGISandData/2019-nCoV).

#### <u>How to install for Mac</u>

Introduction

Welcome to the Covidify Quick Start Guide. We are definitely glad you found us and we hope that you find our code useful and worthy of your contribution. The following documentation will help you get started on your contribution to our project. If you are an experienced developer you may want to skip these steps but hopefully you will find it useful.

GitHub

You've clearly found the URL address for the Covidify project, so how do you contribute? I would recommend you start by downloading the GitHub Desktop.

Once you find the project you want, you will want to locate the fork button in the upper right corner to clone a copy in your online profile or you can select the green "Clone or download" button and select "Open in Desktop" (Fig. 1). Regardless of the option you choose you will most likely want files on your computer so that you can get the code up and running on your machine.

 
Fig. 1

Lastly, if you don't really care to follow the instructions listed here you can also find them at GitHub.

Mac Set-up

Now that you have the repository downloaded and all of the files you need we just need to install the actual program on your machine so you can test functionality, and hopefully make contributions based on your observations.

The easiest solution would be to open terminal, then navigate to the folder you have your Covidify program files by using the "cd" function (Fig. 2). Once you are in the folder you can try running the command "pip install covidify". If you find yourself receiving an error then you may want to try updating your versions of Python and the package manager PIP. 

 
Fig. 2

If you continue receiving an error I recommend you download a program called Anaconda. This will allow you to manage environments and will be a huge benefit if you decide to continue your open source contributions. I recommend selecting the "64-Bit Graphic Installer" for Python 3.7 (Fig. 3).

 
Fig. 3

Once the file is downloaded and you open it you should see a setup wizard. As you are going through there will be an option for download location, you are welcome to place it wherever you like. If you want to install in the user but it’s now allowing (Fig. 4) just select MAC HD then select user again and it should be corrected (Fig 5).

 
Fig. 4

 
Fig. 5

Once everything is installed then you can go ahead and install pip using the code "sudo easy_install pip" or you can upgrade using "sudo pip install --upgrade pip".  If this does not get pip up and running then you may want to pursue other troubleshooting steps.

Hopefully by now you have read up on Anaconda and understand that you can manage multiple environments. We can set up the environment by navigating to our Covidify folder in terminal then running the code "conda create --name [name of program] [environment]", in my case I called it "conda create --name Covidify Python 3.6". Now that your environment is set up try running the "pip install covidify" code one more time. It should be successful, if not you may want to pursue additional trouble shooting steps. 

Please see the "How to use" section to efficiently use the Covidify program. Enjoy.


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

Last updated: `2020-03-02`


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
