from lxml import etree
import csv
import sys
import os

modsNS = 'http://www.loc.gov/mods/v3'
flvcNS = 'info:flvc/manifest/v1'
NSmap = {None: modsNS, 'flvc': flvcNS}
identifier = etree.Element('identifier')
recordInfo = etree.Element('recordInfo')

class mods(etree.ElementBase):
  pass

class identifier(etree.ElementBase):
  parent = mods

class recordInfo(etree.ElementBase):
  parent = mods

class descriptionStandard(etree.ElementBase):
  parent = recordInfo
  
class recordCreationDate(etree.ElementBase):
  parent = recordInfo


def makeMODS(tag, mods, text = None):
  elem = etree.Element(tag)
  if text:
    elem.text = text
#  parents = {identifier: mods, recordInfo: mods, descriptionStandard: recordInfo, recordCreationDate: recordInfo}
#  parents[elem].append(elem)
#  return elem
#  print(elem.tag)

def buildRecord(record):
  mods = etree.Element('mods', nsmap = NSmap)
  for tag, text in record.items():
    makeMODS(tag, mods, text)
  parents = {identifier: mods, recordInfo: mods, descriptionStandard: recordInfo, recordCreationDate: recordInfo}
  for tag, parent in parents.items():
    if etree.iselement(tag) is False:
      tag = etree.Element(tag)
    parent.append(tag)
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