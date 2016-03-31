#!/usr/bin/env python3

from lxml import etree
from functools import partial
import os
import sys
import hashlib
import datetime
import argparse

def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()
    
def get_file_size(filename):
    statinfo = os.stat(filename)
    return statinfo.st_size

def buildMETS(directory, agent_dict):
    NS = { 'mets' : 'http://www.loc.gov/METS/', 'mods': 'http://www.loc.gov/mods/v3',
            'xlink' : 'http://www.w3.org/1999/xlink'}
    with open(directory + '/' + 'mets.xml', 'w') as METSout:
        root = etree.Element("{%s}mets" % NS['mets'], OBJID=directory)
        metsHdr = etree.SubElement(root, "{%s}metsHdr" % NS['mets'], 
                                    ID=directory,
                                    RECORDSTATUS="COMPLETE", 
                                    CREATEDATE=datetime.datetime.isoformat(datetime.datetime.now()),
                                    LASTMODDATE=datetime.datetime.isoformat(datetime.datetime.now()))
        for type, individual in agent_dict.items():
            agent = etree.SubElement(metsHdr, "{%s}agent" % NS['mets'], 
                                    ROLE="CREATOR",
                                    TYPE=type)
# fix these two lines - interpretting str as int                                      
#            if agent['TYPE'] == 'OTHER':
#                agent['OTHERTYPE'] = "SOFTWARE"
            name = etree.Element("{%s}name" % NS['mets'])
            name.text = individual
            agent.append(name)
        dmdSec = etree.SubElement(root, "{%s}dmdSec" % NS['mets'])
        # copy MODS here
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
        for image in os.listdir(directory):
            fileIndex = str(os.listdir(directory).index(image) + 1)
            file = etree.SubElement(fileGrp, "{%s}file" % NS['mets'], 
                                        GROUPID="G" + fileIndex,
                                        ID="TIF" + fileIndex,
                                        MIMETYPE="image/tiff",
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

        #root.set('xmlns:METS', 'http://www.loc.gov/METS/')
        METSout.write(etree.tostring(root, pretty_print=True).decode('utf-8'))
        
        
agent_dict = { 'ORGANIZATION' : 'FSU,Florida State University', 'OTHER' : 'METScreate.py by FSU Libraries' }
parser = argparse.ArgumentParser()
parser.add_argument('directory', help='directory containing files to be used in creating the METS document') 
parser.add_argument('-a', '--agent', help='FSUID of the individual running this program')
args = parser.parse_args()
agent_dict['INDIVIDUAL'] = "FSU/" + args.agent
buildMETS(args.directory, agent_dict)