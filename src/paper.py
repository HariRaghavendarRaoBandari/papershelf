#!/usr/bin/python

import os
import shutil
import settings
from item import *

class Problem(item):
    def __init__(self, problem, subfield, dpath):
        self.problem = problem
        self.subfield = subfield
        self.dpath = dpath
        self.indexes = []
        self.papers = []

        self.__initialize_indexes()
        self.__initialize_papers()

    def __initialize_indexes(self):
        if os.path.exists(self.dpath + '/' + '.paper') == True:
            with open(self.dpath + '/' + '.paper', 'r') as f:
                for line in f:
                    self.indexes.append(line.replace('\n', ''))

    def __initialize_papers(self):
        if os.path.exists(self.dpath + '/' + self.subfield + '.txt') == True:
            with open(self.dpath + '/' + self.subfield + '.txt', 'r') as f:
                for line in f:
                    str = line.replace('\n', '').split('|')
                    self.papers.append(Paper(str[0], str[1], str[2], str[3], str[4]))

    def get_problem(self):
        return self.problem

    def add(self, dpath, spath, name, title, year, conference, description,
            verbosity):
        if name is None:
            return

        if name in self.indexes:
            return
        else:
            for dirpath, dirs, files in os.walk(settings.rootdir):
                if name in files:
                    if title is None:
                        title  =  raw_input('Please enter the title: ')
                    if year is None:
                        year = raw_input('Please enter the year: ')
                    if conference is None:
                        conference = raw_input('Please enter the conference: ')
                    if description is None:
                        description = raw_input('Please enter the description: ')

                    self.indexes.append(name)
                    self.papers.append(Paper(name, title, year, conference, description))
                    with open(self.dpath + '/' + '.paper', 'a') as f:
                        f.write(name + '\n')
                    with open(self.dpath + '/' + self.subfield + '.txt', 'a') as f:
                        f.write(name + '|' + title + '|' + year + '|' + conference
                                + '|' + description + '\n')

                    oldfile = os.path.join(dirpath, name)
                    shutil.move(oldfile, spath)

                    if verbosity >= 1:
                        print 'add paper {}'.format(name)
                    self.add_log('add paper {}'.format(name))
                    break
            else:
                if verbosity >= 1:
                    print 'no file {} founded'.format(name)
                self.add_log('no file {} founded'.format(name))

    def remove(self, dpath, spath, name, verbosity):
        for i in self.indexes[:]:
            if i == name:
                self.indexes.remove(i)

        for p in self.papers[:]:
            if name == p.get_name():
                self.papers.remove(p)

        with open(dpath + '/' + '.paper', 'w') as f:
            for i in self.indexes[:]:
                f.write(i + '\n')
        with open(dpath + '/' + self.subfield + '.txt', 'w') as f:
            for p in self.papers[:]:
                f.write(p.get_name() + '|' + p.get_title() + '|' + p.get_year() + '|' +
                        p.get_conference() + '|' + p.get_description() + '\n')

        os.remove(spath + '/' + name)

        if verbosity >= 1:
            print 'remove paper {}'.format(name)
        self.add_log('remove paper {}'.format(name))

    def show(self, name, verbosity):
        if name == 'all':
            for p in self.papers[:]:
                print '|-|-|-|-{}'.format('Paper Background: ' + p.get_year() +
                                          '\t' + p.get_conference() + '\t' +
                                          p.get_name())
                print '|-|-|-|-|-|-|-{}'.format('Title: ' + p.get_title())
                print '|-|-|-|-|-|-|-{}'.format('Description: ' + p.get_description())
        else:
            for p in self.papers[:]:
                if name == p.get_name():
                    print '|-|-|-|-{}'.format('Paper Background: ' + p.get_year() +
                                              '\t' + p.get_conference() + '\t' +
                                              p.get_name())
                    print '|-|-|-|-|-|-|-{}'.format('Title: ' + p.get_title())
                    print '|-|-|-|-|-|-|-{}'.format('Description: ' + 
                                                    p.get_description())

class Paper(item):
    def __init__(self, name, title, year, conference, description):
        self.name = name
        self.title = title
        self.year = year
        self.conference = conference
        self.description = description

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title

    def get_year(self):
        return self.year

    def get_conference(self):
        return self.conference

    def get_description(self):
        return self.description
