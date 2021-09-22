import os
import time

from modules.BeginProgram import *
from modules.CreateRoles import *
from modules.BaseMapping import *
from modules.StructuralAnalysis import *

if __name__ == '__main__':
    try:
        beginProgram()
        select = input('Select option: ')

        if select == '1':
            cr = input('Informe o CR deste processo: ')
            time_begin = time.time()
            createRoles('1', cr)
            time_end = time.time()
        elif select == '2':
            time_begin = time.time()
            baseMapping()
            time_end = time.time()
        elif select == '3':
            cr = input('Informe o CR deste processo: ')
            time_begin = time.time()
            structuralAnalysis('3', cr)
            time_end = time.time()

        print(f'Time execution: {round(time_end-time_begin)} seconds.')
    except Exception as inst:
        print('********  Finished with exception!  ********')
        print(inst)