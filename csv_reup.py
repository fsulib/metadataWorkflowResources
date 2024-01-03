import sys
import time
import requests
from pathlib import Path
from io import BytesIO
from lxml import etree
from datetime import date

TODAY = date.today()
mods = '{http://www.loc.gov/mods/v3}'
nsmap = {None: 'http://www.loc.gov/mods/v3',
         'mods': 'http://www.loc.gov/mods/v3'}

def parse_csv_for_pids(reup_file):
    """

    """
    import csv
    reup_file = Path(reup_file).absolute()
    with open(reup_file) as f:
        reup_csv = csv.DictReader(f)
        for row in reup_csv:
            #print(row['PID'])
            yield row['PID'], row['Description']


if __name__ == "__main__":
    i = 1
    j = 1

    for pid, desc in parse_csv_for_pids(sys.argv[1]):
        Path(f'io/mods-{TODAY}-batch{i}').mkdir(parents=True, exist_ok=True)

        print(f'Retrieving {pid}')
        r = requests.get(f'https://diginole.lib.fsu.edu/islandora/object/{pid}/datastream/MODS/view')

        # head to next pid if Islandora can't find object
        if r.status_code != 200:
            continue

        # XML parsing w/ LXML
        xml_data = BytesIO(r.content)
        record_tree = etree.parse(xml_data)
        record_root = record_tree.getroot()
        abstract = record_root.find(f'{mods}abstract')
        if abstract is not None:
            if abstract.text == desc:
                continue
            else:
                abstract.text = desc
        else:
            if desc:
                abs_elem = etree.SubElement(record_root, f'{mods}abstract')
                abs_elem.text = desc
        output = open(f'io/mods-{TODAY}-batch{i}/{pid.replace(":", "_")}_MODS.xml', 'w')
        output.write(etree.tostring(record_root,
                                    pretty_print=True,
                                    xml_declaration=True,
                                    encoding="UTF-8").decode('utf-8'))
        output.close()
        time.sleep(1)
        j = j + 1
        if j > 5000:
            i = i + 1
            j = 1
            continue
    exit(0)
