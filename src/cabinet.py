#!/usr/bin/python

import os
import shutil
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

    def remove(self, dpath, spath, problem, name, verbosity):
        for p in self.problems[:]:
            if problem == p.get_problem():
                if name is None:
                    ok = raw_input('Are you sure to delete problem {} --> '.format(
                                   problem))
                    if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                        self.problems.remove(p)

                        if verbosity >= 1:
                            print 'remove problem {}'.format(problem)
                        self.add_log('remove problem {}'.format(problem))
                else:
                    p.remove(dpath, spath, name, verbosity)

        with open(dpath + '/' + '.problem', 'w') as f:
            for p in self.problems[:]:
                f.write(p.get_problem() + '\n')

    def show(self, problem, name, verbosity):
        if problem == 'all':
            for p in self.problems[:]:
                print '|-|-|-{}'.format(p.get_problem())
        else:
            print '|-|-|-{}'.format(problem)
            for p in self.problems[:]:
                if problem == p.get_problem() and name is not None:
                    p.show(name, verbosity)

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

        self.subfields = []
    def remove(self, dpath, spath, subfield, problem, name, verbosity):
        for sf in self.subfields[:]:
            if subfield == sf.get_subfield():
                if problem is None:
                    ok = raw_input('Are you sure to delete subfield {} --> '.format(
                                   subfield))
                    if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                        self.subfields.remove(sf)
                        if os.path.exists(dpath + '/' + subfield) == True:
                            shutil.rmtree(dpath + '/' + subfield)
                        if os.path.exists(spath + '/' + subfield) == True:
                            shutil.rmtree(spath + '/' + subfield)

                        if verbosity >= 1:
                            print 'remove subfield {}'.format(subfield)
                        self.add_log('remove subfield {}'.format(subfield))
                else:
                    sf.remove(dpath + '/' + subfield, spath + '/' + subfield, 
                              problem, name, verbosity)

        with open(dpath + '/' + '.subfield', 'w') as f:
            for sf in self.subfields[:]:
                f.write(sf.get_subfield() + '\n')

    def show(self, subfield, problem, name, verbosity):
        if subfield == 'all':
            for sf in self.subfields[:]:
                print '|-|-{}'.format(sf.get_subfield())
        else:
            print '|-|-{}'.format(subfield)
            for sf in self.subfields[:]:
                if subfield == sf.get_subfield() and problem is not None:
                    sf.show(problem, name, verbosity)

        if verbosity >= 1:
            # don't mix up with the output
            # print 'show subfield {}'.format(subfield)
            pass
        self.add_log('show subfield {}'.format(subfield))
