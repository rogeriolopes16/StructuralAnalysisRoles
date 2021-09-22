import mysql.connector
from settings.credentials import *
from settings.parameters import *
from settings.db import *

# --------------------------- Abrindo conexão com MYSql Blazon ---------------------------
db = mysql.connector.connect(user=CRD_USER_DB_BLAZON, passwd=CRD_PWD_DB_BLAZON, host=PAR_BLAZON_IP,
                             db=PAR_BLAZON_DB_NAME, port=PAR_BLAZON_PORT)
cursor_blazon = db.cursor()

class GetDataBase():
    def __init__(self):
        pass

    def blazon(self, select):
        cursor_blazon.execute(select)
        return cursor_blazon.fetchall()