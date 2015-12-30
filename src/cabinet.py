#!/usr/bin/python

import os
from item import *
from paper import *

class SubCabinet(item):
    def __init__(self, subfield, dpath):
        self.subfield = subfield
        self.dpath = dpath
        self.problems = []

        self.__initialize_problems()

    def __initialize_problems(self):
        if os.path.exists(self.dpath + '/' + self.subfield + '/' + '.problem') == True:
            with open(self.dpath + '/' + self.subfield + '/' + '.problem', 'r') as f:
                for line in f:
                    self.problems.append(Problem(line.replace('\n', ''), self.subfield,
                                                 self.dpath + '/' + self.subfield))

    def get_subfield(self):
        return self.subfield

    def add(self, dpath, spath, problem, name, title, year, conference,
            description, verbosity):
        if problem is None:
            return

        for p in self.problems:
            if problem == p.get_problem():
                p.add(dpath, spath, name, title, year, conference, description,
                      verbosity)
                break
        else:
            ok = raw_input('Are you sure to add problem {} --> '.format(problem))
            if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                self.problems.append(Problem(problem, self.subfield, dpath))
                with open(dpath + '/' + '.problem', 'a') as f:
                    f.write(problem + '\n')

                if verbosity >= 1:
                    print 'add problem {}'.format(problem)
                self.add_log('add problem {}'.format(problem))

                for p in self.problems:
                    if problem == p.get_problem():
                        p.add(dpath, spath, name, title, year, conference, description,
                              verbosity)

class Cabinet(item):
    def __init__(self, field, dpath):
        self.field = field
        self.dpath = dpath
        self.subfields = []

        self.__initialize_subfields()

    def __initialize_subfields(self):
        if os.path.exists(self.dpath + '/' + self.field + '/' + '.subfield') == True:
            with open(self.dpath + '/' + self.field + '/' + '.subfield', 'r') as f:
                for line in f:
                    self.subfields.append(SubCabinet(line.replace('\n', ''),
                                                     self.dpath + '/' + self.field))

    def get_field(self):
        return self.field

    def add(self, dpath, spath, subfield, problem, name, title, year,
            conference, description, verbosity):
        if subfield is None:
            return

        for sf in self.subfields:
            if subfield == sf.get_subfield():
                sf.add(dpath + '/' + subfield, spath + '/' + subfield, problem,
                       name, title, year, conference, description, verbosity)
                break
        else:
            ok = raw_input('Are you sure to add subfield {} --> '.format(subfield))
            if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                self.subfields.append(SubCabinet(subfield, self.dpath + '/' + 
                                                 self.field))
                if os.path.exists(dpath + '/' + subfield) == False:
                    os.makedirs(dpath + '/' + subfield)
                if os.path.exists(spath + '/' + subfield) == False:
                    os.makedirs(spath + '/' + subfield)
                with open(dpath + '/' + '.subfield', 'a') as f:
                    f.write(subfield + '\n')

                if verbosity >= 1:
                    print 'add subfield {}'.format(subfield)
                self.add_log('add subfield {}'.format(subfield))

                for sf in self.subfields:
                    if subfield == sf.get_subfield():
                        sf.add(dpath + '/' + subfield, spath + '/' + subfield, problem,
                               name, title, year, conference, description, verbosity)
