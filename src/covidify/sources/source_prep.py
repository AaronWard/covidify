import github
import wiki

class dataSources:

    def __init__(self):
        pass

    #fetch data from github repositotory
    #Returns pandas dataframe
    def get_github_data(self):
            return github.get()

    #fetch data from wiki when implemented
    def get_wiki_data(self):
        print('Apologies, the wikipedia source is not ready yet - getting github data')
        self.get_github_data()
