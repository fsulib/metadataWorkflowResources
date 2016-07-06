#!/usr/bin/env python3

import csv
import requests
import os
import sys

# 1st argument needs to be a CSV file with a column with the header 'IID', containing OBJ IID's
name = os.path.splitext(sys.argv[1])[0]
in_file = open(name +'.csv', newline='')
records =  csv.DictReader(in_file)
with open(name + 'OUT.csv', 'w', newline='') as out_file:
    fieldnames = ['IID', 'PURL', 'PID']
    CSVwriter = csv.DictWriter(out_file, fieldnames=fieldnames)
    CSVwriter.writeheader()
    for record in records:
        print(record['IID'])
        PURL = "http://purl.flvc.org/fsu/fd/" + record['IID']
        pid_get = requests.get(PURL)
        CSVwriter.writerow({'IID': record['IID'], 'PURL': PURL, 'PID': pid_get.url.split('/')[5].replace('%3A', ':')})
in_file.close()        
    