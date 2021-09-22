import csv
from settings.parameters import *

class ReadCSC():
    def __init__(self):
        pass

    def readCSV(self, directory):
        direct = PAR_DIRECTORY_PROJ + '/' + directory
        file = ' '.join(map(str, os.listdir(direct)))
        self.reader = open(str(direct)+'/'+str(file), 'r')
        next(self.reader)
        self.reader = csv.reader(self.reader, delimiter=',')
        return self.reader