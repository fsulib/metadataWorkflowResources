from lxml import etree
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
  
def mods_name_generator(mods_record, nameSpace_dict):
    allNames = []
    for name in mods_record.iterfind('./{%s}name' % nameSpace_dict['mods']):
        fullName = ""
        if len(name.findall('./{%s}namePart' % nameSpace_dict['mods'])) > 1:
            #Multipart name
            names = {}
            for namePart in name.findall('./{%s}namePart' % nameSpace_dict['mods']):
                if 'type' not in namePart.keys():
                    fullName = namePart.text
                elif 'type' in namePart.keys():
                    names[namePart.attrib['type']] = namePart.text
            fullName = nameGen(names, fullName)
        else:
            #Single part name
            fullName = fullName + name.find('./{%s}namePart' % nameSpace_dict['mods']).text
        allNames.append(fullName)
        return ' || '.join(allNames)
    
def mods_title_generator(mods_record, nameSpace_dict):
    allTitles = []
    for title in mods_record.iterfind('.//{%s}titleInfo' % nameSpace_dict['mods']):
        if title.find('./{%s}nonSort' % nameSpace_dict['mods']) is not None and title.find('./{%s}title' % nameSpace_dict['mods']) is not None and title.find('./{%s}subTitle' % nameSpace_dict['mods']) is not None:
            titleFull = title.find('./{%s}nonSort' % nameSpace_dict['mods']).text + ' ' + title.find('./{%s}title' % nameSpace_dict['mods']).text + ': ' + title.find('./{%s}subTitle' % nameSpace_dict['mods']).text
        elif title.find('./{%s}nonSort' % nameSpace_dict['mods']) is not None and title.find('./{%s}title' % nameSpace_dict['mods']) is not None:
            titleFull = title.find('./{%s}nonSort' % nameSpace_dict['mods']).text + ' ' + title.find('./{%s}title' % nameSpace_dict['mods']).text
        else:
            titleFull = title.find('./{%s}title' % nameSpace_dict['mods']).text
        allTitles.append(titleFull)
        return ' || '.join(allTitles)
    
def mods_date_generator(mods_record, nameSpace_default):
    date_list = ['{%s}dateIssued' % nameSpace_default['mods'],
                 '{%s}dateCreated' % nameSpace_default['mods'],
                 '{%s}copyrightDate' % nameSpace_default['mods'],
                 '{%s}dateOther' % nameSpace_default['mods']]
    ignore_list = ['{%s}place' % nameSpace_default['mods'],
                   '{%s}publisher' % nameSpace_default['mods'],
                   '{%s}dateCaptured' % nameSpace_default['mods'],
                   '{%s}dateValid' % nameSpace_default['mods'],
                   '{%s}dateModified' % nameSpace_default['mods'],
                   '{%s}edition' % nameSpace_default['mods'],
                   '{%s}issuance' % nameSpace_default['mods'],
                   '{%s}frequency' % nameSpace_default['mods']]
    if mods_record.find('./{%s}originInfo' % nameSpace_default['mods']) is not None:
        origin_info = mods_record.find('./{%s}originInfo' % nameSpace_default['mods'])
        date = None
        for child in origin_info.iterchildren():
            if child.tag in date_list:
                # date range
                if 'point' in child.attrib.keys():
                    if child.attrib['point'] == 'start':
                        if date is None:
                            date = child.text
                        else:
                            date = child.text + ' - ' + date
                    elif child.attrib['point'] == 'end':
                        if date is None:
                            date = child.text
                        else:
                            date = date + ' - ' + child.text
                # single date
                else:
                    date = child.text
            elif child.tag in ignore_list:
                pass
        return date
  
def fsudl_purl_search(mods_record, nameSpace_dict):
    purl = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
    for url in mods_record.iterfind('./{%s}location/{%s}url' % (nameSpace_dict['mods'], nameSpace_dict['mods'])):
        match = purl.search(url.text)
        if match is not None:
            return match.group()
      
def fsudl_pid_search(mods_record, nameSpace_dict):
    pid = re.compile('fsu:[0-9]*')
    for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
        match = pid.search(identifier.text)
        if match is not None:
            return match.group()

def mods_subject_generator(mods_record, nameSpace_dict):
    allSubjects = []
    for subject in mods_record.iterfind('.//{%s}subject' % nameSpace_dict['mods']):
        fullSubject = []
        for subjectTerm in subject.iterfind('{%s}subject::child' % nameSpace_dict['mods']):
            fullSubject.append(subjectTerm.text)
    allSubjects.append(fullSubject)
    return allSubjects
