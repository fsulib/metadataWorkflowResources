from lxml import etree
import csv
import sys
import os
import re

NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
tree = etree.parse('fsu_nap01.xml')
root = tree.getroot()
purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
for record in root.iterfind('.//{%s}mods' % NS['mods']):
  print('record')
  for url in record.find('./{%s}location/{%s}url' % (NS['mods'], NS['mods'])):
    print('url')
    m = purl.search(url.text)
    if m:
      print(m.group())


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