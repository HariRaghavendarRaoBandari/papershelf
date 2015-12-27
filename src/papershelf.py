#!/usr/bin/python

import argparse
import os
import logging
from item import *

parser = argparse.ArgumentParser(description = 'A simple paper organization tool',
				 formatter_class = argparse.RawTextHelpFormatter)
parser.add_argument("command", choices = ['configure', 'add', 'remove', 'show'],
		    help = 'Four commands supported by papershelf\n'
		           'Options supported by configure: -shelf -storage\n'
			   'Options supported by add:-a -f -s -p -n -t -y -c -d\n'
			   'Options supported by remove: -a -f -s -p -n\n'
			   'Options supported by show: -a -f -s -p -n\n')
parser.add_argument('--database',
		    help = 'Directory saving the papershelf database')
parser.add_argument('--storage',
		    help = 'Directory saving all recorded papers')
parser.add_argument('-a', '--area', default = 'computer science',
		    help = 'Research area in the specified papershelf')
parser.add_argument('-f', '--field',
		    help = 'Field in the specified research area')
parser.add_argument('-s', '--subfield',
                    help = 'Subfield in the specified field')
parser.add_argument('-p', '--problem',
		    help = 'Problem in the subfiled')
parser.add_argument('-n', '--name',
                    help = 'Paper file name')
parser.add_argument('-t', '--title',
		    help = 'Paper title')
parser.add_argument('-y', '--year', type = int,
		    help = 'Paper published year')
parser.add_argument('-c', '--conference',
		    help = 'Paper published conference/journal/others')
parser.add_argument('-d', '--description',
		    help = 'Write some important notes')
parser.add_argument('-v', '--verbosity', action = 'count', default = 0,
                    help = 'increase output verbosity')
args = parser.parse_args()

class PaperShelf(item):
    def __init__(self):
        self.database_dir = ''
        self.storage_dir = ''
        self.areas = ['computer science']

    def configure(self, database_dir, storage_dir, verbosity):
        """Configure papershelf database_dir and storage_dir

        """
        tmp_database = ''
        tmp_storage = ''

        if os.path.exists('.config') == True:
            with open('.config', 'r') as f:
                for line in f:
                    if 'DATABASE_DIR' in line.split():
                        tmp_database = line
                    if 'STORAGE_DIR' in line.split():
                        tmp_storage = line

        if os.path.exists(str(database_dir or '')) == True:
            self.database_dir = database_dir
            tmp_database = 'DATABASE_DIR = ' + database_dir + '\n'
            if verbosity >= 1:
                print 'database dir <{}> has been updated.'.format(
                str(database_dir or ''))
        else:
            if verbosity >= 1:
                print 'database dir <{}> does not exist.'.format(
                str(database_dir or ''))

        if os.path.exists(str(storage_dir or '')) == True:
            self.storage_dir = storage_dir
            tmp_storage = 'STORAGE_DIR = ' + storage_dir + '\n'
            if verbosity >= 1:
                print 'storage dir <{}> has been updated.'.format(
                str(storage_dir or ''))
        else:
            if verbosity >= 1:
                print 'storage dir <{}> does not exist'.format(
                str(storage_dir or ''))

        with open('.config', 'w') as f:
            f.write(tmp_database)
            f.write(tmp_storage)
            self.add_log('configure {}'.format(tmp_database.replace('\n', '')))
            self.add_log('configure {}'.format(tmp_storage.replace('\n', '')))

    def add(self, area, field, subfield, problem, 
            name, title, year, conference, description, verbosity):
        """Add papershelf info based on input parameters (i.e. area, field, etc.)

        """
        print "add papershelf"

    def remove(self, area, field, subfield, problem, name, verbosity):
        """Remove papershelf info based on input parameters (i.e. area, field, etc.)

        """
        print "remove papershelf"

    def show(self, area, field, subfield, problem, name, verbosity):
        """Show papershelf info based on input parameters (i.e. area, field, etc.)

        """
        print "show papershelf"

if __name__ == "__main__":
    logging.basicConfig(filename='.papershelf.log', format='%(asctime)s %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p', 
                        level = logging.INFO)
    logging.info('Started this transaction')

    allshelf = PaperShelf()

    if args.command == 'configure':
        allshelf.configure(args.database, args.storage, args.verbosity)
    elif args.command == 'add':
        allshelf.add(args.area, args.field, args.subfield, args.problem,
                     args.name, args.title, args.year, args.conference, 
                     args.description, args.verbosity)
    elif args.command == 'remove':
        allshelf.remove(args.area, args.field, args.subfield, args.problem,
                        args.name, args.verbosity)
    else:
        allshelf.show(args.area, args.field, args.subfield, args.problem,
                      args.name, args.verbosity)

    logging.info('Finished this transaction')

    print 'Thanks for using papershelf v0.1 :D'
