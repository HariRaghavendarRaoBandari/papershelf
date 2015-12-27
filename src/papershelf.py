#!/usr/bin/python

import argparse
import os
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
args = parser.parse_args()

class PaperShelf(item):
    def __init__(self):
        self.database_dir = ''
        self.storage_dir = ''
        self.areas = ['computer science']

    def configure(self, database_dir, storage_dir):
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
        else:
            print 'database dir <{}> does not exist'.format(str(database_dir or ''))

        if os.path.exists(str(storage_dir or '')) == True:
            self.storage_dir = storage_dir
            tmp_storage = 'STORAGE_DIR = ' + storage_dir + '\n'
        else:
            print 'storage dir <{}> does not exist'.format(str(storage_dir or ''))

        with open('.config', 'w') as f:
            f.write(tmp_database)
            f.write(tmp_storage)

    def add(self, area, field, subfield, problem, 
            name, title, year, conference, description):
        print "add papershelf"

    def remove(self, area, field, subfield, problem, name):
        print "remove papershelf"

    def show(self, area, field, subfield, problem, name):
        print "show papershelf"

if __name__ == "__main__":
    allshelf = PaperShelf()

    if args.command == 'configure':
        allshelf.configure(args.database, args.storage)
    elif args.command == 'add':
        allshelf.add(args.area, args.field, args.subfield, args.problem, 
                     args.name, args.title, args.year, args.conference, args.description)
    elif args.command == 'remove':
        allshelf.remove(args.area, args.field, args.subfield, 
                        args.problem, args.name)
    else:
        allshelf.show(args.area, args.field, args.subfield, 
                      args.problem, args.name)

    print 'Thanks for using papershelf v0.1 :D'
