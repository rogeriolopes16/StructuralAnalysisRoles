from modules.ReadCSV import *
from modules.DataBase import *
from settings.db import *
from modules.Directory import *

rd = ReadCSC()
db = GetDataBase()

resource = []
resource_result = []
entitlements = []
entitlements_ids = []
entitlements_certifiable = []
entitlements_result = []
entitlements_result_certifiable = []



def baseMapping():
    print('Processing Base Mapping PRD x HML...')
    for r in db.blazon(SELECT_RESOURCE):
        resource.append(r[0])
    for e in db.blazon(SELECT_ENTITLEMENTS_MAP):
        entitlements.append(e[1]+e[3])
        entitlements_ids.append([e[1]+e[3],e[2]])
        if e[4] == 'TRUE':
            entitlements_certifiable.append(e[1]+e[3])

    for n in rd.readCSV('reportEntitlementsBlazon'):
        if n[3].strip() in resource:
            if str(n[3].strip()+n[1].strip()) not in entitlements:
                entitlements_result.append([n[1].strip(), n[3].strip(), n[9].strip()])
        else:
            entitlements_result.append([n[1].strip(), n[3].strip(), n[9].strip()])
            if n[3].strip() not in resource_result:
                resource_result.append(n[3].strip())

        if str(n[3].strip()+n[1].strip()) in entitlements:
            if str(n[3].strip() + n[1].strip()) in entitlements_certifiable:
                if n[9].strip() == 'false':
                    entitlements_result_certifiable.append([str(n[3].strip() + n[1].strip()), 'FALSE'])
            else:
                if n[9].strip() == 'true':
                    entitlements_result_certifiable.append([str(n[3].strip() + n[1].strip()), 'TRUE'])


    # create layout new resources
    if len(resource_result) > 0:
        with open(PAR_DIRECTORY_PROJ + '/output/Layout Import Resources.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['name', 'type'])
            for r in resource_result:
                writer.writerow([r, 'REGULAR'])

    # create layout new entitlements
    if len(entitlements_result) > 0:
        with open(PAR_DIRECTORY_PROJ + '/output/Layout Import Entitlements.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['name', 'resource','certifiable'])
            for e in entitlements_result:
                writer.writerow([e[0], e[1], e[2]])

    # create layout update certifiable entitlements
    if len(entitlements_result_certifiable) > 0:
        with open(PAR_DIRECTORY_PROJ + '/output/Layout Import Entitlements certifiable.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['identifier', 'certifiable'])
            for e in entitlements_result_certifiable:
                for eid in entitlements_ids:
                    if e[0] == eid[0]:
                        writer.writerow([eid[1], e[1]])