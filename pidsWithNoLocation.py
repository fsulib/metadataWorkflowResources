#!/usr/bin/env python3

from lxml import etree
import re
import os
import sys

def fsudl_pid_search(mods_record, nameSpace_dict):
    pid = re.compile('fsu:[0-9]*')
    for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
        match = pid.search(identifier.text)
        if match:
            return match.group()
            
def harvest(name):
    os.system('~/bin/metadataWorkflowResources/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
    analyse_for_locations(name)

def analyse_for_locations(fileName):
    NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
    tree = etree.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
        if record.find('.//{%s}physicalLocation' %NS['mods'] ):
            return
        else:
            print(fsudl_pid_search(record, NS))
            
harvest(sys.argv[1].replace(':', '_'))    