'''
Aggregate root class for wiki and github scripts

'''
class data_sources:
    import github
    import wiki
    import pandas as pd

    def __init__(self):
        pass

    #Grab data from github repo
    #Returns pandas dataframe
    def get_github_data(self):
            return github.get()

    #Grab data from wiki when implemented
    def get_wiki_data(self):
        pass
