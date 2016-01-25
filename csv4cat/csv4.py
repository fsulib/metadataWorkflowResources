#!/usr/bin/env python3

from lxml import etree
from csv4call import archon, aleph
import csv
import os
import sys

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

name = os.path.splitext(sys.argv[1])[0]
writeCSV(name, sys.argv[2])
print('Spreadsheet created.')
