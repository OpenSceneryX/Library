#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2007 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
# If this script is used to generate a scenery library other than OpenSceneryX, recognition MUST be given
# to the author in any documentation accompanying the library.

# classes.py
# Classes
# Version: $Revision$

import datetime
import string
import os
import re
import traceback

from TOC import TOC

#
# Class to hold configuration values
#
class Configuration(object):
	"""Generic container for shared variables."""
	versionTag = ""
	sinceVersionTag = ""
	versionNumber = ""
	versionDate = datetime.datetime.now().strftime("%a, %d %b %Y")
	
	def init(self, versionTag, sinceVersionTag, buildPDF):
		""" Set up the configuration """
		self.versionTag = versionTag
		self.sinceVersionTag = sinceVersionTag
		self.versionNumber = string.replace(self.versionTag, "-", ".")
		self.releaseFolder = "builds/" + self.versionNumber
		self.osxFolder = self.releaseFolder + "/OpenSceneryX-" + self.versionNumber
		self.osxDeveloperPackFolder = self.releaseFolder + "/OpenSceneryX-DeveloperPack-" + self.versionNumber
		self.osxPlaceholderFolder = self.osxDeveloperPackFolder + "/OpenSceneryX-Placeholder-" + self.versionNumber
		self.osxWebsiteFolder = self.releaseFolder + "/OpenSceneryX-Website-" + self.versionNumber
		self.supportFolder = "support"
		self.buildPDF = (buildPDF == "Y" or buildPDF == "y")
		if (self.buildPDF): self.developerPDF = OpenSceneryXPDF("P", "mm", "A4", "OpenSceneryX Developer Reference", self.versionNumber)
		
	def makeFolders(self):
		""" Create any folders that need creating """
		if not os.path.isdir(self.releaseFolder):
			os.mkdir(self.releaseFolder)
		if not os.path.isdir(self.osxFolder):
			os.mkdir(self.osxFolder)
		if not os.path.isdir(self.osxFolder + "/doc"):
			os.mkdir(self.osxFolder + "/doc")
		if not os.path.isdir(self.osxFolder + "/placeholders/invisible"):
			os.makedirs(self.osxFolder + "/placeholders/invisible")
		if not os.path.isdir(self.osxFolder + "/placeholders/visible"):
			os.makedirs(self.osxFolder + "/placeholders/visible")
		if not os.path.isdir(self.osxFolder + "/opensceneryx"):
			os.makedirs(self.osxFolder + "/opensceneryx")
		if not os.path.isdir(self.osxDeveloperPackFolder):
			os.mkdir(self.osxDeveloperPackFolder)
		if not os.path.isdir(self.osxDeveloperPackFolder + "/doc"):
			os.mkdir(self.osxDeveloperPackFolder + "/doc")
		if not os.path.isdir(self.osxPlaceholderFolder):
			os.mkdir(self.osxPlaceholderFolder)
		if not os.path.isdir(self.osxPlaceholderFolder + "/opensceneryx"):
			os.mkdir(self.osxPlaceholderFolder + "/opensceneryx")
		if not os.path.isdir(self.osxWebsiteFolder):
			os.mkdir(self.osxWebsiteFolder)
		if not os.path.isdir(self.osxWebsiteFolder + "/doc"):
			os.mkdir(self.osxWebsiteFolder + "/doc")
		if not os.path.isdir(self.osxWebsiteFolder + "/extras"):
			os.mkdir(self.osxWebsiteFolder + "/extras")
		
		if os.path.lexists('builds/latest'):
			os.unlink('builds/latest')
		if os.path.lexists('builds/latest-website'):
			os.unlink('builds/latest-website')
		if os.path.lexists('builds/latest-library'):
			os.unlink('builds/latest-library')
			
		os.symlink(self.versionNumber, 'builds/latest')
		os.symlink(self.versionNumber + "/OpenSceneryX-Website-" + self.versionNumber, 'builds/latest-website')
		os.symlink(self.versionNumber + "/OpenSceneryX-" + self.versionNumber, 'builds/latest-library')
		
	init = classmethod(init)
	makeFolders = classmethod(makeFolders)
	


