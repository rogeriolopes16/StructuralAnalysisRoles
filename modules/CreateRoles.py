from modules.ReadCSV import *
from modules.DataBase import *
from settings.db import *
from modules.Directory import *
from modules.functions import *

rd = ReadCSC()
db = GetDataBase()


def createRoles(option,cr):
    print('Processing Create Roles...') if option == '1' else print('Processing Structural Analysis...')
    '''
    CREATE LAYOUT CREATE ROLES
    '''
    removeFiles('output')  # remove all files *.csv from directory

    # distinct of the roles from db
    roles = []
    for n in db.blazon(SELECT_ROLES):
        roles.append(n[0])
    layout_create_roles = []
    list_not_exist_cal = []
    list_update_role = []
    exist_create_roles = False
    count_roles = 0
    count_rights, count_rights_input = 0, 0

    # create layout new roles and write in the file
    with open(PAR_DIRECTORY_PROJ + '/output/Layout Criação de Papel do CR ' + cr + '.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['name', 'description', 'visibleToSelfService'])
        for n in rd.readCSV('input'):
            if n[0].strip() not in roles and n[1].strip() == 'DESCRIPTION':
                count_roles += 1
                writer.writerow([n[0].strip(), n[2].strip(), 'TRUE'])
                exist_create_roles = True
                list_update_role.append([n[0].strip(), 'CR' + cr + '; CR ' + cr])

    with open(PAR_DIRECTORY_PROJ + '/output/Layout Update de Papel do CR ' + cr + '.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['name', 'tags'])
        for n in list_update_role:
            writer.writerow([n[0].strip(), n[1].strip()])

    '''
    CREATE LAYOUT CREATE ROLES RIGHTS
    '''
    if not exist_create_roles or option == '3':
        not_exist_cal = None

        # loading informations of the db
        rolesBlazon = db.blazon(SELECT_ROLES)
        entitlementsBlazon = db.blazon(SELECT_ENTITLEMENTS)
        keyroleright = []
        for rr in db.blazon(SELECT_ROLE_RIGHT):
            keyroleright.append(rr[0])

        # create layout new role rights and write in the file
        with open(PAR_DIRECTORY_PROJ + '/output/Layout Criação de Objetos no Papel do CR ' + cr + '.csv', 'w', newline='',
                  encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['roleId', 'role', 'resource', 'resourceId', 'entitlements', 'entitlementsIds'])
            for i in sorted(rd.readCSV('input')):
                count_rights += 1
                found_cal = False
                roleId, role, resource, resourceId, entitlements, entitlementsIds = None, None, None, None, None, None
                for m in rd.readCSV('mapping'):
                    if i[1].strip() != 'DESCRIPTION':
                        if (str(i[2]).strip() in str(m[0]).strip() or str(i[2]) in str(m[0])) and verified_access_out_blazon(i[2].strip()) == False:
                            found_cal = True
                            # assign roles
                            for rol in rolesBlazon:
                                if rol[0].strip() == i[0].strip():
                                    roleId, role = rol[1], rol[0]

                            # search and assign resources and entitlements to variables
                            for ent in entitlementsBlazon:
                                if m[1].strip() == ent[1].strip() and m[2].strip() == ent[3].strip():
                                    resource, resourceId, entitlements, entitlementsIds = ent[1], ent[0], ent[3], ent[2]
                            if resource != None and resourceId != None and entitlements != None and entitlementsIds != None \
                                    and (
                                    str(roleId) + '|' + str(resourceId) + '|' + str(entitlementsIds)) not in keyroleright:
                                count_rights_input += 1
                                writer.writerow([roleId, role, resource, resourceId, entitlements, entitlementsIds])

                # objects of CAL or blazon not found
                if i[1].strip() != 'DESCRIPTION' and (found_cal == False or
                    (resource is None or resourceId is None or entitlements is None or entitlementsIds is None)):
                    not_exist_cal = i[2].strip()
                    list_not_exist_cal.append([i[0], i[2]])

        # create file with objects of CAL or blazon not found
        if option == '3':
            removeFiles('output')  # remove all files *.csv from directory
            if len(list_not_exist_cal) > 0:
                with open(PAR_DIRECTORY_PROJ + '/output/Structural Analysis CR' + cr + '.csv', 'a+', newline='', encoding='utf-8') as files:
                    writers = csv.writer(files, delimiter=',')
                    writers.writerow(['TYPE','MAIN OBJECT', 'SECONDARY OBJECT', 'RESULT'])
                    for lnot in list_not_exist_cal:
                        motive = 'Not exist in Blazon' if verified_access_out_blazon(lnot[1]) else 'Not found CAL or BLAZON'
                        if 'BANCO DE DADOS' in lnot[1]:
                            writers.writerow(['CRITICAL ACCESS', lnot[0], lnot[1], motive])
                        else:
                            writers.writerow(['ACCESS ROLES', lnot[0], lnot[1], motive])

    print(f'Total of roles: {count_roles}') if count_roles > 0 and option == '1' else None
    print(f'Total of entitlements in the file: {count_rights}') if count_rights > 0 and option == '1' else None
    print(f'Total of entitlements to input: {count_rights_input}') if count_rights_input > 0 and option == '1' else None
    print(f'Total of entitlements not found: {len(list_not_exist_cal)}') if len(list_not_exist_cal) > 0 and option == '3' else None
    print('finished!') if option == '1' else None
    return len(list_not_exist_cal)