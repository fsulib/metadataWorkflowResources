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


def zip_it_up(package, dir):
    # zip the stuff
    with ZipFile(os.path.join(PATH, f'{package}.zip'), 'w') as zp:
        for f in os.listdir(os.path.join(PATH, dir)):
            zp.write(os.path.join(PATH, dir, f), arcname=f)
    print(f'\n{package}.zip written')


def manifest(package_name, email, cmodel, parent, dir):
    # print(f'Package: {package_name},\nEmail: {email},\nCModel: {cmodel},\nParent: {parent}')

    if not package_name:
        raise PackagerError('\"package name\"')

    if not email:
        raise PackagerError('\"email address\"')

    if not cmodel:
        raise PackagerError('\"content model\"')

    if not parent:
        raise PackagerError('\"parent collection\"')

    with open(os.path.join(PATH, dir, 'manifest.ini'), 'w') as manifest_file:
        manifest_file.write(f'[{package_name}]')
        manifest_file.write(f'\nsubmitter_email = {email}')
        manifest_file.write(f'\ncontent_model = {cmodel}')
        manifest_file.write(f'\nparent_collection = {parent}')

    print('\nManifest written')


def interactive_run(*args, **kwargs):
    ### Interactive script

    if args[0].package_name:
        package_name = args[0].package_name
    else:
        package_name = input('Package name: ')

    if args[0].email:
        email = args[0].email
    else:
        email = input('\nEmail address: ')

    if args[0].cmodel:
        cmodel = args[0].cmodel
    else:
        print('\nWhat are you ingesting?\n'
              '1. Newspaper issue\n'
              '2. Book')
        cmodel_prompt = input('\nSelect 1 or 2: ')
        if cmodel_prompt == '1':
            cmodel = 'islandora:newspaperIssueCModel'
        elif cmodel_prompt == '2':
            cmodel = 'islandora:bookCModel'
        else:
            print(f'\nUnrecognized option "{cmodel_prompt}". Exiting.')
            sys.exit()

    if args[0].parent:
        parent = args[0].parent
    else:
        parent = input('\nParent collection PID: ')

    manifest(package_name, email, cmodel, parent, args[0].dir)
    if args[0].zip:
        zip_it_up(package_name, args[0].dir)
    else:
        print('\nReady to zip?\n')
        zip = input('Y/n\n')
        if zip == 'Y':
            zip_it_up(package_name, args[0].dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Package books or newspapers for DigiNole\'s AIS')
    parser.add_argument('-n', '--name', help='Package name', dest='package_name')
    parser.add_argument('-e', '--email', help='Submitter email')
    parser.add_argument('-c', '--cmodel', help='Content model',
                        choices=['islandora:newspaperIssueCModel', 'islandora:bookCModel'])
    parser.add_argument('-p', '--parent', help='Parent collection')
    parser.add_argument('-z', '--zip', action='store_true',
                        help='Zip directory when finished?')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Run packaging utility interactively')
    parser.add_argument('dir', help='Directory to work in')
    args = parser.parse_args()
    if args.interactive:
        interactive_run(args)
    else:
        manifest(args.package_name, args.email, args.cmodel, args.parent, args.dir)
        if args.zip:
            zip_it_up(args.package_name, args.dir)
    print('\nAll done.')
    sys.exit()
