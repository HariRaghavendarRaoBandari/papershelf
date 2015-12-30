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
                    str = line.split('|')
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

class Paper(item):
    def __init__(self, name, title, year, conference, description):
        self.name = name
        self.title = title
        self.year = year
        self.conference = conference
        self.description = description
