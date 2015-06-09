### Metadata Workflow Resources
#### For FSU University Libraries
These are tools developed my the Metadata Librarian at Florida State University, University Libraries. They are intended to ease the creation of metadata for [Florida State University's Digital Library](http://fsu.digital.flvc.org). All are released with MIT licenses.

#### Plow
Plow is a metadata reporting tool utilizing the digital library's OAI-PMH feed for harvest. Basic analysis of the DL's description is reported in an CSV.
Plow and plowReport make use of two tools developed by Mark Phillips:
* pyoaiharvester
* metadata_breakers.

Both are available at his [Github account](https://guthub.com/vphill).

The utility xmlstarlet is also required.

#### Sysnum
Sysnum is a basic shell script that generates an Aleph-friendly string of system numbers for easy record export from the catalog.

#### XSLT's
The XSLT folder contains eXtensible Stylesheets for transforming XML as it moves through various metadata workflows. Description of each file's function is recorded in the file's source code.

#### csv4cat
csv4cat is a simple python3 script for generating the spreadsheets shared with Cataloging for the creation of MARC records.
