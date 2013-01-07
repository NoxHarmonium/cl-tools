#!/usr/bin/python
"""
   This script aims to package up latex projects with all it's
   dependencies so that it runs on any machine.
"""

import argparse
import glob
import os

# Constants
EXIT_SUCCESS = 0;
EXIT_ERROR = 1;


def exit_error():
	print "Fatal Error: Exiting..."
	sys.exit(EXIT_ERROR);

print "latex-packager: By Sean Dawson"

parser = argparse.ArgumentParser(description='Packages up a latex directory.')
parser.add_argument('-v', action="store_true",default=False, 			
		help='show verbose debugging messages.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-z', action="store_true",default=False, 			
		help='Use tar/gzip compression. (Default)')
group.add_argument('-j', action="store_true",default=False, 			
		help='Use tar/bzip2 compression.')
group.add_argument('-7', action="store_true",default=False, 			
		help='Use 7z compression. (Requires p7zip)')
group.add_argument('-p', action="store_true",default=False, 			
		help='Use zip compression.v (Requires zip)')


parser.add_argument('source', type=str,
		help='the directory containing the latex source to package')
parser.add_argument('destination', type=str, 
		help='the output file name')


# Parse the given args, show help on invalid args.
args = parser.parse_args()


# Simple sanity check
os.chdir(args.source)
if (len(glob.glob("*.tex")) == 0):
	print "There are no tex files in this directory. Are you sure you supplied a latex source directory?";
	exit_error();



print ("\nlatex-packager works by reading .fls files generated by running latex with the -recorder switch. " 
	"If each .tex file has a matching .fls file with a greater modification time than the packaging can proceed. " 
	"Otherwise other options will be presented.")







