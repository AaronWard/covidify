class File_Date:
    def __init__(self, file_dates):
        self.file_dates = file_dates

    def get_file_date(self):
        return self.__recovered

class Recovered:
    def __init__(self, recovered):
        self.__recovered = recovered

    def get_recovered(self):
        return self.__recovered

class Deaths:
    def __init__(self, deaths):
        self.__deaths = deaths

    def get_deaths(self):
        return self.__deaths

class Confirmed:
    def __init__(self, confirmed):
        self.__confirmed = confirmed

    def get_confirmed(self):
        return self.__confirmed

class Country:
    def __init__(self, name, df):
        for day in enumerate(df.sort_values('file_date').file_date.unique()):
            tmp_df = df[df.file_date == day]

        self.__name = name
        self.__recovered = Recovered(tmp_df['recovered'])
        self.__confirmed = Confirmed(tmp_df['confirmed'])
        self.__deaths = Deaths(tmp_df['deaths'])

    def get_name(self):
        return self.__name

    def get_new_recoveries(self):
        Col = self.__recovered
        diff_list = []
        for i in range(len(Col)):
            if Col[i] == 0:
                diff_list.append[0]
            else:
                try:
                    diff_list.append[Col[i] - Col[i-1]]
                except IndexError:
                    diff_list.append[Col[i]]

        return diff_list

    def get_new_deaths(self):
        Col = self.__deaths
        diff_list = []
        for i in range(len(Col)):
            if Col[i] == 0:
                diff_list.append[0]
            else:
                try:
                    diff_list.append[Col[i] - Col[i-1]]
                except IndexError:
                    diff_list.append[Col[i]]

        return diff_list

    def get_new_rconfirms(self):
        Col = self.__confirmed
        diff_list = []
        for i in range(len(Col)):
            if Col[i] == 0:
                diff_list.append[0]
            else:
                try:
                    diff_list.append[Col[i] - Col[i-1]]
                except IndexError:
                    diff_list.append[Col[i]]

        return diff_list

    def get_confirmed_sum(self):
        return sum(self.__confirmed)

    def get_recovered_sum(self):
        return sum(self.__recovered)

    def get_deaths_sum(self):
        return sum(self.__deaths)