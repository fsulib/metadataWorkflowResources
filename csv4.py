#!/usr/bin/env python3

import csv
import os
import sys
import argparse
from lxml import etree
from csv4call import archon, aleph

NS = {'mods':'http://www.loc.gov/mods/v3'}

def writeCSV(name, arg):
    if arg == 'archon':
        collNum = input("Enter a collection ID number: ")
        series = input("Enter a number for the digital series: ")
        os.system('~/bin/metadataWorkflowResources/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
        archon(name, collNum, series)
    elif arg == 'aleph':    
        os.system('~/bin/metadataWorkflowResources/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
        aleph(name)
    else:
        print('Unrecognized system argument.')    

parser = argparse.ArgumentParser(description='Exports data from FSUDL & structures it into CSV files either for inclusion in Archon as a collection content import, or for transimission to cataloging for digital edition MARC records.')
parser.add_argument('-c', '--collection', required=True, 
                    help='oai setspec or collection PID to harvest')
parser.add_argument('-s', '--system', required=True, choices=['archon', 'aleph'],
                    help='target system')
args = parser.parse_args()
writeCSV(args.collection.replace(':','_'), args.system)
print('Spreadsheet created.')
