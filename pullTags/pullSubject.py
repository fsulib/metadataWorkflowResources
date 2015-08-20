import xml.etree.ElementTree as ET
import sys
import os.path

NS = {'mods' : 'http://www.loc.gov/mods/v3'}

def pull(filename):
    tree = ET.parse(filename +'.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods']):
        for subject in record.iterfind('.//{%s}subject' % NS['mods']):
            for child in subject:
                print(child.text)

fileName = os.path.splitext(sys.argv[1])[0]
pull(fileName)
