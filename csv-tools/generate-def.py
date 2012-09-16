#!/usr/bin/python

#
# Generates a def file for use in gen-graph.py
#

import argparse
import os
import sys
import re

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)


parser = argparse.ArgumentParser(description='Generates a .def file for use in gen-graph.py from the header of a csv file.')
parser.add_argument('-v', action="store_true",default=False, 			help='show verbose debugging messages.')
parser.add_argument('csv_file', type=str, 
		help='the csv file to create the .def file from.')
parser.add_argument('destination', type=str, default='./output.def',
		help='the file to save the definition to. (default: ./output.def)')


args = parser.parse_args()

if (args.v):
	print('Reading {0}...'.format(args.csv_file))

f = open(args.csv_file,'r')
header = f.readline()
f.close()

if (args.v):
	print('Done')
	print('Splitting header...')

defs = header.split(',')

if (args.v):
	print('Done')
	print('Writing .def file...')

f = open(args.destination,'w')

i = 0
for d in defs:
	d = d.strip()	
	if (d != ''):
		f.write('{0},{1}\n'.format(i,convert(d)))
		i += 1

f.close()
