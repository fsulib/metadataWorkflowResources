import xml.etree.ElementTree as ET
import csv
import sys
import os

def writeCSV(fileName):
  header = ['Identifiers;', 'Title;', 'Creator;', 'Date;']
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/'}
  with open(fileName + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(header)
    tree = ET.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}dc' % NS['oai_dc'] ):
      data = []
      for identifier in record.iterfind('.//{%s}identifier' % NS['dc']):
        data.append('%s' % identifier.text)
      data.append(';')
      for title in record.iterfind('.//{%s}title' % NS['dc']):
        data.append('%s' % title.text)
      data.append(';')        
      for creator in record.iterfind('.//{%s}creator' % NS['dc']):
        data.append('%s' % creator.text)
      data.append(';')      
      for date in record.iterfind('.//{%s}date' % NS['dc']):
        data.append('%s' % date.text)
      data.append(';')        
      writer.writerow(data)

name = os.path.splitext(sys.argv[1])[0]
writeCSV(name)
print('Spreadsheet created.')