#
# Class to hold information about an X-Plane scenery object
#
class SceneryObject(object):
	"""An X-Plane scenery object"""
	
	def __init__(self, filePathRoot, fileName):
		self.filePathRoot = filePathRoot
		self.fileName = fileName
		self.infoFilePath = ""
		self.screenshotFilePath = ""
		self.logoFileName = ""

		self.sceneryCategory = None
		
		self.title =""
		self.shortTitle = ""
		self.author = ""
		self.textureAuthor = ""
		self.conversionAuthor = ""
		self.modificationAuthor = ""
		self.email = ""
		self.textureEmail = ""
		self.conversionEmail = ""
		self.modificationEmail = ""
		self.url = ""
		self.textureUrl = ""
		self.conversionUrl = ""
		self.modificationUrl = ""
		self.height = ""
		self.width = ""
		self.depth = ""
		self.note = ""
		self.since = "0.0.0"
		self.description = ""
		
		self.virtualPaths = []
		self.deprecatedVirtualPaths = []
		self.externalVirtualPaths = []
		self.sceneryTextures = []
		
		self.tutorial = 0
		self.animated = 0
		
		self.exportPropagate = -1
		
		self.creationDate = None
		self.modificationDate = None


	def getFilePath(self):
		""" Get the full file path to this SceneryObject """
		return os.path.join(self.filePathRoot, self.fileName)

	def __cmp__(self, other):
		""" Standard compare method for sorting - compare titles """
		if (isinstance(other, SceneryObject)): 
			return cmp(self.title, other.title)
		else:
			return cmp(self.title, other)
	
	def getDocumentationFileName(self):
		""" Get the filename of this SceneryObject's documentation file """
		return self.title + ".html"

	def getWebURL(self, includeDomain = True):
		""" Get the website URL for this SceneryObject """
		if includeDomain:
			return "https://www.opensceneryx.com/" + self.filePathRoot + "/"
		else:
			return self.filePathRoot + "/"

#
# Class to hold information about an X-Plane polygon
#
class Polygon(SceneryObject):
	"""An X-Plane Polygon"""
	
	def __init__(self, filePathRoot, fileName):
		super(Polygon, self).__init__(filePathRoot, fileName)
		
		self.scaleH = ""
		self.scaleV = ""
		self.layerGroupName = ""
		self.layerGroupOffset = ""
		self.surfaceName = ""
		

#
# Class to hold information about a category
#
class SceneryCategory(object):
	"""A scenery documentation category"""
	
	def __init__(self, filePathRoot, parentSceneryCategory):
		self.filePathRoot = filePathRoot
		self.title = ""
		self.url = None
		self.childSceneryCategories = []
		self.childSceneryObjects = []
		self.parentSceneryCategory = parentSceneryCategory
		self.calculateDepth()
		
		if parentSceneryCategory == None:
			self.title = "Catalogue"
			self.url = "/catalogue"
		else:
			file = open(os.path.join(filePathRoot, "category.txt"))
			fileContents = file.readlines()
			file.close()
		
			# define the regex patterns:
			titlePattern = re.compile("Title:\s+(.*)")
			
			for line in fileContents:
				result = titlePattern.match(line)
				if result:
					self.title = result.group(1).replace("\"", "'")
					continue

			parts = filePathRoot.split(os.sep, 1)
			self.url = os.path.join('/', parts[1])

		
	def addSceneryCategory(self, sceneryCategory):
		""" Add a sub SceneryCategory to this category """
		self.childSceneryCategories.append(sceneryCategory)
		sceneryCategory.parentSceneryCategory = self

	def addSceneryObject(self, sceneryObject):
		""" Add a SceneryObject to this category """
		self.childSceneryObjects.append(sceneryObject)
		sceneryObject.sceneryCategory = self

	def getSceneryObjects(self, recursive):
		""" Get our list of SceneryObjects, recursively if desired """
		
		# Clone our own list of objects
		result = self.childSceneryObjects[:]
		# Merge with objects from children
		if recursive:
			for sceneryCategory in self.childSceneryCategories:
				result = map(None, result, sceneryCategory.getSceneryObjects(recursive))
			
		return result
		
	def getSceneryObjectCount(self, recursive):
		""" Get the number of SceneryObjects in this category, recursively if desired """
		result = len(self.childSceneryObjects)
		
		if recursive:
			for sceneryCategory in self.childSceneryCategories:
				result = result + sceneryCategory.getSceneryObjectCount(recursive)
		
		return result
	
	def getAncestors(self, includeSelf):
		""" Get a list of our ancestors, with the root category at the end of the list """
		result = []
		
		if (includeSelf):
			currentSceneryCategory = self
		else:
			currentSceneryCategory = self.parentSceneryCategory
		
		while (currentSceneryCategory != None):
			result.append(currentSceneryCategory)
			currentSceneryCategory = currentSceneryCategory.parentSceneryCategory
		
		return result
	
	def calculateDepth(self):
		""" Calculate our depth down the category tree """
		self.depth = 0
		currentSceneryCategory = self
		
		while (currentSceneryCategory != None):
			self.depth = self.depth + 1
			currentSceneryCategory = currentSceneryCategory.parentSceneryCategory
	
	def sort(self):
		""" Sort our children, both SceneryCategories and SceneryObjects """
		self.childSceneryCategories.sort()
		self.childSceneryObjects.sort()
		
		for sceneryCategory in self.childSceneryCategories:
			sceneryCategory.sort()
			
	def __cmp__(self, other):
		""" Standard compare method for sorting - compares titles """
		if (isinstance(other, SceneryCategory)): 
			return cmp(self.title, other.title)
		else:
			return cmp(self.title, other)


