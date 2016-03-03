#!/usr/bin/env python3

import requests
import sys

def getRecords(pidFile):
    for line in open(pidFile, 'r'):
        r = requests.get('https://fsu.digital.flvc.org/islandora/object/{0}/datastream/MODS/download'.format(line.split('\n')[0]))
        r.encoding = 'utf8'
        outFile = open('MODS/{0}.xml'.format(line.split('\n')[0]), 'w')
        outFile.write(r.text)
        outFile.close()

getRecords(sys.argv[1])
