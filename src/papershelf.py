#!/usr/bin/python
"""
Status: on-going
"""

import argparse
from item import *

parser = argparse.ArgumentParser(description = 'A simply paper organization tool')
parser.add_argument('command', choices = ['configure', 'add', 'remove', 'show'],
		    help = 'Four commands supported by papershelf')
parser.add_argument('-a', '--area', default = 'computer science',
		    help = 'Research area in the papershelf')
parser.add_argument('-f', '--field',
		    help = 'Field in the specified research area')
parser.add_argument('-s', '--subfield',
                    help = 'Subfield in the specified field')
parser.add_argument('-p', '--problem',
		    help = 'Problem in the subfiled')
parser.add_argument('-t', '--title',
		    help = 'Paper title')
parser.add_argument('-y', '--year', type = int,
		    help = 'Paper published year')
parser.add_argument('-c', '--conference/journal/others',
		    help = 'Paper published conference/journal/others')
parser.add_argument('-n', '--notes',
		    help = 'Write some important notes')

args = parser.parse_args()

class papershelf(item):
	pass

if __name__ == "__main__":
	print "Hello world!"
