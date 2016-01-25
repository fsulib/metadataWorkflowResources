from lxml import etree
import csv
import sys
import os
import re

'''
def nameGenerator(name, NS, fullName):
  names = {}
  for namePart in name.iterfind('./{%s}namePart' % NS['mods']):
    if len(namePart.attrib) == 0:
#      print(namePart.text)
      fullName = fullName + namePart.text
    else:
      for key, value in namePart.attrib.items():
#        print(value, namePart.text)
        names[value] = namePart.text
        print(fullName, namePart.text, value)
'''


'''
  if 'family' and 'given' and 'termsOfAddress' and 'date' in names.keys():
    fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ' ' + names['date']
  elif 'family' and 'given' and not 'termsOfAddress' and 'date' in names.keys():
    fullName = fullName + names['family'] + ', ' + names['given'] + ' ' + names['date']
  elif 'family' and 'given' and not 'termsOfAddress' and not 'date' in names.keys():
    fullname = fullName + names['family'] + ', ' + names['given']
  elif not 'family' and 'given' and not 'termsOfAddress' and 'date' in names.keys():
    fullname = fullName + ' ' + names['given'] + ' ' + names['date']
  elif not 'family' and not 'given' and 'termsOfAddress' and not 'date' in names.keys():
    fullName = fullName + ' ' + names['termsOfAddress']
  elif not 'family' and not 'given' and 'termsOfAddress' and 'date' in names.keys():
    fullName = fullName + ' ' + names['termsOfAddress'] + ', ' + names['date']
  elif 'family' and not 'given' and 'termsOfAddress' and not 'date' in names.keys():
    fullName = fullName + names['family'] + ', ' + names['termsOfAddress']
  return fullName
'''
NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
tree = etree.parse('fsu_cookbooksandherbals.xml')
root = tree.getroot()
purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
for record in root.iterfind('.//{%s}mods' % NS['mods']):
  allNames = ""
  for name in record.iterfind('./{%s}name' % NS['mods']):
    fullName = ""
    if len(name.findall('./{%s}namePart' % NS['mods'])) > 1:
      print('trace01')
      if name.xpath('./child::namePart[attribute::type="family"]'):
        print('family name')
#        fullName = fullName + name.find('./{%s}namePart[type="family"]' % NS['mods']).text
        if name.find('./{%s}namePart[type="given"]' % NS['mods']):
          fullName = fullName + ', ' + name.find('./{%s}namePart[type="given"]' % NS['mods']).text
      else:
        print('trace03')
        if len(name.find('./{%s}namePart' % NS['mods']).attrib.items()) == 0:
          fullName = fullName + name.find('./{%s}namePart' % NS['mods']).text
      if name.xpath('./child::namePart[attribute::type="termsOfAddress"]'):
        fullName = fullName + ', ' + name.xpath('./child::namePart[attribute::type="termsOfAddress"]').text
      if name.xpath('./child::namePart[attribute::type="date"]'):
        fullName = fullName + ', ' + name.xpath('./child::namePart[attribute::type="date"]').text
    else:
      print('trace02')
      fullName = fullName + name.find('./{%s}namePart' % NS['mods']).text
    allNames = allNames + fullName + ' || '
    print(allNames)
    
    
    
    
    '''
    #XPath example: child::para[attribute::type="warning"]
      if 'type' in name.find('./{%s}namePart' % NS['mods']).attrib:
        print('Parted name...')        
        if namePart.attrib['type'] == 'family':
          nameFamily = namePart.text
        elif namePart.attrib['type'] == 'given':
          nameGiven = namePart.text
        elif namePart.attrib['type'] == 'date':
          nameDate = namePart.text
        fullName = nameFamily + ', ' + nameGiven + ' ' + nameDate
      elif name.find('./{%s}namePart' % NS['mods']):
        fullName = name.find('./{%s}namePart' % NS['mods']).text
      else:
        fullName = ""
      print(fullName)
      
      
      
            if name.find('./{%s}namePart[type="family"]' % NS['mods']) and name.find('./{%s}namePart[type="given"]' % NS['mods']) and name.find('./{%s}namePart[type="date"]' % NS['mods']) is not None:
        fullName = name.find('./{%s}namePart[type="family"]' % NS['mods']).text + ', ' + name.find('./{%s}namePart[type="given"]' % NS['mods']).text + ' ' + name.find('./{%s}namePart[type="date"]' % NS['mods']).text
      if name.find('./{%s}namePart[type="given"]' % NS['mods']) is not None:
        fullName = fullName + name.find('./{%s}namePart[type="given"]' % NS['mods']).text
      if name.find('./{%s}namePart[type="date"]' % NS['mods']) is not None:
        fullName = fullName + ' ' + name.find('./{%s}namePart[type="date"]' % NS['mods']).text
 '''   
