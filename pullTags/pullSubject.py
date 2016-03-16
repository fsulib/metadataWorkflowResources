#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import os.path
import argparse

NS = {'mods' : 'http://www.loc.gov/mods/v3', 'oai_dc' : 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc' : 'http://purl.org/dc/elements/1.1/'}

def pullMODS(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods']):
        for subject in record.iterfind('.//{%s}subject' % NS['mods']):
            for child in subject:
                print(child.text)
                
def pullOAI(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for record in root.iterfind('.//{%s}dc' % NS['oai_dc']):
        for subject in record.iterfind('.//{%s}subject' % NS['dc']):
            print(subject.text)
    
def pullDC(filename):
    print("dc selected, but not fully supported at the moment")    

parser = argparse.ArgumentParser()
parser.add_argument("file", help="input file")
parser.add_argument("-m", "--metadataPrefix", help="select metadata encoding of source file", 
                        choices=["mods", "dc", "oai_dc"], default="mods")
args = parser.parse_args()
fileName = args.file
if args.metadataPrefix == "mods":
    pullMODS(fileName)
elif args.metadataPrefix == "oai_dc":
    pullOAI(fileName)
elif args.metadataPrefix == "dc":
    pullDC(fileName)