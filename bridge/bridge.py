import os
import sys
import git
from datetime import datetime, date, time 
from dateutil.parser import parse

REPO = 'https://github.com/CSSEGISandData/COVID-19.git'
TMP_FOLDER = '/tmp/corona/'
TMP_GIT = os.path.join(TMP_FOLDER, 'COVID-19')
DATA = os.path.join(TMP_GIT, 'csse_covid_19_data/csse_covid_19_daily_reports/')
out = './'

class DataAccessor:
    def __init__(self, cleaner):
        self.cleaner = cleaner

    def get_date(self, last_update):
        pass

    def get_csv_date(self, file):
        pass

    def get_data(self, cleaned_sheets):
        pass


class AdvancedDataAccessor(DataAccessor):
    def __init__(self, cleaner):
        self.cleaner = cleaner
        # self.REPO = 'https://github.com/CSSEGISandData/COVID-19.git'
        # self.TMP_FOLDER = '/tmp/corona/'
        # self.TMP_GIT = os.path.join(TMP_FOLDER, 'COVID-19')
        # self.DATA = os.path.join(TMP_GIT, 'csse_covid_19_data/csse_covid_19_daily_reports/')
        # self.out = './'

    def get_date(last_update):
        return parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")

    def get_csv_date(file):
        return get_date(file.split('.')[0] + ' ')   

    def get_data(cleaned_sheets):
        all_csv = []
        # Import all CSV's
        for file in tqdm(sorted(sheets), desc='... importing data: '):
            if 'csv' in file:
                # print('...', file)
                tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, header=0, parse_dates=['Last Update'])
                tmp_df = tmp_df[keep_cols]
                tmp_df[numeric_cols] = tmp_df[numeric_cols].fillna(0)
                tmp_df[numeric_cols] = tmp_df[numeric_cols].astype(int)
                tmp_df['Province/State'].fillna(tmp_df['Country/Region'], inplace=True) #If no region given, fill it with country

                tmp_df['Last Update'] = tmp_df['Last Update'].apply(clean_last_updated)
                tmp_df['date'] = tmp_df['Last Update'].apply(get_date)
                tmp_df['file_date'] = get_csv_date(file)
                all_csv.append(tmp_df)

        # concatenate all csv's into one df
        df_raw = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)
        df_raw = df_raw.sort_values(by=['Last Update'])

        frames = cleaner.drop_duplicates(df_raw)
        tmp = pd.concat(frames, axis=0, ignore_index=True, sort=True)
        
        return tmp

    def get_clean_sheets():
        # Create Tmp Folder
        if not os.path.isdir(TMP_FOLDER):
            print('Creating folder...')
            print('...', TMP_FOLDER)
            os.mkdir(TMP_FOLDER)

        #Check if repo exists
        #git pull if it does
        if not os.path.isdir(TMP_GIT):
            cleaner.clone_repo(TMP_FOLDER, REPO)
        else:
            try:
                print('git pull from', REPO)
                rep = git.Repo(TMP_GIT)
                rep.remotes.origin.pull()
            except:
                print('Could not pull from', REPO)
                sys.exit()
            
        sheets = os.listdir(DATA)

        # Clean the result to the sheet tabs we want
        print('Getting sheets...')
        cleaned_sheets = cleaner.clean_sheet_names(sheets)

        return cleaned_sheets

    def get_similar_countries(c, country_list):
        pos_countries = get_close_matches(c, country_list)
        
        if len(pos_countries) > 0:
            print(c, 'was not listed. did you mean', pos_countries[0].capitalize() + '?')
            sys.exit()
        else:
            print(c, 'was not listed.')
            sys.exit()

    def get_new_cases(tmp, col):
        diff_list = []
        tmp_df_list = []
        df = tmp.copy()

        for i, day in enumerate(df.sort_values('date').date.unique()):    
            tmp_df = df[df.date == day]
            tmp_df_list.append(tmp_df[col].sum())
            
            if i == 0:
                diff_list.append(tmp_df[col].sum())
            else:
                diff_list.append(tmp_df[col].sum() - tmp_df_list[i-1])
            
        return diff_list

    def get_moving_average(tmp, col):
        df = tmp.copy()
        return df[col].rolling(window=2).mean()

    def get_exp_moving_average(tmp, col):
        df = tmp.copy()
        return df[col].ewm(span=2, adjust=True).mean()


