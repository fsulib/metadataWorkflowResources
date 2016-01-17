#!/usr/bin/env python3

import os
import sys

name = os.path.splitext(sys.argv[1])[0]
eggs = sys.argv[2]

os.system('../pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -s {0} -o {1}'.format(name, name + '.xml'))
