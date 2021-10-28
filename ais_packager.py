#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from zipfile import ZipFile

PATH = Path.cwd()


class PackagerError(ValueError):

    def __init__(self, k):
        self.msg = f'Value {k} is not supplied'
        ValueError.__init__(self, self.msg)


def zip_it_up(package_dir):
    # zip the stuff
    with ZipFile(os.path.join(PATH, f'{package_dir.name}.zip'), 'w') as zp:
        for f in os.listdir(package_dir):
            if '.zip' not in f:
                zp.write(os.path.join(package_dir, f), arcname=f)
    print(f'\n{package_dir.name}.zip written')


def manifest(email, cmodel, parent, obj_dir):
    if not email:
        raise PackagerError('\"email address\"')

    if not cmodel:
        raise PackagerError('\"content model\"')

    if not parent:
        raise PackagerError('\"parent collection\"')

    with open(os.path.join(obj_dir, 'manifest.ini'), 'w') as manifest_file:
        manifest_file.write(f'[{obj_dir.name}]')
        manifest_file.write(f'\nsubmitter_email = {email}')
        manifest_file.write(f'\ncontent_model = {cmodel}')
        manifest_file.write(f'\nparent_collection = {parent}')

    print(f'\nManifest written for {obj_dir.name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Package books or newspapers for DigiNole\'s AIS')
    parser.add_argument('-e', '--email', help='Submitter email')
    parser.add_argument('-c', '--cmodel', help='Content model',
                        choices=['islandora:newspaperIssueCModel', 'islandora:bookCModel'])
    parser.add_argument('-p', '--parent', help='Parent collection')
    parser.add_argument('-z', '--zip', action='store_true',
                        help='Zip directory when finished?')
    parser.add_argument('dir', help='Directory to work in')
    args = parser.parse_args()

    p = Path(args.dir)
    obj_dirs = [f.resolve() for f in p.iterdir() if f.is_dir()]
    if not obj_dirs:
        obj_dirs = [p.resolve()]

    for obj in obj_dirs:
        manifest(args.email, args.cmodel, args.parent, obj)
        if args.zip:
            zip_it_up(obj)

    print('\nAll done.')
    sys.exit()
