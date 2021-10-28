from modules.Directory import *


def beginProgram():
    removeFiles('output')  # remove all files *.csv from directory
    print('*** Processes of this program ***')
    print('1 - Create Roles')
    print('2 - Base Mapping PRD x HML')
    print('3 - Structural Analysis')
    print('4 - Removing Access')
