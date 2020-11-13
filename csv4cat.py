#!/usr/bin/env python3

import os
import sys
import csv
import argparse
import pymods

# sys.path.append('metadataWorkflowResources/assets/')

# from pymods import MODS, FSUDL

def aleph(fileName):
    header = ['PURL', 'PID', 'Title', 'Creators', 'Date', 'Extent', 'Abstract', 'Notes', 'Comments/Shares']
    with open(fileName + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        mods = pymods.OAIReader(fileName + '.xml')
        for record in mods:
            data = []
            #PURL
            data.append(record.metadata.purl[0])
            #PID
            data.append(record.metadata.pid)
            #title
            title = ""
            for t in record.metadata.titles:
                title = title + '; ' + t
            data.append(title.strip(' ;'))
            #names
            names = ""
            for n in record.metadata.get_creators:
                names = names + '; ' + n.text
            data.append(names.strip(' ;'))
            #date
            dates = ""
            for d in record.metadata.dates:
                dates = dates + '; ' + d.text
            data.append(dates.strip(' ;'))
            #extent
            extent = ""
            for e in record.metadata.extent:
                dates = dates + '; ' + e            
            data.append(extent.strip(' ;'))
            #abstract
            abstracts = ""
            for abstract in record.metadata.abstract:
                abstracts = abstracts + '; ' + abstract.text            
            data.append(abstracts.strip(' ;'))
            #notes
            notes = ""
            for note in record.metadata.note:
                notes = notes + '; ' + note            
            data.append(notes.strip(' ;'))
            #write CSV
            writer.writerow(data)


def archon(fileName, collNum, series):
    with open(fileName + '.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        data = [collNum, str(series), "", "", "", "", 'Materials available online', "", "Digital Collections hosted by FSU Libraries Special Collections & Archives."]
        writer.writerow(data)
        itemNumber = 1
        mods = pymods.OAIReader(fileName + '.xml')
        # fields to pull: collection ID, Series #, Subseries #, Box #, Folder #, Item #, Title, Date, Description (i.e. PURL)
        for record in mods:
            data = [collNum, str(series), "", "", "", str(itemNumber)]
            #title
            data.append(record.metadata.titles[0])
            #date
            data.append(record.metadata.dates[0].text)
            #PURL
            data.append('[url]%s[/url]' % record.metadata.purl[0])
            #write to CSV & increase item# index
            writer.writerow(data)
            itemNumber = itemNumber + 1

def archon_local(dirName, collNum, series):
    with open('archonOutput.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        data = [collNum, str(series), "", "", "", "", 'Materials available online', "", "Digital Collections hosted by FSU Libraries Special Collections & Archives."]
        writer.writerow(data)
        itemNumber = 1
        for file in os.listdir(dirName):
            mods = MODS(dirName + file)
            for record in mods.record_list:
                # fields to pull: collection ID, Series #, Subseries #, Box #, Folder #, Item #, Title, Date, Description (i.e. PURL)
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

def writeCSV(name, system, local):    
    if system == 'archon':
        collNum = input("Enter a collection ID number: ")
        series = input("Enter a number for the digital series: ")
        if local == False:    
            os.system('~/bin/metadataWorkflowResources/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
            archon(name, collNum, series)
        elif local == True:
            archon_local(name, collNum, series)
    elif system == 'aleph':    
        os.system('~/bin/metadataWorkflowResources/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
        aleph(name)
    else:
        print('Unrecognized system argument.')    

        
parser = argparse.ArgumentParser(description='Exports data from FSUDL & structures it into CSV files either for inclusion in Archon as a collection content import, or for transimission to cataloging for digital edition MARC records.')
parser.add_argument('-c', '--collection', required=True, 
                    help='oai setspec or collection PID or local directory')
parser.add_argument('-s', '--system', required=True, choices=['archon', 'aleph'],
                    help='target system')
parser.add_argument('--local-directory', type=bool, default=False, help='use local directory as input instead of OAI')  
args = parser.parse_args()
writeCSV(args.collection.replace(':','_'), args.system, args.local_directory)
print('Spreadsheet created.')
