#!/usr/bin/env python3

import sys
import os
from lxml import etree

def addFragment(mods, fragment):
    NS = {'mods':'http://www.loc.gov/mods/v3'}
    modsTree = etree.parse(mods)
    modsRoot = modsTree.getroot()
    fragmentTree = etree.parse(fragment)
    fragmentRoot = fragmentTree.getroot()
    for node in fragmentRoot.xpath('child::*'):
        modsRoot.append(node)
    modsTree.write(mods +'out', pretty_print=True, xml_declaration=True, encoding='UTF-8')

#arg1 = file to edit; arg2 = xml fragment to add to root
addFragment(sys.argv[1].replace('*',''), sys.argv[2])