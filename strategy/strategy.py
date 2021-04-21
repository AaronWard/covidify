class Strategy:
        def get_date(self, last_update):
            pass
        def get_csv_date(self, file):
            pass
        def clone_repo(TMP_FOLDER, REPO):
            pass
        def clean_sheet_names(self, new_ranges):
            pass
        def clean_data(self, tmp_df):
            pass
        def get_data(self, cleaned_sheets):
            pass
        def clean_last_updated(self, last_update):
            pass
        def drop_duplicates(self, df_raw):
            pass


class Data_prep3( Strategy ):
    def get_date(self, last_update):
        return parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
    def get_csv_date(self, file):
        return get_date(file.split('.')[0] + ' ') 
    def clone_repo(TMP_FOLDER, REPO):
        print('Cloning Data Repo...')
        git.Git(TMP_FOLDER).clone(REPO)
    def clean_sheet_names(self, new_ranges):
        indices =    []
        numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
        return numeric_sheets
    def clean_data(self, tmp_df):
        if 'Demised' in tmp_df.columns:
            tmp_df.rename(columns={'Demised':'Deaths'}, inplace=True)
        if 'Country/Region' in tmp_df.columns:
            tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)
        if 'Province/State' in tmp_df.columns:
            tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
        if 'Last Update' in tmp_df.columns:
            tmp_df.rename(columns={'Last Update':'datetime'}, inplace=True)
        if 'Suspected' in tmp_df.columns:
            tmp_df = tmp_df.drop(columns='Suspected')
        for col in tmp_df.columns:
            tmp_df[col] = tmp_df[col].fillna(0)
        tmp_df.columns = map(str.lower, tmp_df.columns) 
        return tmp_df
    def get_data(self, cleaned_sheets):
        all_csv = []
        for file in sorted(sheets):
            if 'csv' in file:
                print('...', file)
                tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, header=0, parse_dates=['Last Update'])
                tmp_df = tmp_df[keep_cols]
                tmp_df[numeric_cols] = tmp_df[numeric_cols].fillna(0)
                tmp_df[numeric_cols] = tmp_df[numeric_cols].astype(int)
                tmp_df['Province/State'].fillna(tmp_df['Country/Region'], inplace=True)

                tmp_df['Last Update'] = tmp_df['Last Update'].apply(clean_last_updates)
                tmp_df['date'] = tmp_df['Last Update'].apply(get_date)
                tmp_df['file_date'] = get_csv_date(file)

                all_csv.append(tmp_df)
        df_raw = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)
        df_raw = df_raw.sort_values(by=['Last Update'])           
        return df_raw
    def clean_last_updates(self, last_update):
        date = parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
        time = parse(str(last_update).split(' ')[1]).strftime('%H:%M:%S')
        parsed_date = str(date) + ' ' + str(time)
        return parsed_date
    def drop_duplicates(self, df_raw):
        days_list = []
        for datetime in df_raw.date.unique():
            tmp_df = df_raw[df_raw.date == datetime]
            tmp_df = tmp_df[df_raw.file_date != datetime].sort_values(['file_date']).drop_duplicates('Province/State', keep='last')
            days_list.append(tmp_df)
        return days_list



class Data_prep4( Strategy ):
    def get_date(self, last_update):
        return parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
    def get_csv_date(self, file):
        return get_date(file.split('.')[0] + ' ') 
    def clone_repo(TMP_FOLDER, REPO):
        print('Cloning Data Repo...')
        git.Git(TMP_FOLDER).clone(REPO)
    def clean_sheet_names(new_ranges):
        indices =    []
        numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
        return numeric_sheets
    def clean_data(self, tmp_df):
        if 'Demised' in tmp_df.columns:
        tmp_df.rename(columns={'Demised':'Deaths'}, inplace=True)
        if 'Country/Region' in tmp_df.columns:
            tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)  
        if 'Province/State' in tmp_df.columns:
            tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
        if 'Last Update' in tmp_df.columns:
            tmp_df.rename(columns={'Last Update':'datetime'}, inplace=True)   
        if 'Suspected' in tmp_df.columns:
            tmp_df = tmp_df.drop(columns='Suspected')
        for col in tmp_df.columns:
            tmp_df[col] = tmp_df[col].fillna(0)       
        #Lower case all col names
        tmp_df.columns = map(str.lower, tmp_df.columns) 
        return tmp_df
    def get_data(self, cleaned_sheets):
        all_csv = []
        for file in tqdm(sorted(sheets), desc='... importing data: '):
            if 'csv' in file:
                tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, header=0, parse_dates=['Last Update'])
                tmp_df = tmp_df[keep_cols]
                tmp_df[numeric_cols] = tmp_df[numeric_cols].fillna(0)
                tmp_df[numeric_cols] = tmp_df[numeric_cols].astype(int)
                tmp_df['Province/State'].fillna(tmp_df['Country/Region'], inplace=True)
                tmp_df['Last Update'] = tmp_df['Last Update'].apply(clean_last_updated)
                tmp_df['date'] = tmp_df['Last Update'].apply(get_date)
                tmp_df['file_date'] = get_csv_date(file)
                all_csv.append(tmp_df)
        df_raw = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)
        df_raw = df_raw.sort_values(by=['Last Update'])
        frames = drop_duplicates(df_raw)
        tmp = pd.concat(frames, axis=0, ignore_index=True, sort=True) 
        return tmp
    def clean_last_updates(self, last_update):
        date = parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
        time = parse(str(last_update).split(' ')[1]).strftime('%H:%M:%S')
        parsed_date = str(date) + ' ' + str(time)
        return parsed_date
    def drop_duplicates(self, df_raw):
        days_list = []
        for datetime in df_raw.date.unique():
            tmp_df = df_raw[df_raw.date == datetime]
            tmp_df = tmp_df.sort_values(['Last Update']).drop_duplicates('Province/State', keep='last')
            days_list.append(tmp_df)
        return days_list

    class Context:
        private strategy: Strategy
        def setStrategy(Strategy s)
            this.strategy = s
        def execute_get_date()
            strategy.get_date()
        def execute_get_csv_date()
            strategy.get_csv_date()
        def execute_clone_repo()
            strategy.clone_repo()
        def execute_cleaned_sheets()
            strategy.cleaned_sheets()
        def execute_clean_sheet_names()
            strategy.clean_sheet_names()
        def execute_clean_data()
            strategy.clean_data()
        def execute_get_data()
            strategy.get_data()
        def execute_clean_last_updated()
            strategy.clean_last_updated()
        def execute_drop_duplicates()
            strategy.drop_duplicates()


class Application:
    Context context: object
    context.setStrategy(new Data_prep3())
    result = context.execute_get_data()