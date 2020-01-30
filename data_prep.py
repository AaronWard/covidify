from __future__ import print_function
import pandas as pd
import numpy as np
import os
import pickle
import os.path
from datetime import datetime, date, time 
import pyarrow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

def clean_sheet_names(sheets):
    '''
    Get rid of the duplicate sheets, only take the sheets from the 
    latest point in the day
    '''
    new_ranges = []
    indices = []
    
    #Get all the tabs in the sheet 
    for s in sheets:
        new_ranges.append(s.get("properties", {}).get("title"))
        
    #split the names to just get the date
    clean_new_ranges = new_ranges.copy()
    for i, x in enumerate(clean_new_ranges):
        clean_new_ranges[i] = x.split('_')[0]    
    
    #Get the index of the latest tab for each date
    for item in set(clean_new_ranges):
        indices.append(clean_new_ranges.index(item))

    clean_new_ranges = []
    # Return wanted tabs for the sheet extraction
    for index in sorted(indices):
        clean_new_ranges.append(new_ranges[index])

    return clean_new_ranges
    


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w'

"""Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
        
#get all the sheet names for ranges when querying
service = build('sheets', 'v4', credentials=creds)
sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
sheets = sheet_metadata.get('sheets', '')

# Clean the result to the sheet tabs we want
cleaned_ranges = clean_sheet_names(sheets)


def get_data(sheet_range):
    tmp_df = pd.DataFrame([])
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=sheet_range).execute()

    header = result.get('values', [])[0]   # Assumes first line is header!
    values = result.get('values', [])[1:]  # Everything else is data.
    
    
    # rows with no deaths and recovered vals have shorter lists
    # impute missing values with zeros
    for i, row in enumerate(values):
        if len(row) < len(header):
            extra_zeros = (len(header) - len(row))
            values[i] += [0] * extra_zeros

    # Create Dataframe
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        tmp = pd.concat(all_data, axis=1)
        
    print('...', sheet_range)
    return tmp
   
df_list = []
print('Getting sheets to preprocess')
for sheet_range in cleaned_ranges:
    df_list.append(get_data(sheet_range))

# Now that we have all the data we now need to clean it 
# - Fill null values
# - remore suspected values
# - change column names

def clean_data(tmp_df):
    if 'Demised' in tmp_df.columns:
        tmp_df.rename(columns={'Demised':'Deaths'}, inplace=True)

    if 'Country/Region' in tmp_df.columns:
        tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)
    
    if 'Province/State' in tmp_df.columns:
        tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
      
    if 'Last Update' in tmp_df.columns:
        tmp_df.rename(columns={'Last Update':'date'}, inplace=True)
        
    if 'Suspected' in tmp_df.columns:
        tmp_df = tmp_df.drop(columns='Suspected')

    for col in tmp_df.columns:
        tmp_df[col] = tmp_df[col].fillna(0)
    
    #Lower case all col names
    tmp_df.columns = map(str.lower, tmp_df.columns)    
    
    return tmp_df

cleaned_dataframes = []

print('Cleaning dataframes...')
for frame in df_list:
    cleaned_dataframes.append(clean_data(frame))


#Impute the missing columns in the early stages with 0 values (recovered and deaths)
print('Imputing missing columns...')
cleaned_dataframes[-1]['recovered'] = [0] * (cleaned_dataframes[-1]).shape[0]
cleaned_dataframes[-1]['deaths'] = [0] * (cleaned_dataframes[-1]).shape[0]

cleaned_dataframes[-2]['recovered'] = [0] * (cleaned_dataframes[-2]).shape[0]
cleaned_dataframes[-2]['deaths'] = [0] * (cleaned_dataframes[-2]).shape[0]

print('Concatenating all sheet dataframes into one...')
final_df = pd.concat(cleaned_dataframes, sort=True)

def convert_date_time(date):
    
    try:
        if 'PM' in date:
            return datetime.strptime(date,'%m/%d/%Y %H:%M PM').date()
        elif 'AM' in date:
            return datetime.strptime(date,'%m/%d/%Y %H:%M AM').date()
        else:
            return datetime.strptime(date,'%m/%d/%Y %H:%M').date()
    except:
        return datetime.strptime(date, '%m/%d/%y %H:%M PM').date()

# Make sure dates are all the same format
final_df['date'] = final_df['date'].astype(str)
final_df['date'] = final_df['date'].apply(convert_date_time)

# sheets need to be sorted by date value
print('Sorting by date...')
final_df = final_df.sort_values('date')

print('Saving...')
file_name = './data/updated_{}.parquet.gzip'.format(datetime.date(datetime.now()))
final_df.astype(str).to_parquet(file_name, compression='gzip')

