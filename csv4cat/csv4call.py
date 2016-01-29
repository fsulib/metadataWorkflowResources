from lxml import etree
import csv
import re

def nameGen(names, fullName):
  keys = []
  for key in names.keys():
    keys.append(key)
  if all(x in keys for x in ['family', 'given', 'termsOfAddress', 'date']):
    fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
  elif all(x in keys for x in ['family', 'given', 'date']):
    fullName = fullName + names['family'] + ', ' + names['given'] + ' ' + names['date']
  elif all(x in keys for x in ['family', 'given', 'termsOfAddress']):
    fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress']
  elif all(x in keys for x in ['family', 'termsOfAddress', 'date']):
    fullName = fullName + names['family'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
  elif all(x in keys for x in ['given', 'termsOfAddress', 'date']):
    fullName = fullName + names['given'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
  elif all(x in keys for x in ['family', 'given']):
    fullName = fullName + names['family'] + ', ' + names['given']
  elif all(x in keys for x in ['family', 'date']):
    fullName = fullName + names['family'] + ', ' + names['date']
  elif all(x in keys for x in ['family', 'termsOfAddress']):
    fullName = fullName + names['family'] + ', ' + names['termsOfAddress']
  elif all(x in keys for x in ['given', 'date']):
    fullName = fullName + names['given'] + ', ' + names['date']
  elif all(x in keys for x in ['given', 'termsOfAddress']):
    fullName = fullName + names['given'] + ', ' + names['termsOfAddress']
  elif all(x in keys for x in ['termsOfAddress', 'date']):
    fullName = fullName + ', ' + names['termsOfAddress'] + ' ' + names['date']
  elif 'date' in keys:
    fullName = fullName + ', ' + names['date']
  elif 'termsOfAddress' in keys:
    fullName = fullName + ', ' + names['termsOfAddress']
  return fullName

def aleph(fileName):
  purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
  pid = re.compile('fsu:[0-9]*')
  header = ['PURL', 'PID', 'Title', 'Creators', 'Date', 'Extent', 'Abstract', 'Notes', 'Comments/Shares']
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
  with open(fileName + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
    tree = etree.parse(fileName + '.xml')
    root = tree.getroot()
    for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
      data = []
      
      #PURL
      for url in record.iterfind('./{%s}location/{%s}url' % (NS['mods'], NS['mods'])):
        m = purl.search(url.text)
        if m:
          data.append(m.group())
      
      #PID
      for identifier in record.iterfind('.//{%s}identifier' % NS['mods']):
        m = pid.search(identifier.text)
        if m:
          data.append(m.group())
      
      #title
      allTitles = []
      for title in record.iterfind('.//{%s}titleInfo' % NS['mods']):
        if title.find('./{%s}nonSort' % NS['mods']) is not None and title.find('./{%s}title' % NS['mods']) is not None and title.find('./{%s}subTitle' % NS['mods']) is not None:
          titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text + ': ' + title.find('./{%s}subTitle' % NS['mods']).text
        elif title.find('./{%s}nonSort' % NS['mods']) is not None and title.find('./{%s}title' % NS['mods']) is not None:
          titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text
        else:
          titleFull = title.find('./{%s}title' % NS['mods']).text
        allTitles.append(titleFull)	 
      data.append(allTitles)
      
      #names
      allNames = []
      for name in record.iterfind('./{%s}name' % NS['mods']):
        fullName = ""
        if len(name.findall('./{%s}namePart' % NS['mods'])) > 1:
          #Multipart name
          names = {}
          for namePart in name.findall('./{%s}namePart' % NS['mods']):
            if 'type' not in namePart.keys():
              fullName = namePart.text
            elif 'type' in namePart.keys():
              names[namePart.attrib['type']] = namePart.text
          fullName = nameGen(names, fullName)
        else:
          #Single part name
          fullName = fullName + name.find('./{%s}namePart' % NS['mods']).text
        allNames.append(fullName)
      data.append(allNames)
      
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
      
      #extent
      extent = ""
      data.append(extent)

      #abstract
      for description in record.iterfind('.//{%s}abstract' % NS['mods']):
        data.append('%s' % description.text)      

      #notes
      allNotes = ""
      for note in record.iterfind('./{%s}note' % NS['mods']):
        allNotes = allNotes + note.text + ' || '
      data.append(allNotes)
      
      #write CSV
      writer.writerow(data)

def archon(fileName, collNum, series):
  purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
  NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
  with open(fileName + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    data = [collNum, str(series), "", "", "", "", 'Items available online', "", "Items hosted in Digital Collections at DigiNole. Please copy & paste the link into your browser's address bar to access."]
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
      for url in record.iterfind('./{%s}location/{%s}url' % (NS['mods'], NS['mods'])):
        m = purl.search(url.text)
        if m:
          data.append(m.group())
      
      #write to CSV & increase item# index
      writer.writerow(data)
      n = n + 1