#!/usr/bin/env python3

import os
import re
import sys
import time
import logging
import datetime
import requests
from lxml import etree
import pymods

sys.path.append('metadataWorkflowResources/assets/')

import lc_vocab
#from pymods import MODS, FSUDL


LOC_try_index = 0                     
error_log = False

# init error logger
logging.basicConfig(filename='addURI_LOG{0}.txt'.format(datetime.date.today()),
                    level=logging.WARNING,
                    format='%(asctime)s -- %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')


# loop over MODS record list returned by pymods.mods.load                    
for record in pymods.MODSReader(sys.argv[1]):
    record_write = True
    appending_subjects = []

    # check timeout index
    while LOC_try_index <= 5:
        record_IID = record.iid
        print("Checking:", record_IID)

        # loops over keywords 
        for subject in record.subjects:
            URI_search = lc_vocab.uri_lookup(subject.text.replace('&', '%26'), record_IID)
            
            try:
            
                # TGM subject found
                if URI_search.tgm() is not None:
                    appending_subjects.append({'tgm': URI_search.tgm()}) 
                    LOC_try_index = 0
                    record_write = True
                    record.remove(subject.elem)
                    continue
                    
                # no subject found
                else:
                    error_log = True
                    time.sleep(5)
                    pass

            # catch timeout exception and increase timeout index
            except requests.exceptions.Timeout:
                logging.warning("The request timed out after five seconds. {0}-{1}".format(record_IID, subject))
                LOC_try_index = LOC_try_index + 1
            
            if '--' not in subject.text:
                
                try:
                        
                    # LCSH simple
                    if URI_search.lcsh() is not None:
                        appending_subjects.append({'lcsh_simple': URI_search.lcsh()}) #need heading & type
                        LOC_try_index = 0                        
                        record_write = True
                        record.remove(subject.elem)
                    
                    # no subject found
                    else:
                        error_log = True
                        time.sleep(5)
                        pass
            
                # catch timeout exception and increase timeout index
                except requests.exceptions.Timeout:
                    logging.warning("The request timed out after five seconds. {0}-{1}".format(record_IID, subject))
                    LOC_try_index = LOC_try_index + 1
                
            elif '--' in subject.text:
            
                try: 
                    
                    # LCSH complex
                    if URI_search.lcsh_complex() is not None:
                        appending_subjects.append({'lcsh_complex': URI_search.lcsh_complex()}) #need heading & type
                        LOC_try_index = 0
                        record_write = True
                        record.remove(subject.elem)
                    
                    # no subject found
                    else:
                        error_log = True
                        time.sleep(5)
                        pass
                
                # catch timeout exception and increase timeout index
                except requests.exceptions.Timeout:
                    logging.warning("The request timed out after five seconds. {0}-{1}".format(record_IID, subject))
                    LOC_try_index = LOC_try_index + 1
            time.sleep(5)
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
