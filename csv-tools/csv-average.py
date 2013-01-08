#!/usr/bin/python
# csv-average.py: Takes a list of csv files and averages each cell.
# Switches: 
# -s [n] : Skip n lines from the top of the csv files. Default=1

# Access params from: sys.argv

#Imports
import argparse
import os
import sys
from hv import HyperVolume

EPSILON = 0.0001

parser = argparse.ArgumentParser(description='Averages .csv files into one.')
parser.add_argument('-r', action="store_true",default=False, 			help='search for csv files rescursivly.')
parser.add_argument('-v', action="store_true",default=False, 			help='show verbose debugging messages.')
parser.add_argument('-w', action="store_true",default=False, 			help='Use spaces instead of commas when writing the destination file.')

parser.add_argument('-hv', action="store",default='', type=str, 			help='Calculate hypervolume from specified columns (comma delimited).')

parser.add_argument('-s', action="store", default='1',
		dest='n', type=int,			
 		help='the number of lines to skip at the top of the csv file. (default: 1)')
parser.add_argument('csv_file', type=str, nargs='+', 
		help='a list of csv files to average.')
parser.add_argument('destination', type=str, default='./output.csv',
		help='the file to save the averaged values to. (default: ./output.csv)')


#parser.add_argument('-s', dest='skip_lines', nargs='1', #		metavar='lines', default=1, type=int,
#		help='skip n lines at the top of each file. (default: 1 line)')



args = parser.parse_args()

if (args.r and len(args.csv_file) > 1):
	print('You need to provide a single directory for recursive mode.')
	sys.exit(1)

fileList = []
root = ''

if (args.r):
	
	for root, subFolders, files in os.walk(args.csv_file[0]):
		for file in files:			
			f = os.path.join(root,file)	
			fSplit = f.split('.')
			if (fSplit[len(fSplit)-1] == 'csv'):
				fileList.append(f)
else:
	fileList = args.csv_file


if (args.r):
	print('Reading files recursivly: Base directory: {0}'.format(args.csv_file[0]))
else:
	print('Reading file list from console.')
print('Total files selected: {0}'.format(len(fileList)))
print('Averaging cells...')

masterValues = []

first = True
fileCount = 0
bounds = []
front = []
hvCols = []
if (args.hv != ''):
	if (args.v):
		print ('Hypervolume mode enabled on columns {0}...'.format( args.hv))
	hvCols = args.hv.split(',')
	for hvCol in hvCols	:
		bounds.append({'min': sys.float_info.max,
							  'max': sys.float_info.min})
	

for file in fileList:
	fileCount += 1
	f = open(file,'r')
	i = 0
	# Skip n lines	
	for n in range(args.n):
		f.readline()		
	
	line = ' ';
	while (line != ''):

		line = f.readline()
		values = line.split(',')
		j = 0;
		
		masterValues.append([]);
		#if (args.v):
			#print ("leni: {2}, (masterValues[i])={0} == len(values)={1}").format(len(masterValues[i]), len(values),i)
		
		
		if (not(first)):
			if (len(masterValues[i]) != len(values)):
				raise NameError('csv column count not consistant')	

		#if (i > 0):
		#	if (len(masterValues[i]) > 1 and len(masterValues[i-1]) > 1):			
		#		if (masterValues[i][1] < masterValues[i-1][1]):
					#print ('Hypervolume consistancy error:')					
					#print ('file: {0}'.format(file))					
					#print ('i: {0}, h[i]: {1}, h[i-1]: {2}'.format(i, masterValues[i][1],masterValues[i-1][1]))
		point = []
		for h in range(len(bounds)):
			if (len(values) > 1):
				num = 0			
				try:
					num = float(values[int(hvCols[h])])
				except ValueError:
					num = 0					
				if (num < bounds[h]['min']):
					bounds[h]['min'] = num
				if (num > bounds[h]['max']):
					bounds[h]['max'] = num
				point.append(num)

		# (args.v):
		#	print ('p: {0}'.format(point))
		front.append(point)

		for value in values:
			num = 0	
			try:
				num = float(value)
			except ValueError:
				num = 0			
			if (first):
				masterValues[i].append(num)
			else:
				masterValues[i][j] += num
				j += 1
		
		i += 1
	

	f.close()	
	first=False

if (args.hv != ''):
	print('Calculating hypervolume...')
	referencePoint = []	
	for h in range(len(bounds)):
		referencePoint.append(0)		
	
	hyperVolume = HyperVolume(referencePoint)

	newFront = []
	for p in front:
		if (len(p) > 0):
			newFront.append(p)

	front = newFront

	for p in front:
		if (len(p) > 0):		
			if (args.v):
				print ('p: {0}'.format(p))
			for h in range(len(bounds)):
				r = bounds[h]['max'] - bounds[h]['min']
				if (args.v):
					print ('r: {0}'.format(r))
				if (r != 0):
					p[h] /= r
					p[h] = 1 - p[h]				
				else:
					raise NameError('There is no range on r')
				if (p[h] < 0 or p[h] > 1):
					cont = False					
					if (p[h] < 0):
						if abs(p[h] < EPSILON):
							p[h] = 0
							cont = True

					if (p[h] > 1):
						if (abs(p[h]-1) < EPSILON):
							p[h] = 1
							cont = True

					if (not(cont)):
						print('Invalid value: {0} ({1})'.format(p[h],p))
						raise NameError('Range invalid')
			if (args.v):
				print ('p\': {0}\n'.format(p))

	unique = []

	for f in front:
		add = True		
		for u in unique:
			same = []
			#print ('{0} == {1}'.format(f,u))
			for i in range(len(f)):
				#print ('{0} == {1}'.format(len(f), len(u)))
				if (abs(f[i] - u[i]) < EPSILON):
					same.append(i)
			if (len(same) == len(front)):
				add = False
		if (add):
			unique.append(f)
					
	
	front = unique
	if (args.v):
		print ('Final front:')	
		for f in front:
			print ('{0}'.format(f))
	
	result = hyperVolume.compute(front)	
	print ('Result: {0}'.format(result))
	sys.exit(1)

print ('Writing output to {0}...'.format(args.destination))
f = open(args.destination,'w')
rowCount = 0
for row in masterValues:
	if (len(row) > 1):
		rowCount += 1

for row in masterValues:
	if (len(row) > 1):
		
		if (args.v):
			for x in row:
				print('x:{0}, fileCount:{1}, x/fileCount{2}'.format(x,fileCount,x/fileCount))
		delim = ''
		if (args.w):
			delim = ' '
		else:
			delim = ', '		
		f.write(delim.join(str(x/fileCount) for x in row) + '\n')

f.close()
print ('Done!\n')

#print (masterValues[0])
# print (args)
# print (fileList)
