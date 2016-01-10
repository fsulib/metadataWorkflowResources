from lxml import etee
import csv
import os
import sys

NS = {'mods':'http://www.loc.gov/mods/v3'}

def writeCSV(filename):
    

name = os.path.splitext(sys.argv[1])[0]
writeCSV(name)
print('Spreadsheet created.')