class Cleaner: 
    @abstractmethod   
    def clean_sheet_names(self, new_ranges):
        pass

    @abstractmethod
    def clean_last_updates(self, last_update):
        pass

    @abstractmethod
    def drop_duplicates(self, df_raw):
        pass

    @abstractmethod
    def clone_repo(self, TMP_FOLDER, REPO):
        pass

    @abstractmethod
    def clean_data(self, tmp_df):
        pass

    @abstractmethod
    def clean_sheets(self):
        pass


class DataCleaner3(Cleaner):

    def clean_data(tmp_df):
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

    def clean_last_updated(last_update):
        '''
        convert date and time in YYYYMMDD HMS format
        '''
        date = parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
        time = parse(str(last_update).split(' ')[1]).strftime('%H:%M:%S')
        parsed_date = str(date) + ' ' + str(time)

        return parsed_date

    def clean_sheet_names(new_ranges):
        indices = []    
        # Remove all sheets that dont have a numeric header
        numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
    
        return numeric_sheets

    def drop_duplicates(df_raw):
        '''
        Take the max date value for each province for a given date
        '''
        days_list = []
        
        for datetime in df_raw.date.unique():
            tmp_df = df_raw[df_raw.date == datetime]
            tmp_df = tmp_df.sort_values(['Last Update']).drop_duplicates('Province/State', keep='last')
            days_list.append(tmp_df)

        return days_list

    def clone_repo(TMP_FOLDER, REPO):
        print('Cloning Data Repo...')
        git.Git(TMP_FOLDER).clone(REPO)

    def clean_sheets(self):
        # Create Tmp Folder
        if not os.path.isdir(TMP_FOLDER):
            print('Creating folder...')
            print('...', TMP_FOLDER)
            os.mkdir(TMP_FOLDER)

        #Check if repo exists
        #git pull if it does
        if not os.path.isdir(TMP_GIT):
            clone_repo(TMP_FOLDER, REPO)
        else:
            try:
                print('git pull from', REPO)
                rep = git.Repo(TMP_GIT)
                rep.remotes.origin.pull()
            except:
                print('Could not pull from', REPO)
                sys.exit()
            
        sheets = os.listdir(DATA)

        # Clean the result to the sheet tabs we want
        print('Cleaning sheets...')
        cleaned_sheets = clean_sheet_names(sheets)
        return cleaned_sheets


class DataCleaner4(Cleaner):

    def clean_data(tmp_df):
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

    def clean_last_updated(last_update):
        '''
        convert date and time in YYYYMMDD HMS format
        '''
        date = parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
        time = parse(str(last_update).split(' ')[1]).strftime('%H:%M:%S')
        parsed_date = str(date) + ' ' + str(time)

        return parsed_date

    def clean_sheet_names(new_ranges):
        indices = []    
        # Remove all sheets that dont have a numeric header
        numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
    
        return numeric_sheets

    def drop_duplicates(df_raw):
        '''
        Take the max date value for each province for a given date
        '''
        days_list = []
        
        for datetime in df_raw.date.unique():
            tmp_df = df_raw[df_raw.date == datetime]
            tmp_df = tmp_df.sort_values(['Last Update']).drop_duplicates('Province/State', keep='last')
            days_list.append(tmp_df)

        return days_list

    def clone_repo(TMP_FOLDER, REPO):
        print('Cloning Data Repo...')
        git.Git(TMP_FOLDER).clone(REPO)

    def clean_sheets(self):
        # Create Tmp Folder
        if not os.path.isdir(TMP_FOLDER):
            print('Creating folder...')
            print('...', TMP_FOLDER)
            os.mkdir(TMP_FOLDER)

        #Check if repo exists
        #git pull if it does
        if not os.path.isdir(TMP_GIT):
            clone_repo(TMP_FOLDER, REPO)
        else:
            try:
                print('git pull from', REPO)
                rep = git.Repo(TMP_GIT)
                rep.remotes.origin.pull()
            except:
                print('Could not pull from', REPO)
                sys.exit()
            
        sheets = os.listdir(DATA)

        # Clean the result to the sheet tabs we want
        print('Cleaning sheets...')
        cleaned_sheets = clean_sheet_names(sheets)
        return cleaned_sheets