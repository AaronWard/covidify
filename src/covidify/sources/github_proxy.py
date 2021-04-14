from data_sources_interface import DataInterface
from github import Github
import pandas

class GithubProxy(DataInterface):
'''
Proxy class for the Github class. This class should be used in place of Github
'''
    #Initialize and cache a Github instance if one is not already cached
    def __init(self):

        if not getattr(self.__class__, 'cached_object', None):
            self.__class__.cached_object = Github()

    #Returns a copyof the pandas dataframe from the Github class
    def get(self):
        df = self.__class__.cached_object.data
        return df.copy()
