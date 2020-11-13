#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup

def getRecords(pidFile):
    for line in open(pidFile, 'r'):
        pid = line.split('\n')[0]
        r = requests.get('https://fsu.digital.flvc.org/islandora/object/{}/datastream/MODS/download'.format(pid))
        r.encoding = 'utf8'
        outFile = open('MODS/{0}.xml'.format(pid.replace(':', '_')), 'w')
        outFile.write(r.text)
        outFile.close()
        request_RELS_EXT = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/RELS-EXT/view'.format(pid))
        if 'rdf:resource="info:fedora/islandora:compoundCModel"' in request_RELS_EXT.text:
            soup = BeautifulSoup(requests.get('https://fsu.digital.flvc.org/islandora/object/{0}'.format(pid)).text, 
                                              'lxml')
            compound = soup.find('div', attrs={'class':'islandora-compound-thumbs'})
            try:
                for a in compound.find_all('a'):
                    ch_pid = a['href'].split('/')[-1].replace('%3A',':')
                    ch_r = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/MODS/download'.format(ch_pid))
                    ch_r.encoding = 'utf8'
                    outFile = open('MODS/{0}.xml'.format(ch_pid.replace(':', '_')), 'w')
                    outFile.write(ch_r.text)
                    outFile.close()
            except AttributeError:
                pass

#arg1 = filename of plaintext file containing PIDs separated by new lines '\n'
getRecords(sys.argv[1])