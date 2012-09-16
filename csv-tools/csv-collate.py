#!/usr/bin/env python

# JSON Dump
# Performs transformations on 
#

import fileinput
import sys
import json
import md5
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument('-v', action="store_true",default=False, help='show verbose debugging messages.')

parser.add_argument('files', nargs='*', help='specify input files')


group = parser.add_mutually_exclusive_group()
group.add_argument('-o', '--output', 
    help='specify the output file.  The default is stdout')
group.add_argument('-i', '--inplace', action='store_true',
    help='modify files inplace')
args = parser.parse_args()

if args.output and args.output != '-':
   sys.stdout = open(args.output, 'w')

for line in fileinput.input(args.files, inplace=args.inplace):
	print ('')

#TODO: Everything

