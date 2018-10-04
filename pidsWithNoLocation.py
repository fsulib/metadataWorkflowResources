#!/usr/bin/env python3

import re
import os
import sys
import argparse
from lxml import etree


def fsudl_pid_search(mods_record, nameSpace_dict):
    pid = re.compile('fsu:[0-9]*')
    for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
        match = pid.search(identifier.text)
        if match is not None:
            return match.group()
            

def harvest(name):
    os.system('~/bin/metadataWorkflowResources/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
    analyse_for_locations(name)


def analyse_for_locations(fileName):
    NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
    tree = etree.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
        if record.find('.//{%s}physicalLocation' % NS['mods'] ) is None:
            print(fsudl_pid_search(record, NS))

            
#arg1 = OAI setSpec or Islandora collection PID
parser = argparse.ArgumentParser(description="Can't think...")
parser.add_argument('collection', help='collection oai_setspec or Islandora PID')
args = parser.parse_args()
harvest(args.collection.replace(':', '_'))
print('\nDone')
