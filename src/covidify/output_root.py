import os,datetime

#method to create output files, this method moved from
#data_prep.py, this file is the aggregate root so that external files
# or users are not able to make changes to the data_prep file directly
def output_data(out,df,daily_cases_df, log_df):
    # Create date of extraction folder
    data_folder = os.path.join('data', str(datetime.date(datetime.now())))
    save_dir = os.path.join(out, data_folder)

    if not os.path.exists(save_dir):
        os.system('mkdir -p ' + save_dir)

    print('Creating subdirectory for data...')
    print('...', save_dir)

    print('Saving...')
    csv_file_name = 'agg_data_{}.csv'.format(datetime.date(datetime.now()))
    df.astype(str).to_csv(os.path.join(save_dir, csv_file_name))
    print('...', csv_file_name)

    daily_cases_file_name = 'trend_{}.csv'.format(datetime.date(datetime.now()))
    daily_cases_df.astype(str).to_csv(os.path.join(save_dir, daily_cases_file_name))
    print('...', daily_cases_file_name)

    log_file_name = 'log_{}.csv'.format(datetime.date(datetime.now()))
    log_df.astype(str).to_csv(os.path.join(save_dir, log_file_name))
    print('...', log_file_name)

    print('Done!')