from lxml import etree
import csv
import sys
import os

NS = {'mods':'http://www.loc.gov/mods/v3', 'flvc':'info:flvc/manifest/v1'}

def buildMODS(record):
  root = etree.Element('mods')
  for path, text in record.items():
    print(path, text)
  

def readCSV(fileIn):
  with open(fileIn) as csvfile:
    source = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in source:
#      print('%s' % row['IID'])
#      for key, value in row.items():
      buildMODS(row)  


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