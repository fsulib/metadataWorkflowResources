#!/usr/bin/env python3

import sys
import os
from lxml import etree

def addNames(mods, personography):
    NS = {'mods':'http://www.loc.gov/mods/v3'}
    modsTree = etree.parse(mods)
    modsRoot = modsTree.getroot()
    personTree = etree.parse(personography)
    personRoot = personTree.getroot()
    for name in personRoot.iter('name'):
        subject = etree.Element('{%s}subject' %NS['mods'])
        subject.append(name)
        modsRoot.append(subject)
    modsTree.write(mods +'out', pretty_print=True, xml_declaration=True)

parentRecord = sys.argv[1]
personsRecord = sys.argv[2]
addNames(parentRecord, personsRecord)
