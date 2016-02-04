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
	- List all versions in the catalog, not just the newest

"""

import plistlib, codecs
from distutils.version import LooseVersion

with open('stable', 'rb') as fp:
	pl = plistlib.readPlist(fp)
app = []


w = codecs.open('software.html', 'w', 'utf-8')


w.write('<table border="1" style="width:100%"> \n')
w.write('  <tr>\n')
w.write('     <th>Display Name</th>\n')
w.write('     <th>Category</th>\n')
w.write('     <th>Description</th>\n')
w.write('     <th>Version</th>\n')
w.write('  </tr>\n')

for x in range(len(pl)):
	software = pl[x].pop
	try:
		app.append(software('display_name') + '|' + software('category') + '|' + software('description') + '|' + software('version'))
	except:
		pass

for x in range(len(app)):
	display_name =  app[x].split('|')[0]
	category = app[x].split('|')[1]
	description = app[x].split('|')[2]
	version = app[x].split('|')[3]
	match = 0
	ver = 0

	for y in range(len(app)):
		cdisplay_name =  app[y].split('|')[0]
		cversion = app[y].split('|')[3]
		if x != y:
			if display_name == cdisplay_name:
				match = 1
				if LooseVersion(cversion) > LooseVersion(version):
					ver = 1
	if ver == 0 or match == 0:	
		w.write('  <tr>\n')
		w.write('     <th>' + display_name + '</th>\n')
		w.write('     <th>' + category + '</th>\n')
		w.write('     <th>' + description + '</th>\n')
		w.write('     <th>' + version + '</th>\n')

w.write('</table>')
w.close()
