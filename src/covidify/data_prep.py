class SingletonGovt:
   __instance__ = None
   def __init__(self):
       """ Constructor.
       """
       if SingletonGovt.__instance__ is None:
          SingletonGovt.__instance__ = self
       else:
           raise Exception("You cannot create another SingletonGovt class")
    def check_specified_country(self,df, country):
    '''
    let user filter reports by country, if not found
    then give a option if the string is similar
    '''
    # Get all unique countries in the data
       country_list = list(map(lambda x:x.lower().strip(), set(df.country.values)))

       if country:
          print('Country specified!')
       if country.lower() == 'Mainland China': #Mainland china and china doesn't come up as similar
            print(country, 'was not listed. did you mean China?')
            sys.exit(1)
        # give similar option if similarity found
        if country.lower() not in country_list:
            get_similar_countries(country, country_list)
        else:
            #Return filtered dataframe
            print('... filtering data for', country)
            if len(country) == 2:
                df = df[df.country == country.upper()]
            else:
                df = df[df.country == capwords(country)]
            return df
    else:
        print('... No specific country specified')
        return df

   @staticmethod
   def get_instance():
       """ Static method to fetch the current instance.
       """
       if not SingletonGovt.__instance__:
           SingletonGovt()
       return SingletonGovt.__instance__
df = SingletonGovt.get_instance(df, country)
