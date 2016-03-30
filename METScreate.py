#!/usr/bin/env python3

from lxml import etree
import os
import sys
import hashlib
import datetime
import argparse

def buildMETS(directory):
    NS = { 'mets' : 'http://www.loc.gov/METS/', 'mods': 'http://www.loc.gov/mods/v3' }
    with open(directory + '/' + directory + '.xml', 'w') as outFile:
        root = etree.Element("{%s}mets" % NS['mets'], OBJID=directory)
        metsHdr = etree.SubElement(root, "{%s}metsHdr" % NS['mets'], ID=directory,
                                    RECORDSTATUS="COMPLETE", 
                                    CREATEDATE=datetime.datetime.isoformat(datetime.datetime.now()),
                                    LASTMODDATE=datetime.datetime.isoformat(datetime.datetime.now()))
        dmdSec = etree.SubElement(root, "{%s}dmdSec" % NS['mets'])
        fileSec = etree.SubElement(root, "{%s}fileSec" % NS['mets'])
        structMap = etree.SubElement(root, "{%s}structMap" % NS['mets'], 
                                    ID="STRUCT1", TYPE="physical")
        #root.set('xmlns:METS', 'http://www.loc.gov/METS/')
        print(etree.tostring(root, pretty_print=True))
        
    #get_files(directory)

def get_files(directory):
    for image in os.listdir(directory):
        print(image)
        
agent_dict = { 'ORGANIZATION' : 'FSU,Florida State University', 'OTHER' : 'METScreate.py by FSU Libraries' }
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--agent', help='FSUID of individual running this program')
parser.add_argument('directory', help='directory containing files to be used in creating the METS document') 
args = parser.parse_args()
agent_dict['INDIVIDUAL'] = args.agent
buildMETS(sys.argv[1])