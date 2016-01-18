#!/usr/bin/env python3

from lxml import etree
from csv4cat import archon aleph
import csv
import os
import sys

NS = {'mods':'http://www.loc.gov/mods/v3'}

def writeCSV(filename, arg):
    if arg == 'archon':
        archon(filename)
    elif arg == 'aleph':
        aleph(filename)
    else:
        print('Unrecognized system argument.')
    

name = os.path.splitext(sys.argv[1])[0]
os.system('../pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
writeCSV(name, sys.argv[2])
print('Spreadsheet created.')
