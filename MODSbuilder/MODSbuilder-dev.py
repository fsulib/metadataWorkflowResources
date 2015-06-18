from lxml import etree
import csv
import sys
import os

modsNS = 'http://www.loc.gov/mods/v3'
flvcNS = 'info:flvc/manifest/v1'
NSmap = {None: modsNS, 'flvc': flvcNS}

def makeMODS(tag, text):
  elem = etree.Element(tag)
  elem.text = text
  if parent[elem.tag] is None:
    makeMODS(parent[elem.tag])
  else:
    root.append(elem)  
    
def buildRecord(record):
  root = etree.Element('mods', nsmap = NSmap)
  for tag, text in record.items():
    makeMODS(tag, text)
  xmlString = etree.tostring(root, pretty_print=True)
  f = open('output/%s.xml' % record['identifier'], 'w')
  f.write(xmlString.decode('utf-8'))
  f.close()

def readCSV(fileIn):
  with open(fileIn) as csvfile:
    source = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in source:
      buildRecord(row)  

name = sys.argv[1]
readCSV(name)