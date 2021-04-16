from convidify.sources import github, wiki

"""
global values
"""
class DataStoreBridge():
    def jhu_sources(self):
        return github.get()

    def wiki_sources(self):
        return github.get() 