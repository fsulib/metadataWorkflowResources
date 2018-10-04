import xml.etree.ElementTree as ET
import sys
import os
import re

newLine = re.compile(r"^\n\s+")
NS = {'mods': 'http://www.loc.gov/mods/v3'}

def pull(filename):
    tree = ET.parse(filename + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods']):
        for name in record.iterfind('.//{%s}name' % NS['mods']):
            with open(filename + 'Name.txt', 'w') as f:
                fullName = []
                for child in name:
                    if child.text is not None:
                        fullName.append(child.text)
                for item in fullName:
                    match = newLine.match(item)
                    if match:
                        fullName.remove(match.string)
                fullName.sort()    
                print(fullName)

fileName = os.path.splitext(sys.argv[1])[0]
pull(fileName)
