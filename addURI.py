#!/usr/bin/env python3

import os
import re
import sys
import logging
import datetime
import requests

sys.path.append('addURI/assets/')

import clean_up
import lc_vocab
from pymods import mods


LOC_try_index = 0                     
error_log = False

def get_keyword_list(record):
    # generate keywords from note@displayLabel="Keywords" element
    keywords = []
    for note in mods.note(record):
        if isinstance(note, dict):
            if 'Keywords' in note.keys():
                for keyword in note['Keywords'].split(','):
                    keywords.append(keyword.strip()) # going to have to deal with en & em dashes
    return keywords


# init error logger
logging.basicConfig(filename='addURI_LOG{0}.txt'.format(datetime.date.today()),
                    level=logging.WARNING,
                    format='%(asctime)s -- %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')

# loop over MODS record list returned by pymods.mods.load                    
for record in mods.load(sys.argv[1]):
    record_write = False
    appending_subjects = []

    # check timeout index
    while LOC_try_index <= 5:
        record_PID = mods.pid_search(record)
        print("Checking:", record_PID)

        # loops over keywords 
        for keyword in get_keyword_list(record): 
            URI_search = lc_vocab.uri_lookup(keyword, record_PID)
            print(keyword)

            try:
            
                # TGM subject found
                if URI_search.tgm() is not None:
                    appending_subjects.append({'tgm': URI_search.tgm()}) 
                    LOC_try_index = 0
                    record_write = True
                    
                # LCSH subject found
                elif URI_search.lcsh() is not None:
                    appending_subjects.append({'lcsh_simple': URI_search.lcsh()}) #need heading & type
                    LOC_try_index = 0
                    record_write = True
                
                # no subject found
                else:
                    error_log = True
                    pass
                    
            # catch timeout exception and increase timeout index        
            except requests.exceptions.Timeout:
                logging.warning("The request timed out after five seconds. {0}-{1}".format(record_PID, keyword))
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
        print("Writing: ", record_PID)
        lc_vocab.write_record_subjects(record, appending_subjects, record_PID)
    
# clean up namespace prefixes for diginole
clean_up.clean('improvedMODS/')

# indicate errors were logged 
if error_log is True:
    print("\nSome keywords not found.\nDetails logged to: addURI_LOG{0}.txt\n".format(datetime.date.today()))
