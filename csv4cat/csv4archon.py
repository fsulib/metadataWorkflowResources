#!/usr/bin/env python3

from lxml import etee
import csv
import os
import sys

NS = {'mods':'http://www.loc.gov/mods/v3'}

def writeCSV(filename, arg):
    if arg == 'archon':

    elif arg == 'aleph':

    else:
        print('Unrecognized system argument.')
    

name = os.path.splitext(sys.argv[1])[0]
arg = sys.argv[2]
os.sys('python2 ~/bin/pyoaiharvester/pyoaiharvester.py -l http://fsu.digital.flvc.org/oai2 -s {0} -o {1} -m mods'.format(name, name +'.xml'))
writeCSV(name, arg)
print('Spreadsheet created.')
