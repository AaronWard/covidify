import wiki
import github
import pandas as pd

def get_github_data():
    return github.get()
def get_wiki_data():
    return wiki.get()