class DataProcessor:
        def get_date():
            return parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")

        def get_csv_date()
            return get_date(f.split('.')[0] + ' ')

        def clone_repo()
            print('Cloning Data Repo...')
            git.Git(TMP_FOLDER).clone(REPO)

        @abstractmethod
        def cleaned_sheets():
            pass

        @abstractmethod
        def clean_sheet_names():
            pass

        @abstractmethod
        def clean_data():
            pass

        @abstractmethod
        def get_data():
            pass


class Github(DataProcessor):
        def cleaned_sheet_names(self):
            return [x for x in new_ranges if re.search(r'\d', x)]

        def clean_data(self):
            tmp_df = df.copy()
            if 'Demised' in tmp_df.columns:
                tmp_df.rename(columns={'Demised':'deaths'}, inplace=True)
            if 'Country/Region' in tmp_df.columns:
                tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)
            if 'Country_Region' in tmp_df.columns:
                tmp_df.rename(columns={'Country_Region':'country'}, inplace=True)
            if 'Province/State' in tmp_df.columns:
                tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
            if 'Province_State' in tmp_df.columns:
                tmp_df.rename(columns={'Province_State':'province'}, inplace=True)
            if 'Last Update' in tmp_df.columns:
                tmp_df.rename(columns={'Last Update':'datetime'}, inplace=True)
            if 'Last_Update' in tmp_df.columns:
                tmp_df.rename(columns={'Last_Update':'datetime'}, inplace=True)
            #Lower case all col names
            tmp_df.columns = map(str.lower, tmp_df.columns) 
            for col in tmp_df[NUMERIC_COLS]:
                tmp_df[col] = tmp_df[col].fillna(0)
                tmp_df[col] = tmp_df[col].astype(int)
            return tmp_df

        def get_data(self):
            all_csv = []
            # Import all CSV's
            for f in tqdm(sorted(cleaned_sheets), desc='... loading data: '):
                if 'csv' in f:
                    try:
                        tmp_df = pd.read_csv(os.path.join(DATA, f), index_col=None,header=0, parse_dates=['Last Update'])  
                    except:
                        # Temporary fix for JHU's bullshit data management
                        tmp_df = pd.read_csv(os.path.join(DATA, f), index_col=None,header=0, parse_dates=['Last_Update'])  
                    tmp_df = clean_data(tmp_df)
                    tmp_df['date'] = tmp_df['datetime'].apply(get_date) # remove time to get date
                    tmp_df['file_date'] = get_csv_date(f) #Get date of csv from file name
                    tmp_df = tmp_df[KEEP_COLS]
                    tmp_df['province'].fillna(tmp_df['country'], inplace=True) #If no region given, fill it with country
                    all_csv.append(tmp_df)
            df_raw = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)  # concatenate all csv's into one df
            df_raw = fix_country_names(df_raw)    # Fix mispelled country names
            df_raw = df_raw.sort_values(by=['datetime'])
            return df_raw


class DataPrep(DataProcessor):
    def clean_sheet_names(self):
        indices =    []
        # Remove all sheets that dont have a numeric header
        numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
        return numeric_sheets

    def clean_data(self):
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

    @abstractmethod
    def get_data(self):
        pass


class Data_prep3(DataPrep):
        def get_data(self):
            all_csv = []
            # Import all CSV's
            for file in sorted(sheets):
                if 'csv' in file:
                    print('...', file)
                    tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, 
                                        header=0, parse_dates=['Last Update'])
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

    class Data_prep4(DataPrep):
        def get_data(self):
            all_csv = []
        for file in tqdm(sorted(sheets), desc='... importing data: '):
            if 'csv' in file:
                tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, 
                                    header=0, parse_dates=['Last Update'])
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
