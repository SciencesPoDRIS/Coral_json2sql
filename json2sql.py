# !/usr/bin/env python
# -*- coding: utf8 -*-
# Convert  a json file to an sql insert statement
# Execution example : python json2sql.py


#
# Libs
#

import json
import logging
import os
import sys
import time


#
# Config
#

json_fr_file = 'data/data_fr.json'
json_en_file = 'data/data_en.json'
result_file = 'items.sql'
resource_table_name = 'Resource'
lang_table_name = 'ResourceLanguage'
type_table_name = 'ResourceTypeLink'
subject_table_name = 'ResourceSubject'
admin_login = 'coral'
languages = {'en' : 1, 'fr' : 2, 'es' : 3, 'pt' : 4, 'de' : 5, 'multi' : 6}
types = {'reference tools' : 1, 'language dictionaries' : 2, 'e-books' : 3, 'press' : 4, 'e-journals' : 5, 'statistical data' : 6, 'financial data' : 7, 'multimedia' : 8, 'industry profiles' : 9, 'country profiles' : 10, 'maps' : 11, 'working papers' : 12, 'dissertations & theses' : 13, 'official publications' : 14, 'open access resources' : 15, 'national licenses' : 16, 'search engines' : 17, 'tools' : 18}
types_deleted = ['databases', 'dictionaries, encyclopedias']
subjects = {'News' : 1, 'Law' : 2 , 'Economics' : 3, 'Environment' : 4, 'Finance' : 5, 'Management' : 6, 'History' : 7, 'International Relations' : 8, 'Science' : 9, 'Political Science' : 10, 'Languages' : 11, 'Literature' : 12, 'Sociology' : 13, 'Philosophy' : 14, 'Ethnology' : 15, 'Religion' : 16, 'Arts' : 17, 'Education' : 18, 'Psychology' : 19, 'Geography' : 20}
subjects_deleted = ['Test', 'Economics & Finance', 'Social Sciences', 'Statistics', 'Reference']
accesses = {'local access only' : 1, 'remote access only' : 2, 'local and remote access' : 3, 'free access' : 4, 'restricted access' : 5}


#
# Functions
#

def mysqlFormat(s) :
	s = s.replace('\'', '\\\'')
	s = s.replace('\r\n', '')
	s = s.strip()
	return s

def getUrl(item) :
	if 'URL_REMOTE_RES' in item.keys() :
		return item['URL_REMOTE_RES'].strip()
	elif 'URL_LOCAL_RES' in item.keys() :
		return item['URL_LOCAL_RES'].strip()
	elif 'URL_FREE_RES' in item.keys() :
		return item['URL_FREE_RES'].strip()
	else :
		return ''

def insertFrenchItem(item) :
	insert = ''
	insert += 'UPDATE ' + resource_table_name
	insert += ' SET titleText_fr = \'' + mysqlFormat(item['TITRE']) + '\','
	insert += ' descriptionText_fr = \'' + mysqlFormat(item['DESCRIPTION']) + '\''
	insert += ' WHERE resourceID = ' + item['ID'] + ';\n'
	return insert

def insertEnglishItem(item) :
	insert = ''
	if len(item) == 18 or len(item) == 19 :
		if item['DESCRIPTION'] is None :
			logging.error('The discription of this item is empty : ' + item['ID']);
		insert += 'INSERT INTO ' + resource_table_name + ' (resourceID, createDate, createLoginID, titleText, descriptionText, statusID, resourceURL) VALUES ('
		insert += item['ID'] + ', '
		insert += '\'' + time.strftime("%Y-%m-%d") + '\', '
		insert += '\'' + admin_login + '\', '
		insert += '\'' + mysqlFormat(item['TITLE']) + '\', '
		insert += '\'\', ' if item['DESCRIPTION'] is None else '\'' + mysqlFormat(item['DESCRIPTION']) + '\', '
		insert += '1, '
		insert += '\'' + getUrl(item) + '\''
		insert += ');\n'
		insert += 'INSERT INTO ' + lang_table_name + ' (resourceId, languageId) VALUES ('
		insert += item['ID'] + ', '
		insert += str(languages[item['LANG']])
		insert += ');\n'
		# Link a type to a resource
		if item['CLASSEMENT_TYPE'] in types.keys() :
			insert += 'INSERT INTO ' + type_table_name + ' (resourceId, resourceTypeId) VALUES ('
			insert += item['ID'] + ', '
			insert += str(types[item['CLASSEMENT_TYPE']])
			insert += ');\n'
		else :
			if item['CLASSEMENT_TYPE'] not in types_deleted :
				logging.error('This type doesn\'t exist : ' + item['CLASSEMENT_TYPE'] + '.')
		# Link subjects to a resource
		for category in item['category'] :
			if category in subjects.keys() :
				insert += 'INSERT INTO ' + subject_table_name + ' (resourceId, generalDetailSubjectLinkID) VALUES ('
				insert += item['ID'] + ', '
				insert += str(subjects[category])
				insert += ');\n'
			else :
				if category not in subjects_deleted :
					logging.error('This category doesn\'t exist : ' + category + ' in item ' + item['ID'] + '.')
		# Set access type of a resource
		if item['access_type'][0] in accesses.keys() :
			insert += 'UPDATE ' + resource_table_name
			insert += ' SET authenticationTypeID = \'' + str(accesses[item['access_type'][0]]) + '\''
			insert += ' WHERE resourceID = ' + item['ID'] + ';\n'
		else :
			logging.error('This access doesn\'t exist : ' + item['access_type'][0] + ' in item ' + item['ID'] + '.')
	else :
		logging.error('The item length is not correct for item ' + item['ID'] + '\n')
	return insert

def writeFile(data) :
	f = open(result_file, 'w')
	f.write(data)

def main() :
	# Logging initiation routine
	log_folder = 'log'
	log_level = logging.DEBUG

	# Create log file path
	log_file = os.path.join(log_folder, sys.argv[0].replace('.py', '.log'))

	# Init logs
	logging.basicConfig(filename = log_file, filemode = 'w+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')

	# Empty the resources and languages tables
	result = ''
	result += 'TRUNCATE TABLE ' + resource_table_name + ';\n'
	result += 'TRUNCATE TABLE ' + lang_table_name + ';\n'
	result += 'TRUNCATE TABLE ResourceNote;\n'
	result += 'TRUNCATE TABLE ResourceOrganizationLink;\n'
	result += 'TRUNCATE TABLE ResourceRelationship;\n'
	result += 'TRUNCATE TABLE ResourceTuto;\n'
	result += 'TRUNCATE TABLE ResourceTypeLink;\n'
	result += 'TRUNCATE TABLE ResourceSubject;\n'

	# Load json file with data in english
	with open(json_en_file) as json_file :
		items = json.load(json_file)['items']
	for item in items :
		result += insertEnglishItem(item)

	# Load json file with data in french
	with open(json_fr_file) as json_file :
		items = json.load(json_file)['items']
	for item in items :
		result += insertFrenchItem(item)

	# Write SQL query in file
	writeFile(result.encode('utf-8'))
	logging.info('End')


#
# Main
#

if __name__ == '__main__':
	main()