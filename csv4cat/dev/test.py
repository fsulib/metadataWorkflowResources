from lxml import etree
import csv
import sys
import os
import re

def nameGen(names, fullName):
#  print('nameGen', names)
  keys = []
  for key in names.keys():
    keys.append(key)
  #print(keys)  
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
  
NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
tree = etree.parse('fsu_cookbooksandherbals.xml')
root = tree.getroot()
purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
for record in root.iterfind('.//{%s}mods' % NS['mods']):
  allNames = ""
  for name in record.iterfind('./{%s}name' % NS['mods']):
    fullName = ""
    if len(name.findall('./{%s}namePart' % NS['mods'])) > 1:
      #print('Multipart name')
      names = {}
      for namePart in name.findall('./{%s}namePart' % NS['mods']):
        if 'type' not in namePart.keys():
          fullName = namePart.text
        elif 'type' in namePart.keys():
          names[namePart.attrib['type']] = namePart.text
      #print(names)
      nameGen(names, fullName)
    else:
      #print('Single part name')
      fullName = fullName + name.find('./{%s}namePart' % NS['mods']).text
    allNames = allNames + fullName + ' || '
  print(allNames)
			
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