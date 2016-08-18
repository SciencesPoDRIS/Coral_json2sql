# !/usr/bin/env python
# -*- coding: utf8 -*-
# Convert  a json file to an sql inser statement
# Execution example : python json2sql.py


#
# Libs
#

import time
import json


#
# Config
#

json_fr_file = 'data_fr.json'
json_en_file = 'data_en.json'
result_file = 'items.sql'
table_name = 'Resource'
admin_login = 'coral'


#
# Functions
#

def insertItem(item) :
	insert = ''
	insert += 'INSERT INTO ' + table_name + ' (createDate, createLoginID, titleText, descriptionText) VALUES ('
	insert += '\'' + time.strftime("%Y-%m-%d") + '\', '
	insert += '\'' + admin_login + '\', '
	insert += item['TITLE'] + ', '
	insert += item['DESCRIPTION'] + ', '
	insert += ');\n'
	return insert

def writeFile(data) :
	f = open(result_file, 'w')
	f.write(data)

def main() :
	# load json file with data in french
	with open(json_en_file) as json_file :
		items = json.load(json_file)['items']
	result = ''
	for item in items :
		result += insertItem(item)
	writeFile(result)


#
# Main
#

if __name__ == '__main__':
	main()