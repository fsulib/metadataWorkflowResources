"""
Public Domain Searcher

Generates a report to help identify items newly entering the public domain.

The first argument is a year to compare against, the second argument is a directory location of OAI-PMH MODSXML files to analyse. The workflow is to
1. Collect MODS data from the OAI-PMH feed
2. Run this script with the appropriate year and file location
3. Share resulting spreadsheet with colleagues who will ultimately perform the analysis to determine if the object has actually entered the public domain and is free of copyright restrictions.

A follow-up script is needed to update the actual MODS records and package them for reingest.
"""

import os
from pathlib import Path
import dateparser
import pymods
import sys
import csv


def data_file_search(dir):
    for f in os.listdir(dir):
        yield os.path.join(dir, f)


def parse_dates(dates):
    """"""
    earliest_date = None
    earliest_date_type = None
    for d in dates:
        if not earliest_date:
            earliest_date = dateparser.parse(d.text)
            earliest_date_type = d.type.split('}')[1]
        elif earliest_date > dateparser.parse(d.text):
            earliest_date = dateparser.parse(d.text)
            earliest_date_type = d.type.split('}')[1]
        else:
            pass
    return earliest_date_type, earliest_date


def parse_mods(mods_file, year):
    for record in pymods.OAIReader(mods_file):
        if record.metadata is not None:
            try:
                uri = record.metadata.rights[0].uri
            except (AttributeError, IndexError):
                uri = None
            if uri != 'http://rightsstatements.org/vocab/NoC-US/1.0/':
                try:
                    dt, d = parse_dates(record.metadata.dates)
                except TypeError:
                    pass
                pid = record.oai_urn.split(':')[2].replace('_', ':')
                try:
                    iid = record.metadata.iid
                except UnboundLocalError:
                    iid = None
                try:
                    date_type = dt
                except UnboundLocalError:
                    date_type = None
                try:
                    date = d
                except UnboundLocalError:
                    date = None
                try:
                    if date.year <= int(year):
                        yield pid, iid, str(date.date()), date_type
                except AttributeError:
                    pass


if __name__ == "__main__":
    year = sys.argv[1]
    data_directory = sys.argv[2]
    with open('public_domain_report.csv', 'w') as csv_output:
        fieldnames = ['PID', 'Link to item', 'IID', 'Date', 'Date type']
        csv_writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        csv_writer.writeheader()
        for file in data_file_search(data_directory):
            for p, i, date, date_type in parse_mods(file, year):
                print(p, i, date, date_type)
                csv_writer.writerow({'PID': p,
                                     'Link to item': f'https://diginole.lib.fsu.edu/islandora/orbject/{p}',
                                     'IID': i,
                                     'Date': date,
                                     'Date type': date_type})
