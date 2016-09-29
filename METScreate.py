#!/usr/bin/env python3

import os
import sys
import hashlib
import datetime
import argparse
import logging
import mimetypes
import shutil
from lxml import etree
from functools import partial


# get titles from MODS record
def mods_title_generator(mods_record, nameSpace_dict):
    allTitles = []
    for title in mods_record.iterfind('.//{%s}titleInfo' % nameSpace_dict['mods']):
        if title.find('./{%s}nonSort' % nameSpace_dict['mods']) is not None and title.find(
                        './{%s}title' % nameSpace_dict['mods']) is not None and title.find(
                    './{%s}subTitle' % nameSpace_dict['mods']) is not None:
            titleFull = title.find('./{%s}nonSort' % nameSpace_dict['mods']).text + ' ' + title.find(
                './{%s}title' % nameSpace_dict['mods']).text + ': ' + title.find(
                './{%s}subTitle' % nameSpace_dict['mods']).text
        elif title.find('./{%s}nonSort' % nameSpace_dict['mods']) is not None and title.find(
                        './{%s}title' % nameSpace_dict['mods']) is not None:
            titleFull = title.find('./{%s}nonSort' % nameSpace_dict['mods']).text + ' ' + title.find(
                './{%s}title' % nameSpace_dict['mods']).text
        else:
            titleFull = title.find('./{%s}title' % nameSpace_dict['mods']).text
        allTitles.append(titleFull)
        return ' || '.join(allTitles)


# logger to catch missing MODS files
def testForMODS(directory):
    logging.basicConfig(filename='METScreateErrorLog.txt', level=logging.ERROR,
                        format='%(asctime)s -- %(levelname)s : %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S %p')


# build manifest file
def buildManifest(directory, user, target_collection):
    print('Building manifest for ' + directory + '.\n')
    NS = {None: "info:flvc/manifest"}
    with open(directory + '.manifest.xml', 'w') as manifestOut:
        root = etree.Element('manifest', nsmap=NS)
        contentModel = etree.SubElement(root, 'contentModel')
        collection = etree.SubElement(root, 'collection')
        owningUser = etree.SubElement(root, 'owningUser')
        owningInstitution = etree.SubElement(root, 'owningInstitution')
        contentModel.text = 'islandora:newspaperIssueCModel'
        collection.text = target_collection
        owningUser.text = user
        owningInstitution.text = 'FSU'
        manifestOut.write(etree.tostring(root, pretty_print=True,
                                         xml_declaration=True,
                                         encoding="UTF-8").decode('utf-8'))


# hashes image with MD5 hash
def md5sum(filename):
    print('Hashing ' + filename)
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()


# checks image file size
def get_file_size(filename):
    statinfo = os.stat(filename)
    return statinfo.st_size