#    if name.attrib['type'] == 'corporate':
#      names.append('corporate')
#  for item in names:
#    items = items + item
#  print(items)
    



#  for url in record.iterfind('./{%s}location/{%s}url' % (NS['mods'], NS['mods'])):
#    m = purl.search(url.text)
#    if m:
#      print(m.group())


#  if 'keyDate' in record.xpath('./{%s}originInfo/{%s}*' % (NS['mods'], NS['mods'])).attrib:
#    date = record.xpath('./{%s}originInfo/{%s}*' % (NS['mods'], NS['mods'])).text
#  if record.find('./{%s}originInfo/{%s}copyrightDate' % (NS['mods'], NS['mods'])) is not None:
#    date = record.find('./{%s}originInfo/{%s}copyrightDate' % (NS['mods'], NS['mods'])).text
#  elif record.find('./{%s}originInfo/{%s}dateCreated' % (NS['mods'], NS['mods'])) is not None:
#    date = record.find('./{%s}originInfo/{%s}dateCreated' % (NS['mods'], NS['mods'])).text
#  elif record.find('./{%s}originInfo/{%s}dateIssued' % (NS['mods'], NS['mods'])) is not None:
#    date = record.find('./{%s}originInfo/{%s}dateIssued' % (NS['mods'], NS['mods'])).text
#  elif record.find('./{%s}originInfo/{%s}dateOther' % (NS['mods'], NS['mods'])) is not None:
#    date = record.find('./{%s}originInfo/{%s}dateOther' % (NS['mods'], NS['mods'])).text
#  else:
#    date = 'No'
#  print(date)


#  for title in record.iterfind('.//{%s}titleInfo' % NS['mods']):
#    if title.find('./{%s}nonSort' % NS['mods']) is not None and title.find('./{%s}title' % NS['mods']) is not None and title.find('./{%s}subTitle' % NS['mods']) is not None:
#      titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text + ': ' + title.find('./{%s}subTitle' % NS['mods']).text
#    elif title.find('./{%s}nonSort' % NS['mods']) is not None and title.find('./{%s}title' % NS['mods']) is not None:
#      titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text
#    else:
#      titleFull = title.find('./{%s}title' % NS['mods']).text
#    print(titleFull)
# future-proofing warning for below 
#    if title.find('./{%s}title' % NS['mods']) and title.find('./{%s}nonSort' % NS['mods']) and title.find('./{%s}subTitle' % NS['mods']):
#    print(title.find('./{%s}title' % NS['mods']).text)
#      titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text + ': ' + title.find('./{%s}subTitle' % NS['mods']).text
#    elif title.find('./{%s}title' % NS['mods']) and title.find('./{%s}nonSort' % NS['mods']):
#      titleFull = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text
#    else:
#      titleFull = title.find('./{%s}title' % NS['mods']).text
#  print(titleFull)
#    if title.find('./{%s}nonSort' % NS['mods']):
#      title-full = title.find('./{%s}nonSort' % NS['mods']).text + ' ' + title.find('./{%s}title' % NS['mods']).text
#        if title.find('./{%s}subTitle' % NS['mods']):
#          title-full = title-full + ': ' + title.find('./{%s}subTitle' % NS['mods']).text
