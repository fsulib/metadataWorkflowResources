from lxml import etree
import csv
import sys
import os

parents = {'mods': '', 'languageTerm': 'language', 'physicalLocation': 'location', 'namePart': 'name', 'role': 'name', 'roleTerm': 'role', 'dateCreated': 'originInfo', 'dateIssued': 'originInfo', 'issuance': 'originInfo', 'place': 'originInfo', 'placeTerm': 'place', 'publisher': 'originInfo', 'digitalOrigin': 'physicalDescription', 'extent': 'physicalDescription', 'form': 'physicalDescription', 'descriptionStandard': 'recordInfo', 'recordCreationDate': 'recordInfo', 'recordOrigin': 'recordInfo', 'nonSort': 'titleInfo', 'title': 'titleInfo', 'subTitle': 'titleInfo', 'abstract': 'mods', 'accessCondition': 'mods', 'extension': 'mods', 'genre': 'mods', 'identifier': 'mods', 'language': 'mods', 'location': 'mods', 'name': 'mods', 'note': 'mods', 'originInfo': 'mods', 'physicalDescription': 'mods', 'recordInfo': 'mods', 'titleInfo': 'mods', 'typeOfResource': 'mods'}
modsNS = 'http://www.loc.gov/mods/v3'
flvcNS = 'info:flvc/manifest/v1'
NSmap = {None: modsNS, 'flvc': flvcNS}

def makeMODS(tag, text = None, mods = None):
  elem = etree.Element(tag)
  if text:
    elem.text = text
  if parents[elem.tag] is None:
    host = makeMODS(parents[elem.tag])
    host.append(elem)
  else:
    mods.append(elem)  
    
def buildRecord(record):
  mods = etree.Element('mods', nsmap = NSmap)
  for tag, text in record.items():
    makeMODS(tag, text, mods)
  xmlString = etree.tostring(mods, pretty_print=True)
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