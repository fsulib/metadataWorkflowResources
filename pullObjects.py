#!/usr/bin/env python3

import requests
import logging
import datetime
import sys
import os

'''
    Testing PIDs with notes:
        fsu:73090  # OBJ object
        fsu:277457 # PDF object
        fsu:310190 # embargoed
        fsu:274046 # supplements
'''

def getRecords(pidFile):
    
    # iterate over pids in file
    for line in open(pidFile, 'r'):
                
        # assigning these to variable to make life easier
        pid = line.split('\n')[0]
        filename = pid.replace(':','_')
        print('Accessing:', pid)
        
        # ask for and write out MODS to directory
        request_metadata = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/MODS/download'.format(pid))
        request_metadata.encoding = 'utf8'
        os.mkdir('./OBJ_packages/{0}'.format(filename))
        metadata_out = open('OBJ_packages/{0}/{1}.xml'.format(filename, filename), 'w')
        metadata_out.write(request_metadata.text)
        metadata_out.close()
        
        # check if children might be present
        request_RELS_EXT = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/RELS-EXT/view'.format(pid))
        if 'rdf:resource="info:fedora/islandora:compoundCModel"' in request_RELS_EXT.text:
            logging.warning('Compound object; check for children - {0}'.format(pid))
        
        try:
            # first ask for OBJ datastream
            request_OBJ = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/OBJ/download'.format(pid))
            if request_OBJ.status_code == 200:
                with open('OBJ_packages/{0}/{1}.pdf'.format(filename, filename), 'wb') as OBJ_out:
                    OBJ_out.write(request_OBJ.content)
            
            # if OBJ datastream 404s, try PDF datastream
            elif request_OBJ.status_code == 404:
                request_PDF = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/PDF/download'.format(pid))
                if request_PDF.status_code == 200:
                    with open('OBJ_packages/{0}/{1}.pdf'.format(filename, filename), 'wb') as PDF_out:
                        PDF_out.write(request_PDF.content)
                
                # PDF's under embargoes will be logged
                elif request_PDF.status_code == 403:
                    logging.warning('403: Embargo - {0}'.format(pid))
                    
            elif request_OBJ.status_code == 403:
                logging.warning('403: Embargo - {0}'.format(pid))
        
        # catch timeout exceptions
        except requests.exceptions.Timeout:
            logging.warning('Request timed out - {0}'.format(pid))

# begin building directory structure
if 'OBJ_packages' not in os.listdir():
    os.mkdir('./OBJ_packages')
    
# init error logger
logging.basicConfig(filename='pullOBJ_LOG{0}.txt'.format(datetime.date.today()),
                    level=logging.WARNING,
                    format='%(asctime)s -- %(levelname)s -- %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')    

#arg1 = filename of plaintext file containing PIDs separated by new lines '\n'
getRecords(sys.argv[1])