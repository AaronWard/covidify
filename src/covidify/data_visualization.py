import pandas as data
import os.path
import json
import datetime as dt
from datetime import datetime
from regression import *

data.options.mode.chained_assignment = None
samples = 5			#Points to be sampled for regression.
time_series = data.read_csv("https://raw.githubusercontent.com/coder-amey/COVID-19-Global_Data/master/time-series/Global_aggregated.csv")		#Load the time-series.

latest_tally = time_series.loc[time_series["Date"] == time_series.Date.unique()[-1]]		#Date of last update.
yest_tally = time_series.loc[time_series["Date"] == time_series.Date.unique()[-2]]		#Previous day's tally.
predictables = time_series.loc[time_series["Date"] == time_series.Date.unique()[-samples]]	#Dataframe of regions with enough data for a prediction.

#Add new columns to track increments in each type of cases (initialized as current number of cases).
latest_tally["CNF_inc"] = latest_tally["Confirmed"].copy()
latest_tally["RCV_inc"] = latest_tally["Recovered"].copy()
latest_tally["DCS_inc"] = latest_tally["Deceased"].copy()

#Subtract yesterday's tally from the respective cases from every region.
for region in yest_tally.Region.unique():
	window = latest_tally.Region == region
	window_yest = yest_tally.Region == region
	idx = latest_tally[window].index
	latest_tally.loc[idx, "CNF_inc"] = latest_tally[window].iat[0, 2] - yest_tally[window_yest].iat[0, 2]
	latest_tally.loc[idx, "RCV_inc"] = latest_tally[window].iat[0, 3] - yest_tally[window_yest].iat[0, 3]
	latest_tally.loc[idx, "DCS_inc"] = latest_tally[window].iat[0, 4] - yest_tally[window_yest].iat[0, 4]

#Insert and populate columns for active cases and their increments in every region.
latest_tally["Active"] = latest_tally["Confirmed"] - latest_tally["Recovered"] - latest_tally["Deceased"]
latest_tally["ACT_inc"] = latest_tally["CNF_inc"] - latest_tally["RCV_inc"] - latest_tally["DCS_inc"]

#Calculate and store the predictions for each region. [Vectorized approach]
cnf_predictables = []
cnf_matrix =[]
dcs_predictables = []
dcs_matrix = []
latest_tally = latest_tally.set_index("Region")		#Set Region as the index for aligning prediction results.
for region in predictables.Region.unique():
	slice = time_series.Region == region
	if(time_series[slice].Confirmed.tolist()[-samples] > 0):		#Ensure that only non-zero entries are passed.
		cnf_predictables.append(region)								#Mark as predictable region.
		cnf_matrix.append(time_series[slice].Confirmed.tolist()[-samples:])
	
	if(time_series[slice].Deceased.tolist()[-samples] > 0):		#Ensure that only non-zero entries are passed.
		dcs_predictables.append(region)								#Mark as predictable region.
		dcs_matrix.append(time_series[slice].Deceased.tolist()[-samples:])

#Predict new infections:
predictions = maths.rint(exp_predict(samples, *exp_reg(cnf_matrix)))
predictions = data.Series(data = predictions, index = cnf_predictables)
#For regions with insufficient data-points, mark current tally as the next prediction.
for region in [region for region in latest_tally.index if region not in cnf_predictables]:
	predictions[region] = latest_tally.loc[region].Confirmed
latest_tally["CNF_pred"] = predictions

#Predict new deaths:
predictions = maths.rint(exp_predict(samples, *exp_reg(dcs_matrix)))
predictions = data.Series(data = predictions, index = dcs_predictables)
#For regions with insufficient data-points, mark current tally as the next prediction.
for region in [region for region in latest_tally.index if region not in dcs_predictables]:
	predictions[region] = latest_tally.loc[region].Deceased
latest_tally["DCS_pred"] = predictions

#Re-index, re-order and sort the columns. Resetting the index is necessary for maintaining compatibility with JSON format.
latest_tally = latest_tally.reset_index()
latest_tally = latest_tally[["Region", "Confirmed", "CNF_inc", "Active", "ACT_inc", "Recovered", "RCV_inc", "Deceased", "DCS_inc", "CNF_pred", "DCS_pred"]].sort_values(by = ["Active", "Deceased", "Confirmed"], ascending = False, ignore_index = True)
latest_tally = latest_tally.set_index("Region")

#Write the table in the JSON file.
base_dir = os.path.join(os.path.dirname(__file__), "../")		#Obtain the path to the base directory for absolute addressing.
summary = json.loads(latest_tally.to_json(orient = 'split', index = True))
summary["update_time"] = datetime.now().strftime("%d %B %Y, %H:%M") + " IST"			#Include last update time.
with open(base_dir + 'data/Global_summary.json', 'w') as jfile:
	json.dump(summary, jfile)

#Prepare charting data.
chart_data = dict()

time_series.Date = data.to_datetime(time_series.Date, dayfirst = True)	#Make dates compatible with javascript.
last_day = time_series.Date.tolist()[-1] + dt.timedelta(days = 1) 			#Last day (including the prediction).
epoch = time_series.Date.tolist()[0]														#First day of recorded data.
time_series.Date = time_series.Date.dt.strftime("%Y-%m-%d")				#Shorten dates to save space.

chart_data["regions"] = list(latest_tally.index.unique())							#Regions sorted in decreasing order of cases.
chart_data["interval"] = [epoch.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")]			#Store range of dates.
chart_data["update_time"] = datetime.now().strftime("%d %B %Y, %H:%M") + " IST"		#Include last update time.
chart_data["series"] = dict()

#Create and enlist region-wise objects containing series of different cases over time.
for region in chart_data["regions"]:
	df = time_series[time_series.Region == region]
	chart_data["series"][region] = dict()
	chart_data["series"][region]["Date"] = df.Date.tolist()
	chart_data["series"][region]["Infected"] = df.Confirmed.astype(int, copy = True).tolist()
	chart_data["series"][region]["Active"] = (df.Confirmed - df["Recovered"] - df.Deceased).astype(int, copy = True).tolist()
	chart_data["series"][region]["Recovered"] = df["Recovered"].astype(int, copy = True).tolist()
	chart_data["series"][region]["Deceased"] = df.Deceased.astype(int, copy = True).tolist()
	#Read and store predictions for the current region.
	df = latest_tally[latest_tally.index == region]	
	chart_data["series"][region]["Prediction"] = df.CNF_pred.tolist() + df.DCS_pred.tolist()

#Write the charting data in the JSON file.
with open(base_dir + 'data/Global_series.json', 'w') as jfile:
	json.dump(chart_data, jfile)
