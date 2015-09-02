from lxml import etree
import csv
import sys
import os

parents = {'mods': '', 'languageTerm': 'language', 'physicalLocation': 'location', 'namePart': 'name', 'role': 'name', 'roleTerm': 'role', 'dateCreated': 'originInfo', 'dateIssued': 'originInfo', 'issuance': 'originInfo', 'place': 'originInfo', 'placeTerm': 'place', 'publisher': 'originInfo', 'digitalOrigin': 'physicalDescription', 'extent': 'physicalDescription', 'form': 'physicalDescription', 'descriptionStandard': 'recordInfo', 'recordCreationDate': 'recordInfo', 'recordOrigin': 'recordInfo', 'nonSort': 'titleInfo', 'title': 'titleInfo', 'subTitle': 'titleInfo', 'abstract': 'mods', 'accessCondition': 'mods', 'extension': 'mods', 'genre': 'mods', 'identifier': 'mods', 'language': 'mods', 'location': 'mods', 'name': 'mods', 'note': 'mods', 'originInfo': 'mods', 'physicalDescription': 'mods', 'recordInfo': 'mods', 'titleInfo': 'mods', 'typeOfResource': 'mods'}
modsNS = 'http://www.loc.gov/mods/v3'
flvcNS = 'info:flvc/manifest/v1'
NSmap = {None: modsNS, 'flvc': flvcNS}

def makeMODS(tag, mods, text = None):
  tag = tag.split('/')
  if tag[0] == 'identifier' & etree.iselement(identifier) is False:
    identifier = etree.SubElement(mods, tag[0])
    identifier.text = text
  elif tag[1] == 'descriptionStandard' & etree.iselement(recordInfo) is False:
    recordInfo = etree.SubElement(mods, 'recordInfo')
    descriptionStandard = etree.SubElement(recordInfo, 'descriptionStandard')
    descriptionStandard.text = text
  elif tag[1] == 'descriptionStandard' & etree.iselement(recordInfo) is True:
    descriptionStandard = etree.SubElement(recordInfo, 'descriptionStandard')
    descriptionStandard.text = text
  elif tag[1] == 'recordCreationDate' & etree.iselement(recordInfo) is False:
    recordInfo = etree.SubElement(mods, 'recordInfo')
    recordCreationDate = etree.SubElement(mods, 'recordCreationDate')
    recordCreationDate.text = text
  elif tag[1] == 'recordCreationDare' & etree.iselement(recordInfo) is True:
    recordCreationDate = etree.SubElement(mods, 'recordCreationDate')
    recordCreationDate.text = text
#  if tag == 'identifier':
#    identifier.text = text
#  elif tag == 'descriptionStandard':
#    descriptionStandard = etree.SubElement(recordInfo, 'descriptionStandard')
#    descriptionStandard.text = text
#  elif tag == 'recordCreationDate':
#    recordCreationDate = etree.SubElement(recordInfo, 'recordCreationDate')
#    recordCreationDate.text = text
# brute force record construction
#    if tag == 'identifier':
#      identifier = etree.Element(tag)
#      identifier.text = text
#      mods.append(identifier)
#
# recursive construction as subelements    
#  if parents[tag] is None:
#    makeMODS(parents[tag], mods)
#  elem = etree.SubElement(parents[tag], tag)
#  if text:
#    elem.text = text
#
# recursive construction as appended elements
#  elem = etree.Element(tag)
#  host = parents[elem.tag]
#  if text:
#    elem.text = text
#  if etree.iselement(host) is True:
#    
#  else:
#    mods.append(elem)
    
def buildRecord(record):
  mods = etree.Element('mods', nsmap = NSmap)
  for tag, text in record.items():
    makeMODS(tag, mods, text)
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