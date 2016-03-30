#!/usr/bin/env python3

from lxml import etree
import os
import sys
import hashlib
import datetime
import argparse

def buildMETS(directory, agent_dict):
    NS = { 'mets' : 'http://www.loc.gov/METS/', 'mods': 'http://www.loc.gov/mods/v3' }
    with open(directory + '/' + directory + '.xml', 'w') as outFile:
        root = etree.Element("{%s}mets" % NS['mets'], OBJID=directory)
        metsHdr = etree.SubElement(root, "{%s}metsHdr" % NS['mets'], ID=directory,
                                    RECORDSTATUS="COMPLETE", 
                                    CREATEDATE=datetime.datetime.isoformat(datetime.datetime.now()),
                                    LASTMODDATE=datetime.datetime.isoformat(datetime.datetime.now()))
        for type, individual in agent_dict.items():
            agent = etree.SubElement(metsHdr, "{%s}agent" % NS['mets'], ROLE="CREATOR",
                                        TYPE=type)
            if agent['TYPE'] == 'OTHER':
                agent['OTHERTYPE'] = "SOFTWARE"
            name = etree.Element("{%s}name" % NS['mets'])
            name.text = individual
            agent.append(name)
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
parser.add_argument('directory', help='directory containing files to be used in creating the METS document') 
parser.add_argument('-a', '--agent', help='FSUID of the individual running this program')
args = parser.parse_args()
agent_dict['INDIVIDUAL'] = "FSU/" + args.agent
buildMETS(args.directory, agent_dict)