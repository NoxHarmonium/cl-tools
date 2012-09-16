#!/usr/bin/python

#Imports
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Finds csv files with bogus hypervolume values and renames them to .bogus.')
parser.add_argument('-r', action="store_true",default=False, 			help='rename .bogus files back to .csv.')
parser.add_argument('-v', action="store_true",default=False, 			help='show verbose debugging messages.')
parser.add_argument('folder', type=str, 
		help='folder to scan recursivly for bogus hypervolume data.')

args = parser.parse_args()

fileList = []
for root, subFolders, files in os.walk(args.folder):
		for file in files:			
			f = os.path.join(root,file)	
			pathsplit = f.split('.')
			ext = pathsplit[len(pathsplit)-1]
			if (args.v):
				print ('Adding file: {0}, ext: {1}'.format(os.path.basename(f),ext))

			if (not(args.r)):			
				if (ext == 'csv'):
					fileList.append(f)
			else:
				if (ext == 'bogus'):
					fileList.append(f)
				

if (len(fileList) == 0):
	print('No files found to process!')
	sys.exit(1)

if (args.r):
	for filename in fileList:
		print('Restoring \'{0}\'...'.format(os.path.basename(filename)))
		os.rename(filename, filename.replace('.bogus',''))
	print ('Renamed {0} files.'.format(len(fileList)))		
else:

	bogusCount = 0
	for filename in fileList:
		current = 'undefined'		
		f = open(filename,'r')
		line = f.readline()	 
		line = f.readline()	 
		while (line != ''):
			lSplit = line.split(',')
			bogus = False
			if (len(lSplit) > 1):
				if (current == 'undefined'):
					current = lSplit[1]
				else:		
					if (float(current) > float(lSplit[1])):
						if (args.v):
							print('Bogus value found: prevLine: {0}, currLine: {1}'.format(current,lSplit[1]))
							print('line: {0}'.format(line))							
							print('Marked for rename...')
						bogus = True
						break
			line = f.readline()
	
		f.close()

		if (bogus):
			print('\'{0}\' is bogus. Renaming...'.format(os.path.basename(filename)))
			os.rename(filename, '{0}.bogus'.format(filename))	
			bogusCount += 1
	

	print ('Renamed {0} files.'.format(bogusCount))	


