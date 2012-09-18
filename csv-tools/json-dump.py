#!/usr/bin/env python

# JSON Dump
# Parses a JSON file/s to a csv format.
#

import fileinput
import sys
import json
import md5
import os
from argparse import ArgumentParser


# Global Vars
header = []

def isToken(char):
	return char == '.' or char == '>'  or char == '[' or char == ']'

def recurseJson(tokens, jsonObject):
	
	cTokens = list(tokens)
	if (len(cTokens) == 0):
		#if (args.v):		
		#	print ('len(tokens)==0: returning {0}'.format([str(jsonObject)]))
		return [str(jsonObject)]
	
	mainTok = cTokens.pop(0)	
	
	if (args.v):
		print ('toklength={0} name = {1}'.format(len(cTokens),mainTok['name']))	
	#	print ('toks: {0}, o: {1}\n'.format(mainTok,jsonObject))
	#	print ('tok: {0}'.format(mainTok['token']))
	
	
	#print ('toks: {0}, o: {1}\n'.format(mainTok,o))
		
	rows = []
	if (mainTok['token'] == '.'):
		#header[len(tokens)-1] = '<member>'
		header[len(tokens)] = '<member>'
		if (args.v):
			print ('Reading member: {0}'.format(mainTok['name']))
		name = mainTok['name']
		
		if (len(name) > 0 and name[0] == '['):
			if (name[len(name)-1] == ']'):
				name = name[1:-1].split(',')
			else:
				raise NameError('Unmatched brace in token.')
		else:
			name = [name]		
		
		first = True
	 	header[len(tokens)-1] = ''
		for n in name:
			try:
				o = jsonObject[n]		
			except KeyError:
				o = ['null']			
			except TypeError:
				print ('jsonObject: {0}'.format(jsonObject))
				raise
			header[len(tokens)-1] += n + ', <member>, '		
		
			newRows = recurseJson(cTokens,o)
			for i in range(len(newRows)):
				if (first):
					try:					
						rows.append(n + ',' + newRows[i])
					except TypeError:
						print ('n: {0}, newRows[i]: {1}'.format(n, newRows[i]))
						raise
				else:				
					rows[i]  += ',' + n + ',' + newRows[i]		

			first = False
		
		header[len(tokens)-1] = header[len(tokens)-1][:-12]				
			
		return rows

	elif (mainTok['token'] == '>'):
		#if (args.v):		
		#	print ('Expanding array: {0}'.format(mainTok['name']))
		header[len(tokens)-1] = tokens[0]['name']	
		#rows = [mainTok['name']]
		
		index = 0
		for i in jsonObject:
			for j in recurseJson(cTokens,i):
				rows.append(str(index) + ',' + j)
			index += 1
		
		#rows[0] = '>,>'
		#for i in range(len(rows)):
		#	if (i != 0):
		#		rows[i] = str(i) + ',' + rows[i]
	elif (mainTok['token'] == '['):
		rows = []
		for section in mainTok['name'].split(','):		
			newTokens = tokenify(section)		
			j = recurseJson(newTokens,jsonObject)

			rows.append(', '.join([str(x) for x in j])		)
			if (args.v):
				print ('rows!: {0}'.format(rows))
		rows = [', '.join([str(x) for x in rows])]

	return rows;

def tokenify(query):
	tokens = []
	tokens.append({'name': '', 'token':'.'})
	i = 0	
	skipParse = False
	for char in query:
		if (isToken(char)):
			if (skipParse):
				if (char == ']'):
					skipParse = False
				else:
					tokens[i]['name'] += char
				continue
			if (char == '['):
				skipParse = True
				#continue

			tokens.append({'name': '', 'token': char})
			i += 1
			if (char == '>'):
				tokens[i]['name'] = tokens[i-1]['name']			


		else:
			tokens[i]['name'] += char


	return tokens
	
def processFile(fileName,fileData, query):
	#header = []
	if (fileData == ''):
		return
	j = json.loads(fileData)	
	

	tokens = tokenify(query)


	for token in tokens:
		if (args.v):		
			print('token: {0}'.format(token))
		header.append('')
	header.append('')
	
	result = recurseJson(tokens, j)	
	header.append('filename')
	header.reverse()
	print '#' +  ', '.join([str(x) for x in header])
	for r in result:
		print (os.path.basename(fileName) + ',' + r)



parser = ArgumentParser()
parser.add_argument('-v', action="store_true",default=False, help='show verbose debugging messages.')
parser.add_argument('query', type=str, help='the query string to parse the JSON with.')
parser.add_argument('files', nargs='*', help='specify input files')


group = parser.add_mutually_exclusive_group()
group.add_argument('-o', '--output', 
    help='specify the output file.  The default is stdout')
group.add_argument('-i', '--inplace', action='store_true',
    help='modify files inplace')
args = parser.parse_args()

if args.output and args.output != '-':
   sys.stdout = open(args.output, 'w')


currentFile = ''
fileData = ''

firstHeaderStr = ''
#firstHeader = []
firstHeaderMd5 = ''
first = True

for line in fileinput.input(args.files, inplace=args.inplace):
	if (currentFile != fileinput.filename()):
		if (args.v):		
			print ('Now reading \'{0}\'...'.format(fileinput.filename()))
		header = []		
		processFile(currentFile,fileData,args.query)		
		headerStr =  '#' + ', '.join([str(x) for x in header])

		if (first):
			firstHeaderStr = headerStr
			firstHeaderMd5 = md5.new(headerStr).digest()
			first = False
		#else:
			#print ('{0} == {1}'.format(			md5.new(headerStr).digest() , firstHeaderMd5))
			#if (md5.new(headerStr).digest() != firstHeaderMd5):
				#raise NameError('Non consistant header detected')
			
			

		currentFile = fileinput.filename()   
		fileData = line
	else:
		fileData += line
header = []
processFile(currentFile,fileData,args.query)	

	
	#process(line)

