#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import os.path
import argparse

NS = {'mods' : 'http://www.loc.gov/mods/v3'}

def pullMODS(filename):
    tree = ET.parse(filename +'.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods']):
        for subject in record.iterfind('.//{%s}subject' % NS['mods']):
            for child in subject:
                print(child.text)
                
def pullOAI(filename):
    print("oai_dc selected")
    
def pullDC(filename):
    print("dc selected")    

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="input file")
parser.add_argument("-m", "--metadataPrefix", help="select metadata encoding of source file (oai_dc, dc, or mods)")
args = parser.parse_args()
fileName = args.file.split(".")[0]
if args.metadataPrefix == "mods":
    pullMODS(fileName)
elif args.metadataPrefix == "oai_dc":
    pullOAI(fileName)
elif args.metadataPrefix == "dc":
    pullDC(fileName)
else:
    print("Invalid metadata prefix selected.")