#!/usr/bin/python
"""
   This script aims to package up latex projects with all it's
   dependencies so that it runs on any machine.
"""

import argparse
import glob
import os
import sys
import time
from subprocess import call

# Constants
EXIT_SUCCESS = 0;
EXIT_ERROR = 1;

#Global Vars
force = False;
show_debug = False;

def exit_error():
	print "Fatal Error: Exiting..."
	sys.exit(EXIT_ERROR)

def exit_warning():
	if (not(force)):
		print "Error: Exiting... (You can ignore this message and continue by using the '-f' switch."
		sys.exit(EXIT_ERROR);

def debug(message):
	if (show_debug):
		print message

print "latex-packager: By Sean Dawson"

parser = argparse.ArgumentParser(description='Packages up a latex directory.')
parser.add_argument('-v', action="store_true",default=False, 			
		help='show verbose debugging messages.')

parser.add_argument('-f', action="store_true",default=False, 			
		help='force run. Skips error messages.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-z', action="store_true",default=False, 			
		help='Use tar/gzip compression. (Default)')
group.add_argument('-j', action="store_true",default=False, 			
		help='Use tar/bzip2 compression.')
group.add_argument('-7', action="store_true",default=False, 			
		help='Use 7z compression. (Requires p7zip)')
group.add_argument('-p', action="store_true",default=False, 			
		help='Use zip compression.v (Requires zip)')

parser.add_argument('--latex', default='pdflatex', 
		help='specify the latex complier to use when generating .fls files. (Default: pdflatex)')
		

parser.add_argument('tex_file', type=str, nargs='+', 
		help='one or many tex files to package.')
parser.add_argument('destination', type=str, 
		help='the output file name')


# Parse the given args, show help on invalid args.
args = parser.parse_args()

force = args.f;
show_debug = args.v;

for filename in args.tex_file:
	fileSplit = filename.split('.')
	extension = fileSplit[-1]
	rawfilename = "".join(fileSplit[0:-1])
	flsfilename = rawfilename + '.fls'

	debug("filename: '{0}'".format(filename))
	debug("flsfilename: '{0}'".format(flsfilename))
	
	# Simple filename sanity check.
	if (not(extension == 'tex')):
		print ("Warning: '{0}' does not seem to be a .tex file. Please specify a tex file to package.") 
		exit_warning()
	
	# Check if .fls exists
	createfls = not(os.path.exists(flsfilename))

	debug("createfls: {0}".format(createfls))

	# Check the validity of the fls file if it exists
	if (not(createfls)):	
		debug("Checking fls files...")
		# Check if .fls files are up to date
		texMTime = time.ctime(os.path.getmtime(filename))
		flsMTime = time.ctime(os.path.getmtime(flsfilename))

		debug("texMTime: {0}".format(texMTime))
		debug("flsMTime: {0}".format(flsMTime))

		if (flsMTime < texMTime):
			print("The .fls file has a modification date that is earlier than the tex file. It will need to be regenerated.")
			createfls = True

	
	# Regenerate fls files if needed
	if (createfls):
		debug("Regenerating .fls files...")
		
		print("The .fls file does not exist or is out of date. "
			  "The tex file needs to be recompiled with the '-recorder' switch. "
			  "Do you want the script to this for you? [Y/n]")
		
		# Blank answer defaults to yes
		answer = None
		while (not(answer == 'y' or answer == 'n' or answer == '')):
			answer = input().lower().strip()
			
		if (answer == '' or answer == 'y'):
			command = "{0} -recorder {1}".format(args.latex,rawfilename)
			print ("Executing: " + command )
			call(command.split(' '))
		else:
			print ("Warning: You cannot proceed without generating a valid .fls file.") 
			exit_warning()


		
		



