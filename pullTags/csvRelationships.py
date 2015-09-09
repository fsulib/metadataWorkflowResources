import xml.etree.ElementTree as ET
import csv
import sys
import os
import re

def writeCSV(fileName):
  purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
  pid = re.compile('fsu:[0-9]*')
  header = ['PURL;', 'PID;' 'Title;', 'Creator;', 'Date;', 'Notes;', 'Comments/Shares;']
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3'}
  with open(fileName + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(header)
    tree = ET.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
      data = []
      for identifier in record.iterfind('.//{%s}identifier' % NS['mods']):
        m = purl.search(identifier.text)
        if m:
          data.append(m.group())
          data.append(';')
      for identifier in record.iterfind('.//{%s}identifier' % NS['mods']):
        m = pid.search(identifier.text)
        if m:
          data.append(m.group())
          data.append(';')
      for title in record.iterfind('.//{%s}title' % NS['mods']):
        data.append('%s' % title.text)
      data.append(';')        
      for creator in record.iterfind('.//{%s}creator' % NS['mods']):
        data.append('%s' % creator.text)
      data.append(';')      
      for date in record.iterfind('.//{%s}date' % NS['mods']):
        data.append('%s' % date.text)
      data.append(';')
      for subject in record.iterfind('.//{%s}subject' % NS['mods']):
        data.append('%s' % subject.text)
      data.append(';')
      data.append(';')
      writer.writerow(data)

name = os.path.splitext(sys.argv[1])[0]
writeCSV(name)
print('Spreadsheet created.')
