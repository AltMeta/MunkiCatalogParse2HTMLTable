#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Univeristy of Oxford
# Author
# Name: Gary Ballantine
# Email: gary.ballantine at it.ox.ac.uk
# Github: AltMeta
"""
MunkiCatalogParse2HTMLTable

Initial Version of a python script to parse a munki catalog
and output the desired information into an HTML table.

TODO:
	- Add a column to list if the pkg was built by autopkg inc. date and version of last package
	- Add columns for recipe names and override names

"""

import plistlib, codecs, re, os
from distutils.version import LooseVersion

class Software:
	'common base class for all software'

	def __init__(self, display_name, category, description, version):
		self.display_name = display_name
		self.category = category
		self.description = description
		self.version = [version]

def recipesearch():

	f = open('MunkiCatalogParse2HTMLTable.conf', 'r')

	for i in f:
		if re.search('overridesdir=', i):
			overridesdir = i.split('=')[1]
		elif re.search('localdir=', i):
			localdir = i.split('=')[1]
		elif re.search('repodir=', i);
			repodir = i.split('=')[1]
	
	for dirpath, dirnames, filenames in os.walk(localdir):
		for x in filenames:
			print dirpath + '/' + x 
			#Will do some regex later to search for Display Name


def main():

	w = codecs.open('software.html', 'w', 'utf-8')

	w.write('<table border="1" style="width:100%"> \n')
	w.write('  <tr>\n')
	w.write('     <th>Display Name</th>\n')
	w.write('     <th>Category</th>\n')
	w.write('     <th>Description</th>\n')
	w.write('     <th>Recipe Name</th>\n')
	w.write('     <th>Override Name</th>\n')
	w.write('     <th>Version</th>\n')
	w.write('  </tr>\n')

	with open('stable', 'rb') as fp:
		pl = plistlib.readPlist(fp)
	catalog = []

	for x in range(len(pl)):
		info = pl[x].pop
	
		try:
			display_name = info('display_name')
		except:
			display_name = 'fail'
		try:
			category = info('category')
		except:
			category = 'fail'
		try:
			description = info('description')
		except:
			description = 'fail'
		try:
			version = info('version')
		except:
			version = '0'


		catalog.append(Software(display_name,category,description,version))

	for x in range(len(catalog)):
		for y in range(len(catalog)):
			if x != y:
				if catalog[x].display_name != 'done':
					if catalog[x].display_name == catalog[y].display_name:
						if catalog[x].category == 'fail':
							catalog[x].category = catalog[y].category
						if catalog[x].description == 'fail':
							catalog[x].description = catalog[y].category
						catalog[x].version.append(catalog[y].version)
						catalog[y].display_name = 'done'

	for x in range(len(catalog)):
		if catalog[x].display_name != 'done':
			w.write('  <tr>\n')
			w.write('     <th>' + catalog[x].display_name + '</th>\n')
			w.write('     <th>' + catalog[x].category + '</th>\n')
			w.write('     <th>' + catalog[x].description + '</th>\n')
			w.write('     <th>' + str(catalog[x].version) + '</th>\n')
	w.write('</table>')
	w.close()

if __name__ == '__main__':
	main()
