#!/usr/bin/python

from item import *

class shelf(item):
    def __init__(self, area):
        self.area = area

    def get_area(self):
        return self.area

    def add(self, dpath, spath, field, subfield, problem, name, title,
            year, conference, description, verbosity):
        pass

    def remove(self, dpath, spath, field, subfield, problem, name, verbosity):
        pass

    def show(self, dpath, spath, field, subfield, problem, name, verbosity):
        pass
