from __future__ import print_function
import os
import sys
import docopt
import numpy as np
import pandas as pd
from string import capwords
from difflib import get_close_matches
from datetime import datetime, date, time 

from covidify.sources import github, wiki
from covidify.config import REPO, TMP_FOLDER, TMP_GIT, DATA
from covidify.utils.utils import replace_arg_score

#args = docopt.docopt(__doc__)
#out = args['--output_folder']
country = args['--country']
source = args['--source']
#top = int(args['--top'])

class Database:
    def get_data(source)
        if source == 'JHU':
            return github.get()
        elif source == 'wiki':
            print('Apologies, the wikipedia source is not ready yet - getting github data')
            return github.get()
            
