#!/usr/bin/env python3

import os
import csv
import sys
import argparse
import datetime
from lxml import etree

def buildMODS(record):
    with open('MODStemp/' + record['IID'] + '.xml', 'w') as modsOut:
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
        recordInfo = etree.SubElement(root, 'recordInfo')
        recordCreationDate = etree.SubElement(recordInfo, 'recordCreationDate')
        recordCreationDate.text = record['Record creation date']
        descriptionStandard = etree.SubElement(recordInfo, 'descriptionStandard')
        descriptionStandard.text = record['Description Standard']
        recordOrigin = etree.SubElement(recordInfo, 'recordOrigin')
        recordOrigin.text = 'Exported from CSV by MODSbuilder.py from FSU Libraries by ' + os.getlogin() + ' on ' + datetime.datetime.isoformat(datetime.datetime.now())
        modsOut.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode("UTF-8"))
        '''
        What will be difficult

        Various titles @alt, @uniform

        subject loops
            split by || append text nodes & attributes

        '''
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
