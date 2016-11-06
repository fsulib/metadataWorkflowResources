#!/usr/bin/env python3
import csv
import requests
import datetime
from io import StringIO
from lxml import etree


def csv_output(data):
    with open('edgeTable{0}.csv'.format(datetime.date.today()), 'w') as output:
        edge_table = csv.DictWriter(output, fieldnames=['source', 'target'])
        edge_table.writeheader()
        for line in data:
            edge_table.writerow(line)

# namespaces
rdf = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
fedora = '{info:fedora/fedora-system:def/relations-external#}'

# get a list of setSpecs
set_spec_list = []
with open('assets/setSpec.txt') as set_spec_file:
    for line in set_spec_file:
        for set_spec in line.split(' '):
            if set_spec != ')':
                set_spec_list.append(set_spec.replace('setList=(',''))

collection_list = []
for collection in set_spec_list:
    print(collection)
    if 'fsu_fsu_' in collection:
        collection = 'fsu:' + collection[4:]
    else:
        collection = collection.replace('fsu_', 'fsu:')
    collection_relationship = {'source' : collection}
    rels_ext_request = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/RELS-EXT/view'.format(collection))
    rels_ext_tree = etree.parse(StringIO(rels_ext_request.text))
    rels_ext_root = rels_ext_tree.getroot()
    for parent_collection in rels_ext_root.iterfind('.//{0}isMemberOfCollection'.format(fedora)):
        collection_relationship['target'] = parent_collection.attrib.values()[0][12:]
    collection_list.append(collection_relationship)

csv_output(collection_list)        
