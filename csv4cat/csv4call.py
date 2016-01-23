from lxml import etree
import csv
import sys
import os
import re

def aleph(fileName):
  print('aleph')
#  purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
#  pid = re.compile('fsu:[0-9]*')
#  header = ['PURL', 'PID' 'Title', 'Creator', 'Date', 'Notes', 'Comments/Shares']
#  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
#  with open(fileName + '.csv', 'w') as f:
#    writer = csv.writer(f, delimiter=',')
#    writer.writerow(header)
#    tree = etree.parse(fileName + '.xml')
#    root = tree.getroot()
#    for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
#      data = []
#      for url in record.iterfind('./{%s}location/{%s}url' % NS['mods']):
#        m = purl.search(identifier.text)
#        if m:
#          data.append(m.group())
#        else:
#          data.append('null')
#          data.append(';')
#      for identifier in record.iterfind('.//{%s}identifier' % NS['mods']):
#        m = pid.search(identifier.text)
#        if m:
#          data.append(m.group())
#        else:
#          data.append('null')
#          data.append(';')
#      for title in record.iterfind('.//{%s}titleInfo' % NS['mods']):
#        if title.find('./{%s}nonSort' % NS['mods']):
#          title-full = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text
#          if title.find('./{%s}subTitle' % NS['mods']):
#            title-full = title-full + ': ' + title.find('./{%s}subTitle' % NS['mods']).text
#        data.append('%s' % title-full)
#       data.append(';')        
#      for creator in record.iterfind('.//{%s}name' % NS['mods']):
#        data.append('%s' % creator.text)
#      data.append(';')      
#      for date in record.iterfind('.//{%s}date' % NS['mods']):
#        data.append('%s' % date.text)
#      data.append(';')
#      for description in record.iterfind('.//{%s}abstract' % NS['mods']):
#        data.append('%s' % description.text)
#      data.append(';')
#      data.append(';')
#      writer.writerow(data)

def archon(fileName):
  series = input("Enter a number for the digital series: ")
  collNum = input("Enter a collection ID number: ")
  purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
  with open(fileName + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    data = [collNum, str(series), "", "", "", "", 'Items available online', "", "Items hosted in Digital Collections at DigiNole. Please copy the link into your browser to access."]
    writer.writerow(data)
    tree = etree.parse(fileName + '.xml')
    root = tree.getroot()
    n = 1

    # fields to pull: collection ID, Series #, Subseries #, Box #, Folder #, Item #, Title, Date, Description (i.e. PURL)
    for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
      data = [collNum, str(series), "", "", "", str(n)]

      #title
      for title in record.iterfind('.//{%s}titleInfo' % NS['mods']):
        if title.find('./{%s}nonSort' % NS['mods']) is not None and title.find('./{%s}title' % NS['mods']) is not None and title.find('./{%s}subTitle' % NS['mods']) is not None:
          titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text + ': ' + title.find('./{%s}subTitle' % NS['mods']).text
        elif title.find('./{%s}nonSort' % NS['mods']) is not None and title.find('./{%s}title' % NS['mods']) is not None:
          titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text
        else:
          titleFull = title.find('./{%s}title' % NS['mods']).text
        data.append(titleFull)

      #date
      if record.find('./{%s}originInfo/{%s}copyrightDate' % (NS['mods'], NS['mods'])) is not None:
        date = record.find('./{%s}originInfo/{%s}copyrightDate' % (NS['mods'], NS['mods'])).text
      elif record.find('./{%s}originInfo/{%s}dateCreated' % (NS['mods'], NS['mods'])) is not None:
        date = record.find('./{%s}originInfo/{%s}dateCreated' % (NS['mods'], NS['mods'])).text
      elif record.find('./{%s}originInfo/{%s}dateIssued' % (NS['mods'], NS['mods'])) is not None:
        date = record.find('./{%s}originInfo/{%s}dateIssued' % (NS['mods'], NS['mods'])).text
      elif record.find('./{%s}originInfo/{%s}dateOther' % (NS['mods'], NS['mods'])) is not None:
        date = record.find('./{%s}originInfo/{%s}dateOther' % (NS['mods'], NS['mods'])).text
      else:
        date = ""
      data.append(date)
      
      #description (PURL)
      

#      for description in record.iterfind('.//{%s}abstract' % NS['mods']):
#        data.append('%s' % description.text)
      writer.writerow(data)
      n = n + 1

#name = os.path.splitext(sys.argv[1])[0]
#writeCSV(name)
#print('Spreadsheet created.')
