#!/usr/bin/env python3

import os
import sys
import glob
import shutil
import argparse
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
    shutil.move(mods, '.backup/')
    shutil.move(mods +'out', mods)

#arg1 = file to edit; arg2 = xml fragment to add to root
parser = argparse.ArgumentParser(description="Appends the children of root from any well-formed XML fragment to the root of a MODS file.")
parser.add_argument('-f', '--fragment', required=True,
                    help='XML fragment to add to a MODS file')
parser.add_argument('-m', '--mods_file', required=True,
                    help='target MODS file')
args = parser.parse_args()

# create recovery directory
if '.backup' not in os.listdir():
    os.mkdir('.backup')
addFragment(args.mods_file.replace('*',''), args.fragment)