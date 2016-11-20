### Metadata Workflow Resources
#### For FSU University Libraries
These are tools developed by the Metadata Librarian at Florida State University, University Libraries. They are intended to ease the creation of metadata for [Florida State University's DigiNole](http://fsu.digital.flvc.org). All are released with MIT licenses.

This repo is under frequent development.

#### csv4cat

csv4cat is a simple python3 script for generating the spreadsheets shared with Cataloging for the creation of MARC records. An additional function creates collection content CSVs for digital series in Archon.

#### Plow
Plow is a metadata reporting tool utilizing the digital library's OAI-PMH feed for harvest. Basic analysis of the DL's description is reported in an CSV.
Plow and plowReport make use of two tools developed by Mark Phillips:
* pyoaiharvester
* metadata_breakers.

Both are available at his [Github account](https://guthub.com/vphill).

The utility xmlstarlet is also required.

#### pullTags

#### Sysnum
Sysnum is a basic shell script that generates an Aleph-friendly string of system numbers for easy record export from the catalog.

#### XSLT
The XSLT folder contains eXtensible Stylesheets for transforming XML as it moves through various metadata workflows. Description of each file's function is recorded in the file's source code.

#### Scripts

##### addFragment
Appends the children of root in an XML file to a targeted MODSXML file.

##### addNames
Identical to addFragment.

##### addURI
Updates Research Repository records with subject terms stored as keywords with controlled subject terms and URIs from the id.loc.gov interface.

##### appendPID
Add PIDs to objects loaded via the Islandora ZIP loader which does not append PIDs to records at load.

##### collectRecords
_in process_

##### IIDtoPID
Renames _IID_.xml to _PID_.xml

##### METScreate
Creates METS documents for newspaper objects and packages them with TIFFs and MODS for ingest into DigiNole.

##### pidsWithNoLocation
QA tool for identifying objects by PID without `.//mods:physicalLocation` elements.

##### pullObjects
Preservation tool for DigiNole ETDs & faculty publications. Harvests all necessary datastreams from DigiNole for packaging for preservation ingests.

##### pullRecords
Downloads local copies of MODS datastreams for editing.

##### renameByPID
Rename files by _PID_.xml.