# main function - builds & serializes the METS tree
def buildMETS(directory, agent_dict):
    print('Building METS for ' + directory + '.\n')
    if 'Thumbs.db' in os.listdir(directory):
        print('Cleaning directory')
        os.remove(directory + '/Thumbs.db')
    NS = {None: 'http://www.loc.gov/METS/', 'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3',
          'xlink': 'http://www.w3.org/1999/xlink',
          'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    with open(directory + '.mets.xml', 'w') as METSout:
        root = etree.Element("{%s}mets" % NS['mets'],
                             OBJID=directory, nsmap=NS)
        root.attrib[
            '{%s}schemaLocation' % NS['xsi']] = "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd"
        metsHdr = etree.SubElement(root, "{%s}metsHdr" % NS['mets'],
                                   ID=directory,
                                   RECORDSTATUS="COMPLETE",
                                   CREATEDATE=datetime.datetime.isoformat(datetime.datetime.now()),
                                   LASTMODDATE=datetime.datetime.isoformat(datetime.datetime.now()))
        # add agents to metsHdr
        for type, individual in agent_dict.items():
            agent = etree.SubElement(metsHdr, "{%s}agent" % NS['mets'],
                                     ROLE="CREATOR",
                                     TYPE=type)
            if agent.get('TYPE') == 'OTHER':
                agent.set('OTHERTYPE', 'SOFTWARE')
            name = etree.Element("{%s}name" % NS['mets'])
            name.text = individual
            agent.append(name)
        # copy in MODS descriptive metadata
        dmdSec = etree.SubElement(root, "{%s}dmdSec" % NS['mets'],
                                  ID="DMD1")
        mdWrap = etree.SubElement(dmdSec, "{%s}mdWrap" % NS['mets'],
                                  MDTYPE="MODS",
                                  MIMETYPE="text/xml",
                                  LABEL="MODS metadata")
        xmlData = etree.SubElement(mdWrap, "{%s}xmlData" % NS['mets'])
        try:
            with open('MODS/' + directory + '.xml', 'r') as modsFile:
                modsTree = etree.parse(modsFile)
                modsRoot = modsTree.getroot()
                mods_title = mods_title_generator(modsRoot, NS).split(' || ')[0]
                xmlData.append(modsRoot)
        except FileNotFoundError:
            logging.error('No MODS for ' + directory + ' when building manifest.')
        # build fileSec & structMap parents for iterative children
        fileSec = etree.SubElement(root, "{%s}fileSec" % NS['mets'])
        fileGrp = etree.SubElement(fileSec, "{%s}fileGrp" % NS['mets'],
                                   USE="archive")
        structMap = etree.SubElement(root, "{%s}structMap" % NS['mets'],
                                     ID="STRUCT1",
                                     TYPE="physical")
        div1 = etree.SubElement(structMap, "{%s}div" % NS['mets'],
                                DMDID="DMD1",
                                LABEL=mods_title,
                                ORDER="0",
                                TYPE="main")
        div2 = etree.SubElement(div1, "{%s}div" % NS['mets'],
                                ID="PDIV1",
                                ORDER="1",
                                TYPE="Main")
        # loop over files in directory & build fileSec & structMap children
        for image in sorted(os.listdir(directory)):
            fileIndex = str(sorted(os.listdir(directory)).index(image) + 1)
            file = etree.SubElement(fileGrp, "{%s}file" % NS['mets'],
                                    GROUPID="G" + fileIndex,
                                    ID="TIF" + fileIndex,
                                    MIMETYPE=mimetypes.guess_type(image)[0],
                                    CHECKSUM=md5sum(directory + "/" + image),
                                    CHECKSUMTYPE="MD5",
                                    SIZE=str(get_file_size(directory + "/" + image)))
            FLocat = etree.SubElement(file, "{%s}FLocat" % NS['mets'],
                                      LOCTYPE="OTHER",
                                      OTHERLOCTYPE="SYSTEM")
            div3 = etree.SubElement(div2, "{%s}div" % NS['mets'],
                                    ID="PAGE" + fileIndex,
                                    LABEL="Page " + fileIndex,
                                    ORDER=fileIndex,
                                    TYPE="Page")
            fptr = etree.SubElement(div3, "{%s}fptr" % NS['mets'],
                                    FILEID="TIF" + fileIndex)
            FLocat.set('{%s}href' % NS['xlink'], image)

        METSout.write(etree.tostring(root, pretty_print=True,
                                     xml_declaration=True,
                                     encoding="UTF-8",
                                     standalone=False).decode('utf-8'))


agent_dict = {'ORGANIZATION': 'FSU, Florida State University', 'OTHER': 'METScreate.py by FSU Libraries'}
# argument inputs
logging.basicConfig(filename='METScreateErrorLog.txt', level=logging.ERROR,
                    format='%(asctime)s -- %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')
parser = argparse.ArgumentParser(description="Builds newspaper ingest packages for FSUDL.")
parser.add_argument('directory', help='directory containing files to be used in creating the METS document')
parser.add_argument('-c', '--collection',
                    required=True, help='PID of digital collection target for package')
parser.add_argument('-f', '--FSUDL_login',
                    required=True, help='your FSUDL login name')
parser.add_argument('-m', '--manifest', choices=['y', 'n'],
                    default='y', help='build package manifest')
parser.add_argument('-z', '--zip', choices=['y', 'n'],
                    default='n', help='zip completed package')
args = parser.parse_args()

if args.directory[-1] == '/':
    args.directory = args.directory[:-1]
if args.collection[0:4] != 'fsu:':
    args.collection = 'fsu:' + args.collection
agent_dict['INDIVIDUAL'] = "FSU/" + os.getlogin()
buildMETS(args.directory, agent_dict)
if args.manifest == 'y':
    buildManifest(args.directory, args.FSUDL_login, args.collection)
    shutil.move(args.directory + '.manifest.xml', args.directory + '/manifest.xml')
shutil.move(args.directory + '.mets.xml', args.directory + '/mets.xml')
try:
    shutil.move('MODS/' + args.directory + '.xml', args.directory + '/' + args.directory + '.xml')
except FileNotFoundError:
    logging.error('No MODS for ' + args.directory + ' when moving MODS.')
if args.zip == 'y':
    shutil.make_archive(args.directory, 'zip', args.directory)
print(args.directory + ' fully packaged.\n')
