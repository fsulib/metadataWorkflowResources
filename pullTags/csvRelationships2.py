import xml.etree.ElementTree as ET
import csv
import sys
import os
import re

def writeCSV(fileName):
  purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
  pid = re.compile('fsu:[0-9]*')
  header = ['Source', 'Target']
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3'}
  with open(fileName + 'GEPHI' + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(header)
    tree = ET.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}dc' % NS['oai_dc'] ):
      for subject in record.iterfind('.//{%s}subject' % NS['dc']):
          data = []
          for identifier in record.iterfind('.//{%s}identifier' % NS['dc']):
              m = pid.search(identifier.text)
              if m and m is not data[0]:
                  data.append(m.group())
          data.append(subject.text)
          writer.writerow(data)

name = os.path.splitext(sys.argv[1])[0]
writeCSV(name)
print('Spreadsheet created.')
