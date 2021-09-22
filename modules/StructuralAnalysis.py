from modules.ReadCSV import *
from modules.DataBase import *
from settings.db import *
from modules.Directory import *
from modules.CreateRoles import *

rd = ReadCSC()
db = GetDataBase()

def structuralAnalysis(option, cr):
    returnAS = createRoles(option, cr)
    list_certifiable = []
    list_owner = []
    role_current = ''
    total = 0
    list_csv_basic_access = sorted(rd.readCSV('basic_access'))
    list_basic_access = []

    # check about access Certifiable and Critical in Role
    for i in sorted(rd.readCSV('input')):
        for n in rd.readCSV('reportEntitlementsBlazon'):
            if i[2].strip() == n[1].strip() and n[9].strip() == 'true':
                list_certifiable.append(['CERTIFIABLE ROLE', i[0], i[2], 'CERTIFIABLE'])
                list_certifiable.append(['CRITICAL ROLE', i[0], i[2], 'CRITICAL'])

        if i[0].strip() != role_current and i[1].strip() != 'DESCRIPTION':
            role_current = i[0].strip()
            list_owner.append([i[1].strip(),0,0]) if list_owner == [] else None
            for lw in list_owner:
                if lw[0].strip() == i[1].strip():
                    lw[1] += 1
                    total += 1
                    break
                else:
                    list_owner.append([i[1].strip(),1,0])
                    total += 1
                    break

        # check basic access
        for b in list_csv_basic_access:
            if i[2].strip() == b[0].strip():
                list_basic_access.append([i[0].strip(), b[0].strip()])


    # check approvals of the owners Role
    list_owner_blazon = []

    for n in db.blazon(SELECT_OWNER):
        list_owner_blazon.append([n[0], n[1]])

    for lown in list_owner:
        search_owner = True
        list_owner_blazon_result = []
        list_owner_blazon_result.append([lown[0],'N'])
        while search_owner:
            for owblresult in list_owner_blazon_result:
                if owblresult[1] == 'N':
                    for owbldb in list_owner_blazon:
                        if owblresult[0] == owbldb[1]:
                            list_owner_blazon_result.append([owbldb[0], 'N'])
                    owblresult[1] = 'S'

            for owblresult in list_owner_blazon_result:
                if owblresult[1] == 'N':
                    search_owner = True
                else:
                    search_owner = False
        lown[2] = (len(list_owner_blazon_result)-1)


    # create file with objects of CAL or blazon not found
    with open(PAR_DIRECTORY_PROJ + '/output/Structural Analysis CR' + cr + '.csv', 'a+', newline='', encoding='utf-8') as files:
        writers = csv.writer(files, delimiter=',')
        writers.writerow(['TYPE','MAIN OBJECT', 'SECONDARY OBJECT', 'RESULT']) if returnAS == 0 else None
        for listSA in list_certifiable:
            writers.writerow([listSA[0], listSA[1], listSA[2], listSA[3]])

        for lw in list_owner:
            writers.writerow(['OWNER ROLE', lw[0], lw[1], str(round((lw[1]/total)*100))+'%'])
            writers.writerow(['OWNER APPROVAL', lw[0], 'Number of Members', lw[2]])

        for lba in list_basic_access:
            writers.writerow(['BASIC ACCESS', lba[0], lba[1], ''])


    print(f'Total of Certifiable: {len(list_certifiable)}')
    print(f'Total of Criticals: {len(list_certifiable)}')
    print(f'Total of Owners: {len(list_owner)}')
    print(f'Total of Basic Access: {len(list_basic_access)}')
    print('finished!')