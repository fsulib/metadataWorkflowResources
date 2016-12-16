#!/usr/bin/env python3

import os
import sys
from lxml import etree

NS = { 'mods':'http://www.loc.gov/mods/v3' }
#files = os.listdir('MODS/')
for xml in os.listdir(sys.argv[1]):
    print(xml)
    tree = etree.parse(sys.argv[1]+ xml)
    root = tree.getroot()
    for element in root.iter("{%s}identifier" %NS['mods']):
        if element.get('type') is not None:
            if element.get('type') == 'fedora':
                ID = element.text
                tree.write(sys.argv[1] + ID.replace(':', '_') +'.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')
