import xml.etree.ElementTree as ET
import csv
import sys
import os

def getData(element, nameSpace):
  for tag in root.iterfind('.//{%s}%s' % nameSpace, element):
    data.append(tag.text)
    return data

def writeCSV(fileName):
  header = ['Identifiers', 'Title', 'Date', 'Creator']
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1'}
  with open(fileName + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    tree = ET.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}record' % NS['oai_dc'] ):
      data = []
      data.append(getData(identifier, NS['dc']))
      data.append(getData(title, NS['dc']))
      data.append(getData(date, NS['dc']))
      data.append(getData(creator, NS['dc']))
      writer.writerow(data)

name = os.path.splitext(sys.argv[1])[0]
writeCSV(name)
print('Spreadsheet created.')
