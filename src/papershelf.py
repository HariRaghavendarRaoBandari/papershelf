#!/usr/bin/python

import argparse
import os
import logging
import shutil
import settings
from shelf import *
from item import *

parser = argparse.ArgumentParser(description = 'A simple paper organization tool',
				 formatter_class = argparse.RawTextHelpFormatter)
parser.add_argument("command", choices = ['configure', 'add', 'remove', 'show'],
		    help = 'Four commands supported by papershelf\n'
		           'Options supported by configure: --database --storage ' 
                           '--searchdir\n'
			   'Options supported by add:-a -f -s -p -n -t -y -c -d\n'
			   'Options supported by remove: -a -f -s -p -n\n'
			   'Options supported by show: -a -f -s -p -n\n')
parser.add_argument('--database',
		    help = 'Directory saving the papershelf database')
parser.add_argument('--storage',
		    help = 'Directory saving all recorded papers')
parser.add_argument('--searchdir',
                    help = 'Directory for searching the file')
parser.add_argument('-a', '--area', default = 'ComputerScience',
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
        self.shelves = []
        settings.init()

        self.__initialize_configs()
        self.__initialize_areas()

    def __initialize_configs(self):
        if os.path.exists('.config') == True:
            with open('.config', 'r') as f:
                for line in f:
                    if 'DATABASE_DIR' in line.split():
                        self.database_dir = line.split()[2]
                    if 'STORAGE_DIR' in line.split():
                        self.storage_dir = line.split()[2]
                    if 'SEARCH_DIR' in line.split():
                        settings.rootdir = line.split()[2]

    def __initialize_areas(self):
        #if self.__path_check(self.database_dir, self.storage_dir, settings.rootdir,
        #                     'initializing') == False:
        #    return

        if os.path.exists('.area') == True:
            with open('.area', 'r') as f:
                for line in f:
                    self.shelves.append(Shelf(line.replace('\n', ''), 
                                              self.database_dir))

    def configure(self, database_dir, storage_dir, search_dir, verbosity):
        """Configure papershelf database_dir and storage_dir

        """
        tmp_database = ''
        tmp_storage = ''
        tmp_search = ''

        if os.path.exists('.config') == True:
            with open('.config', 'r') as f:
                for line in f:
                    if 'DATABASE_DIR' in line.split():
                        tmp_database = line
                    if 'STORAGE_DIR' in line.split():
                        tmp_storage = line
                    if 'SEARCH_DIR' in line.split():
                        tmp_search = line

        if os.path.exists(str(database_dir or '')) == True:
            self.database_dir = database_dir
            tmp_database = 'DATABASE_DIR = ' + database_dir + '\n'
            if verbosity >= 1:
                print 'configure database dir {}'.format(
                      str(database_dir or ''))
        else:
            if verbosity >= 1:
                print 'invalid database dir {}'.format(
                      str(database_dir or ''))

        if os.path.exists(str(storage_dir or '')) == True:
            self.storage_dir = storage_dir
            tmp_storage = 'STORAGE_DIR = ' + storage_dir + '\n'
            if verbosity >= 1:
                print 'configure storage dir {}'.format(
                      str(storage_dir or ''))
        else:
            if verbosity >= 1:
                print 'invalid storage dir {}'.format(
                      str(storage_dir or ''))

        if os.path.exists(str(search_dir or '')) == True:
            settings.rootdir = search_dir
            tmp_search = 'SEARCH_DIR = ' + search_dir + '\n'
            if verbosity >= 1:
                print 'configure search dir {}'.format(
                      str(search_dir or ''))
        else:
            if verbosity >= 1:
                print 'invalid search dir {}'.format(
                      str(search_dir or ''))

        with open('.config', 'w') as f:
            f.write(tmp_database)
            f.write(tmp_storage)
            f.write(tmp_search)
            self.add_log('configure database dir {}'.format(
                         tmp_database.replace('\n', '')))
            self.add_log('configure storage dir {}'.format(
                         tmp_storage.replace('\n', '')))
            self.add_log('configure search dir {}'.format(
                         tmp_search.replace('\n', '')))

    def add(self, area, field, subfield, problem, 
            name, title, year, conference, description, verbosity):
        """Add papershelf info based on input parameters (i.e. area, field, etc.)

        """
        if self.__path_check(self.database_dir, self.storage_dir, settings.rootdir,
                             'adding') == False:
            return

        if area is None:
            area = 'ComputerScience'

        for s in self.shelves:
            if area == s.get_area():
                s.add(self.database_dir + '/' + area, self.storage_dir + '/' + area, 
                      field, subfield, problem, name, title, year, conference, 
                      description, verbosity)
                break
        else:
            ok = raw_input('Are you sure to add area {} --> '.format(area))
            if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                self.shelves.append(Shelf(area, self.database_dir))
                if os.path.exists(self.database_dir + '/' + area) == False:
                    os.makedirs(self.database_dir + '/' + area)
                if os.path.exists(self.storage_dir + '/' + area) == False:
                    os.makedirs(self.storage_dir + '/' + area)
                with open('.area', 'a') as f:
                    f.write(area + '\n')

                if verbosity >= 1:
                    print 'add area {}'.format(area)
                self.add_log('add area {}'.format(area))

                for s in self.shelves:
                    if area == s.get_area():
                        s.add(self.database_dir + '/' + area, self.storage_dir + '/' +
                              area, field, subfield, problem, name, title, year, 
                              conference, description, verbosity)

    def remove(self, area, field, subfield, problem, name, verbosity):
        """Remove papershelf info based on input parameters (i.e. area, field, etc.)

        """
        if self.__path_check(self.database_dir, self.storage_dir, settings.rootdir,
                             'removing') == False:
            return

        for s in self.shelves[:]:
            if area == s.get_area():
                if field is None:
                    ok = raw_input('Are you sure to delete area {} --> '.format(area))
                    if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                        self.shelves.remove(s)
                        if os.path.exists(self.database_dir + '/' + area) == True:
                            shutil.rmtree(self.database_dir + '/' + area)
                        if os.path.exists(self.storage_dir + '/' + area) == True:
                            shutil.rmtree(self.storage_dir + '/' + area)

                        if verbosity >= 1:
                            print 'remove area {}'.format(area)
                        self.add_log('remove area {}'.format(area))
                else:
                    s.remove(self.database_dir + '/' + area, self.storage_dir + '/' +
                             area, field, subfield, problem, name, verbosity)

        with open('.area', 'w') as f:
            for s in self.shelves[:]:
                f.write(s.get_area() + '\n')

    def show(self, area, field, subfield, problem, name, verbosity):
        """Show papershelf info based on input parameters (i.e. area, field, etc.)

        """
        if self.__path_check(self.database_dir, self.storage_dir, settings.rootdir,
                             'showing') == False:
            return

        if area == 'all':
            for s in self.shelves[:]:
                print '{}'.format(s.get_area())
                s.show('all', 'all', 'all', 'all', verbosity)
        else:
            print '{}'.format(area)
            for s in self.shelves[:]:
                if area == s.get_area() and field is not None:
                    s.show(field, subfield, problem, name, verbosity)

        if verbosity >= 1:
            # don't mix up with the output
            # print 'show area {}'.format(area)
            pass
        self.add_log('show area {}'.format(area))

    def __path_check(self, dpath, spath, searchpath, message):
        if os.path.exists(dpath) == False:
            print "Please configure valid DATABASE_DIR path before {}".format(message)
            return False
        if os.path.exists(spath) == False:
            print "Please configure valid STORAGE_DIR path before {}".format(message)
            return False
        if os.path.exists(searchpath) == False:
            print "Please configure valid SEARCH_DIR path before {}".format(message)
            return False

        return True

if __name__ == "__main__":
    logging.basicConfig(filename='.papershelf.log', format='%(asctime)s %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p', 
                        level = logging.INFO)
    allshelf = PaperShelf()

    if args.command == 'configure':
        logging.info('Start configure transaction')
        allshelf.configure(args.database, args.storage, args.searchdir, args.verbosity)
    elif args.command == 'add':
        logging.info('Start add transaction')
        allshelf.add(args.area, args.field, args.subfield, args.problem,
                     args.name, args.title, args.year, args.conference, 
                     args.description, args.verbosity)
    elif args.command == 'remove':
        logging.info('Start remove transaction')
        allshelf.remove(args.area, args.field, args.subfield, args.problem,
                        args.name, args.verbosity)
    else:
        logging.info('Start show transaction')
        allshelf.show(args.area, args.field, args.subfield, args.problem,
                      args.name, args.verbosity)

    logging.info('End transaction')
    print 'Thanks for using papershelf v0.1 :D'
