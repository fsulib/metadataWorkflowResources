#!/usr/bin/env python3

from lxml import etree
import re
import os
import sys

def fsudl_pid_search(mods_record, nameSpace_dict):
    pid = re.compile('fsu:[0-9]*')
    for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
        match = pid.search(identifier.text)
        if match is not None:
            return match.group()

def analyse_for_locations(fileName, dir):
    NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
    tree = etree.parse(os.curdir + '/' + dir + fileName)
    root = tree.getroot()
    if root.find('.//{%s}physicalLocation' %NS['mods'] ) is not None:
        for location in root.iterfind('.//{%s}physicalLocation' %NS['mods'] ):
            if len(location.getparent().attrib) > 0:
                print(fileName + ' : ' + 
                      fsudl_pid_search(tree, NS)
                       + ' -- LOCATION IN PURL'
                      )
    elif root.find('.//{%s}physicalLocation' %NS['mods'] ) is None:
        print(fileName + ' : ' + 
              fsudl_pid_search(tree, NS)
              + ' -- NO LOCATION'
              )
            
#arg1 = directory location containing MODS files
for fileIn in os.listdir(sys.argv[1]):
    if os.path.isfile(os.curdir + '/' + sys.argv[1] + fileIn):
        analyse_for_locations(fileIn, sys.argv[1])
print('\nDone')