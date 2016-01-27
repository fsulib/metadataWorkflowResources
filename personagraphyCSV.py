#!/usr/bin/env python3

import csv
from lxml import etree
import os
import sys

name = os.path.splitext(sys.argv[1])[0]
personsCSV = open(name +'.csv', newline='')
persons =  csv.DictReader(personsCSV)
root = etree.Element('names')
for line in persons:
	person = etree.Element('name', type='personal', authority='lcnaf', authorityURI='http://id.loc.gov/authorities/names', valueURI=line['valueURI'])
	for key in line.keys():
		if key != 'valueURI':
			namePart = etree.Element('namePart', type=key)
			namePart.text = line[key]
			person.append(namePart)
	root.append(person)
tree = root.getroottree()
tree.write(name +'.xml', pretty_print=True, xml_declaration=True)