#
# Class to hold information about a texture
#
class SceneryTexture(object):
	"""A scenery texture"""
	
	def __init__(self, filePath):
		self.fileName = os.path.basename(filePath)
		self.sceneryObjects = []


#
# Subclass of TOC to handle our bespoke header and footer
#
class OpenSceneryXPDF(TOC):
	""" Subclass of PDF to customise OpenSceneryX PDF output """
	columns = 2
	current_column = 1
	column_gutter = 3
	
	def __init__(self, orientation="P", unit="mm", format="A4", title="", version="", columns=2):
		""" Custom constructor """
		
		# Call superclass constructor
		TOC.__init__(self, orientation, unit, format)
		
		# Create an alias for the total number of pages in the document
		self.alias_nb_pages()

		self.title = title
		self.version = "Version: " + version
		self.columns = columns

		if (not os.path.exists(os.getcwd() + '/font/DejaVuSansCondensed.ttf') or not os.path.exists(os.getcwd() + '/font/DejaVuSansCondensed-Bold.ttf')):
			raise RuntimeError("TTF Font files 'DejaVuSansCondensed.ttf' and 'DejaVuSansCondensed-Bold.ttf' required at path : %s" % os.getcwd() + '/font')

		self.add_font('DejaVu', '', os.getcwd() + '/font/DejaVuSansCondensed.ttf', uni=True)
		self.add_font('DejaVu', 'B', os.getcwd() + '/font/DejaVuSansCondensed-Bold.ttf', uni=True)
		
		# Generate title page
		self.add_page()
		
		# Image
		imagewidth = self.w
		pagewidth = self.w - self.r_margin - self.x
		xpos = (pagewidth - imagewidth) / 2.0 + self.l_margin
		self.image("../" + Configuration.supportFolder + "/x_banner_print.png", xpos, 100, imagewidth, 0, "PNG", "https://www.opensceneryx.com")
		
		# Text
		self.set_text_color(255, 255, 255)
		self.set_y(113)
		self.set_font("DejaVu", "B", 16)
		self.cell(0, 10, self.title, 0, 1, "C")
		self.set_font("DejaVu", "B", 10)
		self.cell(0, 10, self.version, 0, 1, "C")
		self.set_text_color(0)
				
		# Generate first normal page
		self.add_page()

		self.start_page_nums()


	def get_column_x(self):
		available_width = self.w - self.l_margin - self.r_margin - ((self.columns - 1) * self.column_gutter)
		column_width = available_width / float(self.columns)
		
		return self.l_margin + ((self.current_column - 1) * (column_width + self.column_gutter))

		
	def ln(self, h=''):
		""" Overridden to use column x rather than page x """
		
		self.x=self.get_column_x()
		if(isinstance(h, basestring)):
			self.y+=self.lasth
		else:
			self.y+=h


	def cell(self, w, h=0, txt='', border=0, ln=0, align='', fill=0, link=''):
		""" Overridden to start next column if appropriate """
		
		if (self.y + h > self.page_break_trigger and not self.in_footer):
			if (self.current_column < self.columns):
				# Column break
				self.current_column += 1
				self.x=self.get_column_x()
				self.y=self.t_margin + 15
			else:
				# Page break
				self.current_column = 1
				self.x=self.get_column_x()
			
		TOC.cell(self, w, h, txt, border, ln, align, fill, link)
		
		
	def add_page(self, orientation=''):
		""" Overridden to handle columns on new page """

		self.current_column = 1
		self.x=self.get_column_x()
		self.y=self.t_margin + 15
		TOC.add_page(self, orientation)
	
	
	def new_column(self):
	
		if (self.current_column < self.columns):
			self.current_column += 1
			self.x=self.get_column_x()
			self.y=self.t_margin + 15
		else:
			self.add_page()
			

	def header(self):
		""" Custom header """
		
		# Don't output on the first page
		if (self.page_no() == 1): return;
		
		# Image
		self.image("../" + Configuration.supportFolder + "/x_print.png", self.l_margin, self.t_margin, 5, 0, "PNG", "https://www.opensceneryx.com")

		# Text
		self.set_font("DejaVu", "B", 8)
		self.set_y(self.t_margin + 2.3)
		self.set_x(self.l_margin + 5)
		self.cell(0, 0, self.title)
		self.cell(0, 0, self.version, 0, 0, "R")
		
		# Line break, to ensure the page content starts in the correct place
		self.ln(15)


	def footer(self):
		""" Custom footer """

		# Don't output on the first page
		if (self.page_no() == 1): return;
		if (self.in_toc == 1): return;
		
		self.set_font("DejaVu", "B", 8)
		self.set_y(-self.b_margin)
		self.cell(0, 0, "Page %s" % self.num_page_no(), 0, 0, "R")


#
# A general build error
#
class BuildError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
