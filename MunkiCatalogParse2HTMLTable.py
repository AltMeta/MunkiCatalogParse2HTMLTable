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
		self.local_identifier = recipesearch(display_name, '/srv/autopkg/Recipes')
		self.remote_identifier = recipesearch(display_name, '/srv/autopkg/RecipeRepos')
		self.override_identifier = recipesearch(display_name, '/srv/autopkg/RecipeOverrides')
		

def recipesearch(display_name, path):

	identifier = []

	for dirpath, dirnames, filenames in os.walk(path):
		for x in filenames:
			if re.search(display_name, x):
				try:
					with open(dirpath + '/' + x, 'rb') as fp:
						pl = plistlib.readPlist(fp)
					identifier.append(pl["Identifier"])
				except:
					pass

	return identifier


def main():

	w = codecs.open('software.html', 'w', 'utf-8')

	w.write('<table border="1" style="width:100%"> \n')
	w.write('  <tr>\n')
	w.write('     <th>Display Name</th>\n')
	w.write('     <th>Category</th>\n')
	w.write('     <th>Description</th>\n')
	w.write('     <th>Recipe Identifier</th>\n')
	w.write('     <th>Override Identifier</th>\n')
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
			w.write('     <th>' + str(catalog[x].local_identifier) + str(catalog[x].remote_identifier) + '</th>\n')
			w.write('     <th>' + str(catalog[x].override_identifier) + '</th>\n')
			w.write('     <th>' + str(catalog[x].version) + '</th>\n')
	w.write('</table>')
	w.close()

if __name__ == '__main__':
	main()
