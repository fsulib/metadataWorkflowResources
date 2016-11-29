#!/usr/bin/env python3

import os
import re
import sys
import logging
import datetime
import requests
from lxml import etree

sys.path.append('metadataWorkflowResources/assets/')

import lc_vocab
from pymods import mods, fsudl


LOC_try_index = 0                     
error_log = False

def get_subject_list(record):
    # get lcsh terms
    subject_list = []
    for subject in record.iterfind('.//{http://www.loc.gov/mods/v3}subject'):
        if 'authority' in subject.attrib.keys():
            if 'lcsh' == subject.attrib['authority']:
                for child in subject.iterchildren():
                    subject_list.append(child.text.replace(u'\u2014', '--').replace(u'\u2013', '--'))
                # remove subjects that will be checked & re-added
                record.remove(subject)
    return subject_list


# init error logger
logging.basicConfig(filename='addURI_LOG{0}.txt'.format(datetime.date.today()),
                    level=logging.WARNING,
                    format='%(asctime)s -- %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')

# loop over MODS record list returned by pymods.mods.load                    
for record in mods.load(sys.argv[1]):
    record_write = True
    appending_subjects = []

    # check timeout index
    while LOC_try_index <= 5:
        record_IID = fsudl.local_identifier(record)
        print("Checking:", record_IID)

        # loops over keywords 
        for subject in get_subject_list(record): 

            if '--' not in subject:
                
                try:
                        
                    # LCSH simple
                    if lc_vocab.uri_lookup.lcsh(subject, record_IID) is not None:
                        appending_subjects.append({'lcsh_simple': lc_vocab.uri_lookup.lcsh(subject, record_IID)}) #need heading & type
                        record_write = True
                    
                    # no subject found
                    else:
                        pass
            
                # catch timeout exception and increase timeout index
                except requests.exceptions.Timeout:
                    logging.warning("The request timed out after five seconds. {0}-{1}".format(record_IID, subject))
                    LOC_try_index = LOC_try_index + 1
                
            elif '--' in subject:
            
                try: 
                    
                    # LCSH complex
                    if lc_vocab.uri_lookup.lcsh_complex(subject, record_IID) is not None:
                        appending_subjects.append({'lcsh_complex': lc_vocab.uri_lookup.lcsh_complex(subject, record_IID)}) #need heading & type
                        record_write = True
                    
                    # no subject found
                    else:
                        pass
                
                # catch timeout exception and increase timeout index
                except requests.exceptions.Timeout:
                    logging.warning("The request timed out after five seconds. {0}-{1}".format(record_IID, subject))
                    LOC_try_index = LOC_try_index + 1

        break                
                    
    # LOC has timed out multiple times
    else:
        print("\nid.loc.gov seems unavailable at this time. Try again later.\n")
        break

    # if any records have new subject values, write them    
    if record_write == True:
        if 'improvedMODS' not in os.listdir():
            os.mkdir('improvedMODS')
        print("Writing: ", record_IID)
        lc_vocab.write_record_subjects(record, appending_subjects, record_IID)

# indicate errors were logged 
if error_log is True:
    print("\nSome keywords not found.\nDetails logged to: addURI_LOG{0}.txt\n".format(datetime.date.today()))
