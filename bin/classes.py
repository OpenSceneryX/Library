#!/usr/local/bin/python
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
import sys
import re


#
# Class to hold configuration values
#
class Configuration:
	"""Generic container for shared variables."""
	versionTag = ""
	versionNumber = ""
	versionDate = datetime.datetime.now().strftime("%c")
	
	def setVersionTag(self, versionTag):
		""" Set up the configuration """
		self.versionTag = versionTag
		self.versionNumber = string.replace(self.versionTag, "-", ".")
		self.releaseFolder = "tags/" + self.versionNumber
		self.osxFolder = self.releaseFolder + "/OpenSceneryX-" + self.versionNumber
		self.osxDeveloperPackFolder = self.releaseFolder + "/OpenSceneryX-DeveloperPack-" + self.versionNumber
		self.osxPlaceholderFolder = self.osxDeveloperPackFolder + "/OpenSceneryX-Placeholder-" + self.versionNumber
		self.osxWebsiteFolder = self.releaseFolder + "/OpenSceneryX-Website-" + self.versionNumber
		self.supportFolder = "trunk/support"
		
	def makeFolders(self):
		""" Create any folders that need creating """
		if not os.path.isdir(self.releaseFolder):
			os.mkdir(self.releaseFolder)
		if not os.path.isdir(self.osxFolder):
			os.mkdir(self.osxFolder)
		if not os.path.isdir(self.osxFolder + "/doc"):
			os.mkdir(self.osxFolder + "/doc")
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

	setVersionTag = classmethod(setVersionTag)
	makeFolders = classmethod(makeFolders)
	


#
# Class to hold information about an X-Plane scenery object
#
class SceneryObject:
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
		self.email = ""
		self.textureEmail = ""
		self.conversionEmail = ""
		self.url = ""
		self.textureUrl = ""
		self.conversionUrl = ""
		self.height = ""
		self.width = ""
		self.depth = ""
		self.note = ""
		self.description = ""
		
		self.virtualPaths = []
		self.deprecatedVirtualPaths = []
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


#
# Class to hold information about a category
#
class SceneryCategory:
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
			self.title = "Home"
			self.url = "/"
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

			self.url = "/doc/c_" + self.title + ".html"

		
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
class SceneryTexture:
	"""A scenery texture"""
	
	def __init__(self, filePath):
		self.fileName = os.path.basename(filePath)
		self.sceneryObjects = []


#
# A general build error
#
class BuildError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
