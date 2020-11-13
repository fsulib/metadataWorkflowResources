### Metadata Workflow Resources
#### For FSU University Libraries
These are tools developed by the Metadata Librarian at Florida State University, University Libraries. They are intended to ease the creation of metadata for [Florida State University's DigiNole](http://fsu.digital.flvc.org). All are released with MIT licenses.

This repo is under frequent development. It's probably best to think of this as a training space and testing ground for ideas, or the scripts might be one-off solutions to problems. Some ideas might be repackaged as stand-alone utilities:
* [pymods](https://github.com/mrmiguez/pymods)

#### addFragment 
_python3_

Appends the children of root in an XML snippet to a targeted MODSXML file.

#### addNames
_python3_

Identical to addFragment.

#### addURI
_python3_

Updates Research Repository records with subject terms stored as keywords with controlled subject terms and URIs from the id.loc.gov interface.

#### appendPID
_python3_

Add PIDs to objects loaded via the Islandora ZIP loader which does not append PIDs to records at load.

#### assets
* clean-up - python3 utility for managing some XML namespace prefix issues
* hpLocationFragment - `mods:physicalLocation` XML snippet
* lc_vacab - python3 utilities for querying and parsing id.loc.gov for controlled subject terms and URIs, appending the results to a MODSXML document, and writing out the modified file
* oaiDefaultNamespace - `sed` pattern for adding default OAI-PMH namespace to OAI-PMH harvested XML
* pymods _depreciated_ - python3 utility bundle for working with MODSXML
* SpCLocationFragment - `mods:physicalLocation` XML snippet

#### collectRecords
_python3_

_in process_ Utility to parse MODS files out into appropriate object directory structure for ingest packaging.

#### csv4cat
_python3_

csv4cat is a simple python3 script for generating the spreadsheets shared with Cataloging for the creation of MARC records. An additional function creates collection content CSVs for digital series in Archon.

#### digiLibComplexLCSH
_python3_

Queries `mods:subject @authority='lcsh'` values against id.loc.gov for linked data attributes and updates the records. Can parse out complex subject terms using LCSH double-hyphen delimination and bundle terms in appropriate mods subject types.  

#### IIDtoPID
_python3_

Renames _IID_.xml to _PID_.xml

#### METScreate
_python3_

Creates METS documents for newspaper objects and packages them with TIFFs and MODS for ingest into DigiNole.

#### personagraphyCSV
_python3_

#### pidsWithNoLocation_local
_python3_

QA tool for identifying objects by PID without `.//mods:physicalLocation` elements. Takes local OAI-PMH document as input.

#### pidsWithNoLocation
_python3_

QA tool for identifying objects by PID without `.//mods:physicalLocation` elements. Queries DigiNole's OAI-PMH feed.

#### Plow
_shell script & python_

Plow is a metadata reporting tool utilizing the digital library's OAI-PMH feed for harvest. Basic analysis of the DL's description is reported in an CSV.
Plow and plowReport make use of two tools developed by Mark Phillips:
* pyoaiharvester
* metadata_breakers.

Both are available at his [Github account](https://guthub.com/vphill).

The utility xmlstarlet is also required.

#### pullObjects
_python3_

Preservation tool for DigiNole ETDs & faculty publications. Harvests all necessary datastreams from DigiNole for packaging for preservation ingests.

#### pullRecords
_python3_

Downloads local copies of MODS datastreams for editing.

#### pullTags

See separate [README](pullTags/README.md).

#### pyoaiharvester
_python2_

Copy of [Mark Phillips'](https:github.com/vphill) [pyoaiharvester](https://github.com/vphill/pyoaiharvester).

#### renameByPID
_python3_

Rename files by _PID_.xml.

#### Sysnum
Sysnum is a basic shell script that generates an Aleph-friendly string of system numbers for easy record export from the catalog.

#### XSLT
The XSLT folder contains eXtensible Stylesheets for transforming XML as it moves through various metadata workflows.
* alephtoMODS - modified version of LC's MARCXML to MODS transformation
* assets - files needed other XSLT documents
* inc - files used by LC's transformations
* langEdit - find and `mods:language @type="term"` for matching `mods:languageTerm @type="code"` within MODS document
* LCtransformations - XSLT published by the Library of Congress
* multiOutAleph - split out individual MODS files from MODScollection document generated from MARCXML process
* multiOutMODSOAI - split out individual MODS files from OAI-PMH harvest
* multiOutORefinePIDS - split out individual MODS files from MODScollection document generated from OpenRefine process. Name files by PID rather than IID. 
* multiOutORefine-splitOnFilename - split out individual MODS files from MODScollection document generated from OpenRefine process. Name files to match source object filename rather than IID.
* multiOutORefine - split out individual MODS files from MODScollection document generated from OpenRefine process
* omekaDC-RDF - 
* stripEmptyElements01 - clean up empty elements and attributes
* stripEmptyElements02 - clean up remaining empty elements
* stripFilenameIdentifier - 
* stripLocationFromPURLs - 
* stripQuotes - 
