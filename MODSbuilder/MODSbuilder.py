#!/usr/bin/env python3

import csv
import sys
import argparse
from lxml import etree

def buildMODS(record):
    NS = { None : 'http://www.loc.gov/mods/v3',
            'mods': 'http://www.loc.gov/mods/v3',
            'flvc' : 'info:flvc/manifest',
            'xlink' : 'http://www.w3.org/1999/xlink',
            'xsi' : 'http://www.w3.org/2001/XMLSchema-instance' }
    root = etree.Element('mods', nsmap=NS)
    extension = etree.SubElement(root, 'extension')
    flvc = etree.SubElement(extension, '{%s}flvc' % NS['flvc'])
    owningInstitution = etree.SubElement(flvc, '{%s}owningInstitution' %NS['flvc'])
    owningInstitution.text = 'FSU'
    submittingInstitution = etree.SubElement(flvc, '{%s}submittingInstitution' %NS['flvc'])
    submittingInstitution.text = 'FSU'
    print(etree.tostring(root).decode("UTF-8"))
#    for path, text in record.items():
#        print(path, text)
    
def readCSV(fileIn):
    with open(fileIn) as csvfile:
        source = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in source:
            buildMODS(row) 
      
parser = argparse.ArgumentParser(description="create Metadata Object Description Schema XML documents from CSV files")
parser.add_argument('CSV', help='CSV to be converted to MDOS')
args = parser.parse_args()
readCSV(args.CSV)      