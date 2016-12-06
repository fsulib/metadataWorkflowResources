#!/usr/bin/env python3

import os
import sys
import csv
import argparse

sys.path.append('metadataWorkflowResources/assets/')

from pymods import MODS, FSUDL

def aleph(fileName):
    header = ['PURL', 'PID', 'Title', 'Creators', 'Date', 'Extent', 'Abstract', 'Notes', 'Comments/Shares']
    with open(fileName + '.csv', 'w') as f:
        mods = MODS(fileName)
        for record in mods.record_list:
            data = []
            #PURL
            data.append(FSUDL.purl_search(record))
            #PID
            data.append(FSUDL.pid_search(record))
            #title
            data.append(MODS.title_constructor(record))
            #names
            data.append(MODS.name_constructor(record, NS))
            #date
            data.append(MODS.date_constructor(record))
            #extent    
            data.append(MODS.extent(record)
            #abstract
            data.append(MODS.abstract(record))
            #notes
            data.append(MODS.note(record))
            #write CSV
            writer.writerow(data)

def archon(fileName, collNum, series):
    with open(fileName + '.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        data = [collNum, str(series), "", "", "", "", 'Materials available online', "", "Digital Collections hosted by FSU Libraries Special Collections & Archives."]
        writer.writerow(data)
        itemNumber = 1
        # fields to pull: collection ID, Series #, Subseries #, Box #, Folder #, Item #, Title, Date, Description (i.e. PURL)
        for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
            data = [collNum, str(series), "", "", "", str(itemNumber)]
            #title
            data.append(MODS.title_constructor(record))
            #date
            data.append(MODS.date_constructor(record))
            #PURL
            data.append('[url]%s[/url]' % FSUDL.purl_search(record))
            #write to CSV & increase item# index
            writer.writerow(data)
            itemNumber = itemNumber + 1

def archon_local():
    pass

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
