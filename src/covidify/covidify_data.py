from convidify.sources import github, wiki

"""
global values
"""
class DataStore():
    def jhu_sources(self):
        return github.get()

    def wiki_sources(self):
        return github.get()