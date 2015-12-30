#!/usr/bin/python

import os
import shutil
from item import *
from cabinet import *

class Shelf(item):
    def __init__(self, area, dpath):
        self.area = area
        self.dpath = dpath
        self.fields = []

        self.__initialize_fields()

    def __initialize_fields(self):
        if os.path.exists(self.dpath + '/' + self.area + '/' + '.field') == True:
            with open(self.dpath + '/' + self.area + '/' + '.field', 'r') as f:
                for line in f:
                    self.fields.append(Cabinet(line.replace('\n', ''),
                                               self.dpath + '/' + self.area))

    def get_area(self):
        return self.area

    def add(self, dpath, spath, field, subfield, problem, name, title,
            year, conference, description, verbosity):
        if field is None:
            return

        for f in self.fields:
            if field == f.get_field():
                f.add(dpath + '/' + field, spath + '/' + field, subfield, problem,
                      name, title, year, conference, description, verbosity)
                break
        else:
            ok = raw_input('Are you sure to add field {} --> '.format(field))
            if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                self.fields.append(Cabinet(field, self.dpath + '/' + self.area))
                if os.path.exists(dpath + '/' + field) == False:
                    os.makedirs(dpath + '/' + field)
                if os.path.exists(spath + '/' + field) == False:
                    os.makedirs(spath + '/' + field)
                with open(dpath + '/' + '.field', 'a') as f:
                    f.write(field + '\n')

                if verbosity >= 1:
                    print 'add field {}'.format(field)
                self.add_log('add field {}'.format(field))

                for f in self.fields:
                    if field == f.get_field():
                        f.add(dpath + '/' + field, spath + '/' + field, subfield,
                              problem, name, title, year, conference, description,
                              verbosity)

    def remove(self, dpath, spath, field, subfield, problem, name, verbosity):
        for f in self.fields[:]:
            if field == f.get_field():
                if subfield is None:
                    ok = raw_input('Are you sure to delete field {} --> '.format(field))
                    if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                        self.fields.remove(f)
                        if os.path.exists(dpath + '/' + field) == True:
                            shutil.rmtree(dpath + '/' + field)
                        if os.path.exists(spath + '/' + field) == True:
                            shutil.rmtree(spath + '/' + field)

                        if verbosity >= 1:
                            print 'remove field {}'.format(field)
                        self.add_log('remove field {}'.format(field))
                else:
                    f.remove(dpath + '/' + field, spath + '/' + field, subfield,
                             problem, name, verbosity)

        with open(dpath + '/' + '.field', 'w') as f:
            for fe in self.fields[:]:
                f.write(fe.get_field() + '\n')

    def show(self, dpath, spath, field, subfield, problem, name, verbosity):
        pass
