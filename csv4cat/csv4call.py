from lxml import etree
import csv
from MODStools import mods_name_generator, mods_date_generator, mods_title_generator, fsudl_purl_search, fsudl_pid_search

def aleph(fileName):
    header = ['PURL', 'PID', 'Title', 'Creators', 'Date', 'Extent', 'Abstract', 'Notes', 'Comments/Shares']
    NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
    with open(fileName + '.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        tree = etree.parse(fileName + '.xml')
        root = tree.getroot()
        for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
            data = []
            #PURL
            data.append(fsudl_purl_search(record, NS))
            #PID
            data.append(fsudl_pid_search(record, NS))
            #title
            data.append(mods_title_generator(record, NS))
            #names
            data.append(mods_name_generator(record, NS))
            #date
            data.append(mods_date_generator(record, NS))
            #extent
            extentNotes = []
            for physDesc in record.iterfind('./{%s}physicalDescription' % NS['mods']):
                for extent in physDesc.iterfind('./{%s}extent' % NS['mods']):
                    extentNotes.append(extent.text)      
            data.append(extentNotes)
            #abstract
            abstracts = []
            for description in record.iterfind('.//{%s}abstract' % NS['mods']):
                abstracts.append(description.text)
            data.append(abstracts)
            #notes
            allNotes = []
            for note in record.iterfind('./{%s}note' % NS['mods']):
                allNotes.append(note.text)
            data.append(allNotes)
        #write CSV
        writer.writerow(data)

def archon(fileName, collNum, series):
    NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
    with open(fileName + '.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        data = [collNum, str(series), "", "", "", "", 'Items available online', "", "Items hosted in Digital Collections at DigiNole. Please copy & paste the link into your browser's address bar to access."]
        writer.writerow(data)
        tree = etree.parse(fileName + '.xml')
        root = tree.getroot()
        itemNumber = 1
        # fields to pull: collection ID, Series #, Subseries #, Box #, Folder #, Item #, Title, Date, Description (i.e. PURL)
        for record in root.iterfind('.//{%s}mods' % NS['mods'] ):
            data = [collNum, str(series), "", "", "", str(itemNumber)]
            #title
            data.append(mods_title_generator(record, NS))
            #date
            data.append(mods_date_generator(record, NS))
            #PURL
            data.append('[url]%s[/url]' % fsudl_purl_search(record, NS))
            #write to CSV & increase item# index
            writer.writerow(data)
            itemNumber = itemNumber + 1