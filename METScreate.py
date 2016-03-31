#!/usr/bin/env python3

import os
import sys
import hashlib
import datetime
import argparse
import mimetypes
import shutil
from lxml import etree
from functools import partial

#hashes image with MD5 hash
def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()
    
#checks image file size
def get_file_size(filename):
    statinfo = os.stat(filename)
    return statinfo.st_size

#main function - builds & serializes the METS tree
def buildMETS(directory, agent_dict):
    print('Building METS for ' + directory + '.\n')
    NS = { 'mets' : 'http://www.loc.gov/METS/', 'mods': 'http://www.loc.gov/mods/v3',
            'xlink' : 'http://www.w3.org/1999/xlink',
            'xsi' : 'http://www.w3.org/2001/XMLSchema-instance' }
    with open(directory + '.' + 'mets.xml', 'w') as METSout:
        root = etree.Element("{%s}mets" % NS['mets'], OBJID=directory)
        metsHdr = etree.SubElement(root, "{%s}metsHdr" % NS['mets'], 
                                    ID=directory,
                                    RECORDSTATUS="COMPLETE", 
                                    CREATEDATE=datetime.datetime.isoformat(datetime.datetime.now()),
                                    LASTMODDATE=datetime.datetime.isoformat(datetime.datetime.now()))
        #add agents to metsHdr
        for type, individual in agent_dict.items():
            agent = etree.SubElement(metsHdr, "{%s}agent" % NS['mets'], 
                                    ROLE="CREATOR",
                                    TYPE=type)                                      
            if agent.get('TYPE') == 'OTHER':
                agent.set('OTHERTYPE', 'SOFTWARE')
            name = etree.Element("{%s}name" % NS['mets'])
            name.text = individual
            agent.append(name)
        #copy in MODS descriptive metadata
        dmdSec = etree.SubElement(root, "{%s}dmdSec" % NS['mets'])
        mdWrap = etree.SubElement(dmdSec, "{%s}mdWrap" % NS['mets'],
                                    MDTYPE="MODS",
                                    MIMETYPE="text/xml",
                                    LABEL="MODS metadata")
        xmlData = etree.SubElement(mdWrap, "{%s}xmlData" % NS['mets'])                                        
        with open('MODS/' + directory + '.xml') as modsFile:
            modsTree = etree.parse(modsFile)
            modsRoot = modsTree.getroot()
            xmlData.append(modsRoot)
        #build fileSec & structMap parents for iterative children 
        fileSec = etree.SubElement(root, "{%s}fileSec" % NS['mets'])
        fileGrp = etree.SubElement(fileSec, "{%s}fileGrp" % NS['mets'], 
                                    USE="archive")
        structMap = etree.SubElement(root, "{%s}structMap" % NS['mets'], 
                                    ID="STRUCT1", 
                                    TYPE="physical")
        div1 = etree.SubElement(structMap, "{%s}div" % NS['mets'],
                                    DMDID="DMD1",
                                    LABEL="temp",
                                    ORDER="0",
                                    TYPE="main")
        div2 = etree.SubElement(div1, "{%s}div" % NS['mets'],
                                    ID="PDIV1",
                                    ORDER="1",
                                    TYPE="Main")                                     
        #loop over files in directory & build fileSec & structMap children
        for image in os.listdir(directory):
            fileIndex = str(os.listdir(directory).index(image) + 1)
            file = etree.SubElement(fileGrp, "{%s}file" % NS['mets'], 
                                        GROUPID="G" + fileIndex,
                                        ID="TIF" + fileIndex,
                                        MIMETYPE=mimetypes.guess_type(image)[0],
                                        CHECKSUM=md5sum(directory + "/" + image),
                                        CHECKSUMTYPE="MD5",
                                        SIZE=str(get_file_size(directory + "/" + image)))
            FLocat = etree.SubElement(file, "{%s}FLocat" % NS['mets'],
                                        LOCTYPE="OTHER",
                                        OTHYERLOCTYPE="SYSTEM")
            div3 = etree.SubElement(div2, "{%s}div" % NS['mets'],
                                        ID="PAGE" + fileIndex,
                                        ORDER=fileIndex,
                                        TYPE="Page")
            fptr = etree.SubElement(div3, "{%s}div" % NS['mets'],
                                        FILEID="TIF" + fileIndex)
            FLocat.set('{%s}href' % NS['xlink'], image)                            

        METSout.write(etree.tostring(root, pretty_print=True, xml_declaration=True).decode('utf-8'))
        
        
agent_dict = { 'ORGANIZATION' : 'FSU, Florida State University', 'OTHER' : 'METScreate.py by FSU Libraries' }

parser = argparse.ArgumentParser()
parser.add_argument('directory', help='directory containing files to be used in creating the METS document') 
parser.add_argument('-a', '--agent', help='FSUID of the individual running this program')
args = parser.parse_args()
agent_dict['INDIVIDUAL'] = "FSU/" + args.agent

buildMETS(args.directory, agent_dict)

shutil.move(args.directory + '.mets.xml', args.directory + '/mets.xml')
shutil.copy('MODS/' + args.directory + '.xml', args.directory + '/' + args.directory + '.xml')
print(args.directory + ' fully packaged.\n')