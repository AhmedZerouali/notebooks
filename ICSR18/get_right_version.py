import pandas as pd
import datetime
import re
import numpy as np
from datetime import datetime

def get_right_version_digit(version,date,dependency):
	version_2=version.split('-')[0]
	if 'x' in version_2.lower() or '*' in version_2:
		return get_right_version_caret_tilde(version,date,dependency)
	return versions1.query('package=="'+dependency+'"').query('version=="'+str(version)+'"').head(1).values[0]

def get_right_version_caret_tilde(version,date,dependency):
	versionT=version.split('.')
	version_minor=version.lower().replace("x", "0")
	version_minor=version_minor.lower().replace("*", "0")
	if version.startswith('~'):
		version=version[1:]
		version_minor=versionT[0].lower()[1:]+'.'+versionT[1].lower()+'.'+versionT[2].lower()
		version=versionT[0].lower()[1:]+'.'+str(int(versionT[1].lower())+1)
	if version.startswith('^'):
		version_minor=versionT[0].lower()[1:]
		version=str(int(versionT[0].lower()[1:])+1)

	return versions.query('version>="'+version_minor+'"').query('version<"'+version+'"').tail(1).values[0]

def get_right_version_latest(date,dependency):
	return versions.query('date<="'+date+'"').tail(1).version.values[0]

def get_right_version_bigger(version,date,dependency):
	if 'x' in version.lower() or '*' in version:
		version=version.lower().replace("x", "0")
		version=version.lower().replace("*", "0")
	if version[0]=='=':
		version=version[1:]
		return versions.query('version>="'+version+'"').tail(1).values[0]
	return versions.query('version>"'+version+'"').tail(1).values[0]

	
def get_right_version_lesser(version,date,dependency):
	if 'x' in version.lower() or '*' in version:
		version=version.lower().replace("x", "0")
		version=version.lower().replace("*", "0")
	if version[0]=='=':
		version=version[1:]
		return versions.query('version<="'+version+'"').tail(1).values[0]
	return versions.query('version<"'+version+'"').tail(1).values[0]


def get_right_version_letter(version,date,dependency):
	if '@' in version:
		return get_right_version(version.split('@')[1],date,dependency,False,False)
	if 'undefined' in version:
		return get_right_version(version.replace('undefined',''),date,dependency,False,False)
	if '{""version"' in version:
		return get_right_version(version.split('"')[7],date,dependency,False,False)
	return get_right_version(version[1:],date,dependency,False,True)


def get_right_version(version,date,dependency,equal,last_chance):
	if version[0].isdigit(): # if it starts with a number
		return get_right_version_digit(version,date,dependency)

	if equal: # if it starts with '=' or 'v', second iteration
		if version[1:][0].isdigit():
			return get_right_version_digit(version[1:],date,dependency)
		return 'False'

	if version.startswith('^') or version.startswith('~'):
		return get_right_version_caret_tilde(version,date,dependency)

	if version.startswith('=') or version.startswith('v'):
		return get_right_version(version[1:],date,dependency,True,False)

	if version.startswith('<'):
		return get_right_version_lesser(version[1:],date,dependency)

	if version.startswith('>'):
		return get_right_version_bigger(version[1:],date,dependency)

	if version.startswith('*.') or version.lower().startswith('x.') or len(version)==1 or version=='latest' or version.lower()=='x' or version=='*':
		return get_right_version_latest(date,dependency)
	if last_chance:
		return 'False'
	return get_right_version_letter(version,date,dependency)


versions1=pd.read_csv('./versions_15June17.csv', sep=',', dtype=object, index_col=None)
versions1.sort_values(['date'], ascending=True, inplace=True)


num_lines = sum(1 for line in open('new_data,csv'))

f=open('new_data2.csv','w')
with open('./easy_ones_2.csv') as lines:
	for index, line in enumerate(lines):
		if index < num_lines:
			continue
		line=line.strip('\n')
		row=line.split(',')
		version=row[4]
		date=row[5]
		dependency=row[0]
		versions=versions1.query('package=="'+dependency+'"').query('date<="'+date+'"')
		try:
			right_version=get_right_version(version,date,dependency,False,False)
			new_date=versions.tail(1).date.values[0]
		except:
			right_version=['False','False','False']
			new_date='False'

		f.write(line+','+right_version[1]+','+new_date+','+right_version[2]+'\n')
f.close()


