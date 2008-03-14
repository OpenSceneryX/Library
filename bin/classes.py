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
	"Generic container for shared variables."
	versionTag = ""
	versionNumber = ""
	versionDate = datetime.datetime.now().strftime("%c")
	
	def setVersionTag(self, versionTag):
		self.versionTag = versionTag
		self.versionNumber = string.replace(self.versionTag, "-", ".")
		self.releaseFolder = "tags/" + self.versionNumber
		self.osxFolder = self.releaseFolder + "/OpenSceneryX-" + self.versionNumber
		self.osxDeveloperPackFolder = self.releaseFolder + "/OpenSceneryX-DeveloperPack-" + self.versionNumber
		self.osxPlaceholderFolder = self.osxDeveloperPackFolder + "/OpenSceneryX-Placeholder-" + self.versionNumber
		self.osxWebsiteFolder = self.releaseFolder + "/OpenSceneryX-Website-" + self.versionNumber
		
	def makeFolders(self):
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

	setVersionTag = classmethod(setVersionTag)
	makeFolders = classmethod(makeFolders)
	


#
# Class to hold information about an X-Plane scenery object
#
class SceneryObject:
	"An X-Plane scenery object"
	
	def __init__(self, filePathRoot, fileName):
		self.filePathRoot = filePathRoot
		self.fileName = fileName
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
		self.description = ""
		self.virtualPaths = []
		self.tutorial = 0
		self.animated = 0
		self.exportPropagate = -1
		self.infoFilePath = ""
		self.screenshotFilePath = ""
		self.deprecatedVirtualPaths = []
		self.sceneryTextures = []

	def getFilePath(self):
		return os.path.join(self.filePathRoot, self.fileName)

	def __cmp__(self, other):
		return cmp(self.title, other.title)
	
	def getDocumentationFileName(self):
		return self.title + ".html"


#
# Class to hold information about a category
#
class SceneryCategory:
	"A scenery documentation category"
	
	def __init__(self, filePathRoot):
		self.filePathRoot = filePathRoot
		self.title = ""
		self.childSceneryCategories = []
		self.childSceneryObjects = []
		
		if filePathRoot == "":
			self.title = "Root"
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

		
	def addSceneryCategory(self, sceneryCategory):
		self.childSceneryCategories.append(sceneryCategory)

	def addSceneryObject(self, sceneryObject):
		self.childSceneryObjects.append(sceneryObject)

	def getSceneryObjects(self, recursive):
		# Clone our own list of objects
		result = self.childSceneryObjects[:]
		# Merge with objects from children
		if recursive:
			for sceneryCategory in self.childSceneryCategories:
				result = map(None, result, sceneryCategory.getSceneryObjects(recursive))
			
		return result
		
	def getSceneryObjectCount(self, recursive):
		result = len(self.childSceneryObjects)
		
		if recursive:
			for sceneryCategory in self.childSceneryCategories:
				result = result + sceneryCategory.getSceneryObjectCount(recursive)
		
		return result
		
	def sort(self):
		self.childSceneryCategories.sort()
		self.childSceneryObjects.sort()
		
		for sceneryCategory in self.childSceneryCategories:
			sceneryCategory.sort()
			
	def __cmp__(self, other):
		return cmp(self.title, other.title)


#
# Class to hold information about a texture
#
class SceneryTexture:
	"A scenery texture"
	
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
