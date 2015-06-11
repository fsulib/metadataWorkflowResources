from lxml import etree
import csv
import sys
import os

def readCSV(fileIn):
  with open(fileIn) as csvfile:
    source = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in source:
      print('%s' % row['IID'])

name = sys.argv[1]
readCSV(name)




#root = etree.Element('root')
#etree.SubElement(root, 'element').text = 'test text'
#xmlString = etree.tostring(root, pretty_print=True)
#f = open('test.xml', 'w')
#f.write(xmlString.decode('utf-8'))
#f.close()