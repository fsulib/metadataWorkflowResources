#!/usr/bin/env python3

import os
import shutil
import sys
import glob

path = sys.argv[1]
for directory in glob.glob( path + 'FSU*'):
    if os.path.isdir( directory) == True:
        shutil.move('MODS/' +  directory.split('/')[1] + '.xml', path + 'MODS/' + directory.split('/')[1] + '.xml')
        
