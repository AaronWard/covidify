#!/usr/bin/env python3
from __future__ import print_function
import pandas as pd
import re
import os
import sys
import git
import numpy as np
from tqdm import tqdm
from time import strftime
from dateutil.parser import parse
from datetime import datetime, date, time
from covidify.config import REPO, TMP_FOLDER, TMP_GIT, DATA, KEEP_COLS, NUMERIC_COLS
from data_sources_interface import DataInterface

class Github(DataInterface):

    data_sheet = None

    def __init__(self):
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
                sys.exit(1)

        data_sheet = os.listdir(DATA)




    # use this function to fetch the data
    def get(self):

        return self.data_sheet
