#!/usr/bin/python 

'''
	NGINX Install Script for EC2 Linux
	By Sean Dawson (NoxHarmonium@github)
	
	
	
'''
###
actionSet = dict()
actionSet['yum_install'] = {'command': 'yum -y ', 'do': 'install', 'undo': 'remove', 'reversible': True}

