"""
OSError handler
"""

import os

class DIRManager():
    def __init__(self, file_path ):
        self.file_path = file_path

    def create_folder(self, custom_error = ''):
        try:
            os.mkdir(self.file_path)
        except OSError as ex:
            print('=================================================================================\n')
            if custom_error != '':
                print( custom_error )
            else:
                print( 'FAILED TO CREATE DIR, PLEASE MAKESURE SCRIPT HAS PERMISSION TO CREATE FOLDERS OR FAILED TO '
                       'CREATE\n' )
            print('=================================================================================\n')
            print( ex.errno )
