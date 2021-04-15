
#use this as our aggregate root for wiki and github which have their own files in /sources
class agg_data:
    import wiki
    import github    
    import pandas as pd 
    #Pandas is an open source Python package that is most widely used for data science/data analysis and machine learning tasks
    #so including it here will also help with aggregate pattern as its used in many of the python code in this project.

        
    def github_data(self):
            return github.getData()


    def wiki_data(self):
            return wiki.getData()
    #wiki.py isempty no code.
    