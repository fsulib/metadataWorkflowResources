from lxml import etree
import csv
import sys

parents = {'languageTerm': 'language', 'physicalLocation': 'location', 'namePart': 'name', 'role': 'name', 'roleTerm': 'role', 'dateCreated': 'originInfo', 'dateIssued': 'originInfo', 'issuance': 'originInfo', 'place': 'originInfo', 'placeTerm': 'place', 'publisher': 'originInfo', 'digitalOrigin': 'physicalDescription', 'extent': 'physicalDescription', 'form': 'physicalDescription', 'descriptionStandard': 'recordInfo', 'recordCreationDate': 'recordInfo', 'recordOrigin': 'recordInfo', 'nonSort': 'titleInfo', 'title': 'titleInfo', 'subTitle': 'titleInfo', 'abstract': 'mods', 'accessCondition': 'mods', 'extension': 'mods', 'genre': 'mods', 'identifier': 'mods', 'language': 'mods', 'location': 'mods', 'name': 'mods', 'note': 'mods', 'originInfo': 'mods', 'physicalDescription': 'mods', 'recordInfo': 'mods', 'titleInfo': 'mods', 'typeOfResource': 'mods'}

class elem(etree.ElementBase):
  Parent = parents[tag]
    
def makeMODS(tag, text):
  el = elem(tag)
  el.text = text
  el.Parent = parents[tag]
  if el.Parent is None:
      host = makeMODS(parents[tag])
      host.append(el)
      return host
  else:
      return el

def buildRecord(record):
  root = etree.Element('mods')
  for tag, text in record.items():
    el = makeMODS(tag, text)
    root.append(el)
#    el = etree.Element(tag)
#    el.text = text
#    el.Parent = parents[tag]
#    if el.Parent is None:
      
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