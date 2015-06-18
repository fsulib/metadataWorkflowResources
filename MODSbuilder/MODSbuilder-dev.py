from lxml import etree
import csv
import sys
import os

NS = {None:'http://www.loc.gov/mods/v3', 'flvc':'info:flvc/manifest/v1'}

#def makeMODS(tag, text):
  

def buildRecord(record):
  root = etree.Element('mods', nsmap=None, xsi:SchemaLocation='http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd', version='3.4' )
  for tag, text in record.items():
#    tag = 
#    print(path, text)
    child = etree.SubElement(root, tag)
    child.text = text
  xmlString = etree.tostring(root, pretty_print=True)
  f = open('output/%s.xml' % record['IID'], 'w')
  f.write(xmlString.decode('utf-8'))
  f.close()

def readCSV(fileIn):
  with open(fileIn) as csvfile:
    source = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in source:
#      print('%s' % row['IID'])
#      for key, value in row.items():
      buildRecord(row)  


name = sys.argv[1]
readCSV(name)

#DICTIONARY METHODS
#Dictionary.keys() --> gets list of keys
#for key, value in Dictionary.items():
#  print(key, value)   
#----------------------> iterate over dict contents

#BUILDING XML
#root = etree.Element('root')
#etree.SubElement(root, 'element').text = 'test text'
#xmlString = etree.tostring(root, pretty_print=True)
#f = open('test.xml', 'w')
#f.write(xmlString.decode('utf-8'))
#f.close()