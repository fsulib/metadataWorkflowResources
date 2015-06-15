from lxml import etree
import csv
import sys

def buildMODS(record):
  root = etree.Element('mods')
  for path, text in record.items():
    print(path, text)
    
def readCSV(fileIn):
  with open(fileIn) as csvfile:
    source = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in source:
      buildMODS(row) 
      
name = sys.argv[1]
readCSV(name)      