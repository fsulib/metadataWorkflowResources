#!/usr/bin/env python3

import re
import os
import sys
from pathlib import Path
import shutil
from lxml import etree

nameSpace_default = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 
                     'dc': 'http://purl.org/dc/elements/1.1/', 
                     'mods': 'http://www.loc.gov/mods/v3', 
                     'dcterms': 'http://purl.org/dc/terms',
                     'repox': 'http://repox.ist.utl.pt' }
                     

def oai_dc_pid_search(record, nameSpace_dict=nameSpace_default):
    pid = re.compile('fsu_[0-9]+')
    for identifier in record.iterfind('.//{%s}identifier' % nameSpace_dict['oai_dc']):
        match = pid.search(identifier.text)
        if match:
            return match.group().replace('_',':')
            

def repox_pid_search(record, nameSpace_dict=nameSpace_default):
    pid = re.compile('fsu_[0-9]+')
    match = pid.search(record.attrib['id'])
    if match:
        return match.group().replace('_',':')
                


if __name__ == "__main__":

    edit_record_count = 0
    input_file = Path(sys.argv[1])
    #print(os.path.abspath(input_file))

    with open(os.path.abspath(input_file)) as in_file:    
        with open(os.path.abspath(input_file) + ".tmp", 'w') as out_file:
            tree = etree.parse(in_file)
            root = tree.getroot()
            #print(root.tag)
            
            # repository root file
            if 'repository' in root.tag:
                # check for default oai_dc namespace
                if None not in root.nsmap:
                    print('No default namespace.')
                for record in root.iterfind('.//{%s}record' % nameSpace_default['oai_dc']):
                    PID = oai_dc_pid_search(record)
                    PID_present = 0
                    if record.find('.//{%s}mods' % nameSpace_default['mods']) is not None:
                        mods_root = record.find('.//{%s}mods' % nameSpace_default['mods'])
                        if mods_root.find('.//{%s}identifier' % nameSpace_default['mods']) is None:
                            new_identifier = etree.SubElement(mods_root, "{%s}identifier" % nameSpace_default['mods'], type="fedora")
                            new_identifier.text = PID
                            edit_record_count = edit_record_count + 1
                            pass 
                        elif mods_root.find('.//{%s}identifier' % nameSpace_default['mods']) is not None:
                            for identifier in mods_root.iterfind('.//{%s}identifier' % nameSpace_default['mods']):
                                if len(identifier.attrib) == 0:
                                    pass
                                elif len(identifier.attrib) >= 1:
                                    if "type" in identifier.attrib.keys():
                                        if "fedora" in identifier.attrib["type"]:
                                            PID_present = 1
                            if PID_present != 1:
                                new_identifier = etree.SubElement(mods_root, "{%s}identifier" % nameSpace_default['mods'], type="fedora")
                                new_identifier.text = PID
                                edit_record_count = edit_record_count + 1
                out_file.write(etree.tostring(root, pretty_print=True,
                                                     xml_declaration=True,
                                                     encoding="UTF-8",
                                                     standalone=False).decode('utf-8'))
        
            # exportedRecords root file
            elif 'exportedRecords' in root.tag:
                for record in root.iterfind('.//{%s}record' % nameSpace_default['repox']):
                    PID = repox_pid_search(record)
                    PID_present = 0
                    if record.find('.//{%s}mods' % nameSpace_default['mods']) is not None:
                        mods_root = record.find('.//{%s}mods' % nameSpace_default['mods'])
                        if mods_root.find('.//{%s}identifier' % nameSpace_default['mods']) is None:
                            new_identifier = etree.SubElement(mods_root, "{%s}identifier" % nameSpace_default['mods'], type="fedora")
                            new_identifier.text = PID
                            edit_record_count = edit_record_count + 1
                            pass 
                        elif mods_root.find('.//{%s}identifier' % nameSpace_default['mods']) is not None:
                            for identifier in mods_root.iterfind('.//{%s}identifier' % nameSpace_default['mods']):
                                if len(identifier.attrib) == 0:
                                    pass
                                elif len(identifier.attrib) >= 1:
                                    if "type" in identifier.attrib.keys():
                                        if "fedora" in identifier.attrib["type"]:
                                            PID_present = 1
                            if PID_present != 1:
                                new_identifier = etree.SubElement(mods_root, "{%s}identifier" % nameSpace_default['mods'], type="fedora")
                                new_identifier.text = PID
                                edit_record_count = edit_record_count + 1
                out_file.write(etree.tostring(root, pretty_print=True,
                                                     xml_declaration=True,
                                                     encoding="UTF-8",
                                                     standalone=False).decode('utf-8'))
            elif 'oai' in root.tag:
                for record in root.iterfind('{*}record'):
                    oai_id = record.find('{*}header/{*}identifier')
                    PID = oai_id.text.split(':')[-1].replace('_',':')
                                 
                    PID_present = 0
                    if record.find('.//{%s}mods' % nameSpace_default['mods']) is not None:
                        mods_root = record.find('.//{%s}mods' % nameSpace_default['mods'])
                        if mods_root.find('.//{%s}identifier' % nameSpace_default['mods']) is None:
                            new_identifier = etree.SubElement(mods_root, 
                                    "{%s}identifier" % nameSpace_default['mods'], 
                                    type="fedora")
                            new_identifier.text = PID
                            edit_record_count = edit_record_count + 1
                            pass 
                        elif mods_root.find('.//{%s}identifier' % nameSpace_default['mods']) is not None:
                            for identifier in mods_root.iterfind('.//{%s}identifier' % nameSpace_default['mods']):
                                if len(identifier.attrib) == 0:
                                    pass
                                elif len(identifier.attrib) >= 1:
                                    if "type" in identifier.attrib.keys():
                                        if "fedora" in identifier.attrib["type"]:
                                            PID_present = 1
                            if PID_present != 1:
                                new_identifier = etree.SubElement(mods_root, 
                                        "{%s}identifier" % nameSpace_default['mods'], 
                                        type="fedora")
                                new_identifier.text = PID
                                edit_record_count = edit_record_count + 1
                out_file.write(etree.tostring(root, pretty_print=True,
                                                     xml_declaration=True,
                                                     encoding="UTF-8",
                                                     standalone=False).decode('utf-8'))
                    
    
    if '.backup' not in os.listdir():
        os.mkdir('.backup')
    os.rename(os.path.abspath(input_file), os.path.join(os.path.split(input_file)[0], '.backup', os.path.split(input_file)[-1]))
    os.rename(os.path.abspath(input_file) + '.tmp', os.path.abspath(input_file)) 
    print("\nComplete:\n\n" + str(edit_record_count), "records edited.\n")          
    
                
