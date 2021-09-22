'''import os
import glob
from settings.parameters import *

def removeFiles(directory):
    py_files = glob.glob(PAR_DIRECTORY_PROJ+'/'+directory+'/*.csv')

    for py_file in py_files:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")'''

import shutil
from settings.parameters import *

def removeFiles(directory):
    try:
        shutil.rmtree(PAR_DIRECTORY_PROJ + '/' + directory)
        os.mkdir(PAR_DIRECTORY_PROJ + '/' + directory)
    except OSError as e:
        print(e)
