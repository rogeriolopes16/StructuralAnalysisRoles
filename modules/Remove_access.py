from modules.ReadCSV import *
from modules.DataBase import *
from settings.db import *
from modules.Directory import *
from modules.functions import *

rd = ReadCSC()

def remove_access():
    removeFiles('output')  # remove all files *.csv from directory

    list_current_user = []
    list_access_cal = []

    for n in rd.readCSV('input_access_remove'):
        current_role = ''
        if n[3] != '':
            current_role = n[1]
            for n_in in rd.readCSV('input_access_remove'):
                if current_role == n_in[1] and n_in[2] != '':
                    list_current_user.append([n[0], n[1], n_in[2], n[3]])

    for n_cal in rd.readCSV('access_cal'):
        list_access_cal.append([n_cal[2].strip().upper()+n_cal[4].strip().upper()])


    # create file data remove
    with open(PAR_DIRECTORY_PROJ + '/output/Remove Access.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['CR', 'PAPEL', 'ACESSO REMOÇÃO', 'MEMBROS DO PAPEL'])

        for n_perfil in list_current_user:
            if ([str(n_perfil[3].strip().upper())+str(n_perfil[2].strip().upper())]) in list_access_cal:
                writer.writerow([n_perfil[0], n_perfil[1], n_perfil[2], n_perfil[3]])