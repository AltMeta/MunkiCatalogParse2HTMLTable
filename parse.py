#! /usr/bin/env python
#
# Copyright University of Oxford
# Author
# Name: Gary Ballantine
# Email: gary.ballantine at it.ox.ac.uk
# GitHub: AltMeta

"""

"""

import codecs, plistlib
from distutils.version import LooseVersion

AppList = []

class App(object):

	def __init__(self, display_name, category, description):
		self.display_name = display_name
		self.category = category
		self.description = description
		self.recipe_name = ''
		self.version_catalog = {}
		self.catalog = []

class main():

	def ReadCatalogs(catalog):
		
		with open(catalog, 'rb') as fp:
			pl = plistlib.readPlist(fp)


		for x in range(len(pl)):
			extract = pl[x].pop
			
			try:
				display_name = extract('display_name')
			except:
				display_name = ''
			try:
				category = extract('category')
			except:
			        category = ''
			try:
			        description = extract('description')
			except:
			        description = ''
			try:
			        version = extract('version')
			except:
				version = ''

			appobject = App(display_name,category,description)
			appobject.catalog.append(catalog)


			if not 'stable' in appobject.version_catalog:
				appobject.version_catalog[ 'stable' ] = []
			if not 'unstable' in appobject.version_catalog:
				appobject.version_catalog[ 'unstable' ] = []
			if not 'testing' in appobject.version_catalog:
				appobject.version_catalog[ 'testing' ] = []

			appobject.version_catalog[ catalog ].append(version)

			if len(AppList) == 0:
				AppList.append(appobject)

			NameMatch = 0

			for y in range(len(AppList)):
				if appobject.display_name == AppList[y].display_name:
					NameMatch = 1
					if appobject.version_catalog[ catalog ] > AppList[y].version_catalog[ catalog ]:
						#The Category and Description are set to the contents of the latest version
						AppList[y].category = appobject.category
						AppList[y].description = appobject.description
						AppList[y].version_catalog[ catalog ].append(version)

			if NameMatch == 0:
				AppList.append(appobject)

	def WriteHTMLTable():

		#TODO Add some nice templating stuff so this isn't so ugly

		w = codecs.open('software.html', 'w', 'utf-8')

		w.write('<table border="1" style="width:100%"> \n')
		w.write('  <tr>\n')
		w.write('    <th>Display Name</th>\n')
		w.write('    <th>Category</th>\n')
		w.write('    <th>Description</th>\n')
		w.write('    <th>Recipe Name</th>\n')
		w.write('    <th>Override Name</th>\n')
		w.write('    <th>Stable Versions</th>\n')
		w.write('    <th>Testing Versions</th>\n')
		w.write('    <th>Unstable Versions</th>\n')
		w.write('  </tr>\n')

		for i in AppList:
			w.write('  <tr>\n')
			w.write('      <th>' + i.display_name + '</th>\n')
			w.write('      <th>' + i.category + '</th>\n')
			w.write('      <th>' + i.description + '</th>\n')
			w.write('      <th> Feature Request </th>\n')
			w.write('      <th> Feature Request </th>\n')
			w.write('      <th>' + str(i.version_catalog[ 'stable' ]) + '</th>\n')
			w.write('      <th>' + str(i.version_catalog[ 'testing' ]) + '</th>\n')
			w.write('      <th>' + str(i.version_catalog[ 'unstable' ]) + '</th>\n')
		w.write('</table>')
		w.close()

	ReadCatalogs('stable')
	ReadCatalogs('unstable')
	ReadCatalogs('testing')
	WriteHTMLTable()
