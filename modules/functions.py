from modules.ReadCSV import *
from modules.DataBase import *
from settings.db import *
from modules.Directory import *

rd = ReadCSC()


def verified_access_out_blazon(access):
    status = False
    for n in rd.readCSV('access_out_blazon'):
        if n[0] in access:
            status = True
    return status
