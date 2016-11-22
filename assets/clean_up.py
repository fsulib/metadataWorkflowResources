import os
import sys
import glob
import shutil

def clean(in_directory):
    for in_file in os.listdir(in_directory):
        with open(in_directory + '/' + in_file + 'out', 'w') as out_file:
            for line in open(in_directory + '/' + in_file, 'r'):
                if 'mods:mods' in line:
                    out_file.write(line)
                else:
                    out_file.write(line.replace('mods:',''))
    if '.backup' not in os.listdir(in_directory):
        os.mkdir(in_directory + '.backup')
    for file in glob.glob(in_directory + '*.xml'):
        shutil.move(file, in_directory + '.backup/')
    for file in glob.glob(in_directory + '*.xmlout'):
        shutil.move(file, os.path.splitext(file)[0] + '.xml')