import os
import sys

def clean(in_directory):
    for in_file in os.listdir(in_directory):
        with open(in_directory + '/' + in_file + 'out', 'w') as out_file:
            for line in open(in_directory + '/' + in_file, 'r'):
                if 'mods:mods' in line:
                    out_file.write(line)
                else:
                    out_file.write(line.replace('mods:',''))
