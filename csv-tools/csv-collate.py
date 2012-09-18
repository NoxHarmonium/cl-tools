#!/usr/bin/env python

# JSON Dump
# Performs transformations on multiple csv files
# of the same format such as averaging.
#

import fileinput
import sys
import json
import md5
from argparse import ArgumentParser
from hv import HyperVolume

parser = ArgumentParser(description='Performs transformations on multiple csv files of the same format such as averaging.',
	     epilog="By Sean Dawson")
parser.add_argument('-v', action="store_true",default=False, help='show verbose debugging messages.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-n', action="store", type=int, default=-1, help='the number of rows considered as one page (default: detect from blank lines).')
group.add_argument('-g' , action="store", help='group by specifed column/s (comma delimited).')

parser.add_argument('-m', action="store", help='min of specified column/s (comma delimited).')
parser.add_argument('-M', action="store", help='max of specified column/s (comma delimited).')
parser.add_argument('-a', action="store", help='average specified column/s (comma delimited).')
parser.add_argument('-y', action="store", help='calculate hypervolume on specified column/s (comma delimited). The first column specifies the rank.')
parser.add_argument('-s', action="store", type=int, default=0, help='the amount of lines to skip on each page. (to avoid headers)')



parser.add_argument('files', nargs='*', help='specify input files')


group = parser.add_mutually_exclusive_group()
group.add_argument('-o', '--output', 
    help='specify the output file.  The default is stdout')
group.add_argument('-i', '--inplace', action='store_true',
    help='modify files inplace')
args = parser.parse_args()

def processCell(cell, index, allCols,n):
	i = index	
	for col in allCols:
		i -= len(col['list'])
		if (i < 0):
			if (args.v):			
				print ('index: {0}, col: {1}'.format(index,col['action']))

			if (col['action'] == 'average'):
				return cell / n

			if (col['action'] == 'hypervolume'):
				return hvAggr/hvTotal
			return cell

if args.output and args.output != '-':
   sys.stdout = open(args.output, 'w')

lineCount = args.s
agrLines = []
pageCount = 0
hvBounds = []
if (args.m != None):
	minCols = map(int, args.m.split(','))
else:
	minCols = []
if (args.M != None):
	maxCols = map(int, args.M.split(','))
else:
	maxCols = []
if (args.a != None):
	avCols = map(int, args.a.split(','))
else:
	avCols = []
if (args.y != None):
	hvCols = map(int, args.y.split(','))
	for i in range(len(hvCols)):
		if i < 2: 
			continue
		hvBounds.append({'min': sys.float_info.max, 'max': sys.float_info.min})
else:
	hvCols = []

fronts = [[]]
hvCounter = 0
hvTotal = 0
hvAggr = 0
frontCount = 1

allCols = [
		{'action': 'min', 'list': minCols},
		{'action': 'max', 'list': maxCols},
		{'action': 'average', 'list': avCols},
		{'action': 'hypervolume', 'list': hvCols}]

if (args.n != -1):
	for i in range(args.n):
		agrLines.append([])

for line in fileinput.input(args.files, inplace=args.inplace):
	
	line = line.strip()	
	if (line == '' or line[0] == '#'):
		lineCount = 0
		continue	
	if (args.n != -1):
		if (lineCount >= args.n + args.s -1):
			lineCount = 0
			pageCount += 1	
			if (args.v):
				print ('New page')

		#if (lineCount <= args.s):
		#	lineCount += 1
		#	continue

		tokens = line.split(',')
		
		lineIndex = lineCount - args.s-1
		if (args.v):		
			print ('lineIndex: {0} toks: {1}'.format(lineIndex,tokens))
		
		l = 0

		try:
			for i in range(len(minCols)):
				col = minCols[i]
				if (len(agrLines[lineIndex]) - 1 < i + l):
					agrLines[lineIndex].append(float(tokens[col]))
				else:
					agrLines[lineIndex][i+l] = min(agrLines[lineIndex][i+l],float(tokens[col]))

			l += len(minCols)

			for i in range(len(maxCols)):
				col = maxCols[i]
				if (len(agrLines[lineIndex]) - 1 < i + l):
					agrLines[lineIndex].append(float(tokens[col]))
				else:
					agrLines[lineIndex][i+l] = max(agrLines[lineIndex][i+l],float(tokens[col]))

			l += len(maxCols)

			for i in range(len(avCols)):
				col = avCols[i]
				if (len(agrLines[lineIndex]) - 1 < i + l):
					agrLines[lineIndex].append(float(tokens[col]))
				else:
					agrLines[lineIndex][i+l] += float(tokens[col])
		
			l += len(avCols)		
	
			point = []
			for i in range(len(hvCols)):
				if (len(agrLines[lineIndex]) - 1 < i + l):
					agrLines[lineIndex].append('hv')
				else:
					agrLines[lineIndex][i+l] = 'hv'

				col = hvCols[i]
				if (i == 0):
					if (hvCounter > int(hvCols[i])):
						front = fronts[frontCount-1]
						#print 'Appending front: {0}'.format(front)
						#front = []

						fronts.append([])
						frontCount += 1												
						#hvAggr += hv
						hvCounter = 0
						#hvTotal += 1

					else:
						hvCounter += 1
						#print ('a')
				
				if (i > 1):
					#print "hvBounds[i-2]['min']: {0}, tokens[col]: {1}".format(hvBounds[i-2]['min'],tokens[col])
					hvBounds[i-2]['min'] = min(hvBounds[i-2]['min'],float(tokens[col]))
					hvBounds[i-2]['max'] = max(hvBounds[i-2]['max'],float(tokens[col]))
					point.append(float(tokens[col]))				

				if (i == 1):
					if (int(tokens[col]) != 1):
						#break if not rank 1
						break

				
		except IndexError:
			print ('Current line: {0}, i: {1}, l: {2}, tokens: {3}, lineCount: {4}'.format(agrLines[lineIndex],i,l,tokens,lineCount))
			raise
			
		if (point != []):		
			fronts[frontCount-1].append(point)
		l += len(hvCols)		



		lineCount += 1

#if (lineCount != 0):
#	pageCount += 1

#print ('Final page count: {0}'.format(pageCount))

#print 'Points:'
#for point in front:
#	print(point)

#print 'hvBounds:\n{0}'.format(hvBounds)

for front in fronts:
	
	
	
	for i in range(len(front)):
		for j in range(len(front[i])):
			front[i][j] = (front[i][j] - hvBounds[j]['min']) / (hvBounds[j]['max'] - hvBounds[j]['min'])
		#print ('Normalised Front: {0}'.format(front[i]))
		referencePoint = [1,1]						
	
	
	hyperVolume = HyperVolume(referencePoint)
	hv = hyperVolume.compute(front)	
	hvAggr += hv
	hvTotal += 1

#print 'Hypervolume:\n {0}'.format(hvAggr/hvTotal)





#print 'Results:'
for line in agrLines:
	lineString = ''
	i = 0
	for cell in line:
		cell = processCell(cell,i,allCols,pageCount)		
		lineString += '{0}, '.format(cell)
		i += 1
	print lineString[:-2]
		




#TODO: Somethings

