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
import shutil
import tempfile
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
group.add_argument('-z', action="store_true",default=True, 			
		help='Use tar/gzip compression. (Default)')
group.add_argument('-j', action="store_true",default=False, 			
		help='Use tar/bzip2 compression.')
group.add_argument('-s', action="store_true",default=False, 			
		help='Use 7z compression. (Requires p7zip)')
group.add_argument('-p', action="store_true",default=False, 			
		help='Use zip compression. (Requires zip)')

parser.add_argument('--latex', default='pdflatex', 
		help='specify the latex complier to use when generating .fls files. (Default: pdflatex)')
		

parser.add_argument('tex_file', type=str, nargs='+', 
		help='one or many tex files to package.')
parser.add_argument('destination', type=str, 
		help='the output file name')


# Save the current directory to restore it
currentDir = os.path.dirname(os.path.abspath(__file__))

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
	if (not(os.path.exists(filename))):
		print ("Warning: '{0}' does not exist. Please specify a valid tex file.".format(filename))
		exit_warning()
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
		else:
			debug("The .fls file is up to date.")
	
	# Regenerate fls files if needed
	if (createfls):
		debug("Regenerating .fls files...")
		
		print("The .fls file does not exist or is out of date. "
			  "The tex file needs to be recompiled with the '-recorder' switch. "
			  "Do you want the script to this for you? [Y/n]")
		
		# Blank answer defaults to yes
		answer = None
		while (not(answer == 'y' or answer == 'n' or answer == '')):
			answer = raw_input().lower().strip()
			
		if (answer == '' or answer == 'y'):
			command = "{0} -recorder {1}".format(args.latex,os.path.basename(rawfilename))
			print ("Executing: " + command )
			print ("cwd: " + os.path.dirname(filename))
			os.chdir(os.path.dirname(filename))
			error_code = call(command.split(' '), cwd=os.path.dirname(filename))
			os.chdir(currentDir)
			if (error_code != EXIT_SUCCESS):
				print ("Warning: Latex complile returned errorcode {0}.".format(error_code))
				print ("Removing incomplete .fls file...")
				try:
					os.remove(flsfilename)
				except:
					""
				exit_warning()
		else:
			print ("Warning: You cannot proceed without generating a valid .fls file.") 
			exit_warning()

	# By this point the fls file should be valid
	# Read in file	
	debug("Reading in fls file...")
	flsFile = open(flsfilename, 'r')
	flsLines = flsFile.readlines()
	
	debug("Creating temp directory...")
	tempDir = tempfile.mkdtemp()
	debug("Temp directory is at '{0}'".format(tempDir))

	for line in flsLines:
		splitLine = line.split(' ')
		commandCode = splitLine[0]
		if (commandCode == 'INPUT'):
			inputFile = splitLine[1].strip()

			targetFile = ''
			#Check for absolute path
			if (inputFile[0] == '/'):
				targetFile = tempDir + '/' + os.path.basename(inputFile)
			else:
				targetFile = tempDir + '/' + inputFile

			
			debug("Copy: {0} -> {1}".format(inputFile,targetFile))
			os.chdir(os.path.dirname(filename))
			
			shutil.copyfile(inputFile, targetFile)
			os.chdir(currentDir)
		
	error_code = 0;	
		

	debug("Starting compression operation...")
	arc_format = '';

	if (args.z):
		arc_format = 'gztar'
		
	if (args.j):
		arc_format = 'bztar'

	if (args.p):
		arc_format = 'zip'

	if (args.s):
		error_code = call(['7zr','a',args.destination,'.'], cwd=os.path.dirname(filename))
	else:
		shutil.make_archive(
			os.path.abspath(args.destination),
			arc_format,
			tempDir,
			verbose=args.v)


	if (error_code != 0):
		print ("Warning: Latex compile returned errorcode {0}.".format(error_code))
		exit_warning()
	
	debug("Removing temp directory...")
	shutil.rmtree(tempDir)
		
		



