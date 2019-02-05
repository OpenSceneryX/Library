# -*- coding: utf-8 -*-
# Copyright (c) 2007 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
# If this script is used to generate a scenery library other than OpenSceneryX, recognition MUST be given
# to the author in any documentation accompanying the library.

# functions.py
# Common functions
# Version: $Revision$

import os
import shutil
import re
import urllib
import classes
import fnmatch
import sys
import random

from distutils.version import LooseVersion
from colorama import Fore, Style

try:
	from PIL import Image

except ImportError:
	Image = None

# Global regex patterns
exportPattern = re.compile("Export:\s+(.*)")
titlePattern = re.compile("Title:\s+(.*)")
shortTitlePattern = re.compile("Short Title:\s+(.*)")
authorPattern = re.compile("Author:\s+(.*)")
textureAuthorPattern = re.compile("Author, texture:\s+(.*)")
conversionAuthorPattern = re.compile("Author, conversion:\s+(.*)")
modificationAuthorPattern = re.compile("Author, modifications:\s+(.*)")
widthPattern = re.compile("Width:\s+(.*)")
heightPattern = re.compile("Height:\s+(.*)")
depthPattern = re.compile("Depth:\s+(.*)")
descriptionPattern = re.compile("Description:\s+(.*)")
excludePattern = re.compile("Exclude:\s+(.*)")
animatedPattern = re.compile("Animated:\s+(.*)")
exportPropagatePattern = re.compile("Export Propagate:\s+(.*)")
exportDeprecatedPattern = re.compile("Export Deprecated v(.*):\s+(.*)")
exportExternalPattern = re.compile("Export External (.*):\s+(.*)")
exportExtendedPattern = re.compile("Export Extended:\s+(.*)")
logoPattern = re.compile("Logo:\s+(.*)")
notePattern = re.compile("Note:\s+(.*)")
sincePattern = re.compile("Since:\s+(.*)")
# Texture patterns
v8TexturePattern = re.compile("TEXTURE\s+(.*)")
v8LitTexturePattern = re.compile("TEXTURE_LIT\s+(.*)")
v9NormalTexturePattern = re.compile("TEXTURE_NORMAL\s+(.*)")
v8PolygonTexturePattern = re.compile("(?:TEXTURE|TEXTURE_NOWRAP)\s+(.*)")
polygonNormalTexturePattern = re.compile("(?:TEXTURE_NORMAL|TEXTURE_NORMAL_NOWRAP)\s+(?:.*?)\s+(.*)")
# Polygon patterns
scalePattern = re.compile("(?:SCALE)\s+(.*?)\s+(.*)")
layerGroupPattern = re.compile("(?:LAYER_GROUP)\s+(.*?)\s+(.*)")
surfacePattern = re.compile("(?:SURFACE)\s+(.*)")


def buildCategoryLandingPages(sitemapXMLFileHandle, sceneryCategory):
	""" Build all the documentation landing pages for SceneryCategories """

	# Only build landing pages where depth >= 2
	if sceneryCategory.depth >= 2:
		txtFileContent = ""
		txtFileContent += "Title: " + sceneryCategory.title + "\n"
		txtFileContent += "===============\n"

		# Content

		# Sub-categories in this category
		if len(sceneryCategory.childSceneryCategories) > 0:
			for childSceneryCategory in sceneryCategory.childSceneryCategories:
				txtFileContent += "Sub-category: \"" + childSceneryCategory.title + "\" \"" + childSceneryCategory.url + "\"\n"

		# Objects in this category
		if len(sceneryCategory.getSceneryObjects(0)) > 0:
			for sceneryObject in sceneryCategory.getSceneryObjects(0):
				txtFileContent += "Item: \"" + sceneryObject.title + "\" \"" + sceneryObject.filePathRoot + "\"\n"

		txtFileHandle = open(classes.Configuration.osxWebsiteFolder + sceneryCategory.url + os.sep + "category.txt", "w")
		txtFileHandle.write(txtFileContent)
		txtFileHandle.close()

		# XML sitemap entry
		writeXMLSitemapEntry(sitemapXMLFileHandle, sceneryCategory.url + "/", str(1 - 0.1 * (sceneryCategory.depth - 1)))

	# Recurse
	children = sceneryCategory.childSceneryCategories
	for childCategory in children:
		buildCategoryLandingPages(sitemapXMLFileHandle, childCategory)



def handleFolder(dirPath, currentCategory, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, authors, textures, toc, latest):
	""" Parse the contents of a library folder """

	contents = os.listdir(dirPath)

	# Handle category descriptor first, if present
	if "category.txt" in contents:
		currentCategory = handleCategory(dirPath, currentCategory)

	for item in contents:
		fullPath = os.path.join(dirPath, item)

		if (item == "object.obj"):
			handleObject(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest)
			continue
		elif (item == "facade.fac"):
			handleFacade(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest)
			continue
		elif (item == "forest.for"):
			handleForest(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest)
			continue
		elif (item == "line.lin"):
			handleLine(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest)
			continue
		elif (item == "polygon.pol"):
			handlePolygon(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest)
			continue
		elif (item == "category.txt"):
			# Do nothing
			continue
		elif os.path.isdir(fullPath):
			if not item == ".svn":
				handleFolder(fullPath, currentCategory, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, authors, textures, toc, latest)



def handleCategory(dirpath, currentCategory):
	""" Create an instance of the SceneryCategory class """

	sceneryCategory = classes.SceneryCategory(dirpath, currentCategory)
	currentCategory.addSceneryCategory(sceneryCategory)

	parts = dirpath.split(os.sep, 1)
	if not createPaths(parts): return

	return sceneryCategory



def handleObject(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest):
	""" Create an instance of the SceneryObject class for a .obj """

	global v8TexturePattern, v8LitTexturePattern, v9NormalTexturePattern

	mainobjectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 1)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[1], filename)

	# Locate and check whether the support files exist
	if not checkSupportFiles(mainobjectSourcePath, dirpath, sceneryObject): return

	# Set up paths
	if not createPaths(parts): return

	# Build a list containing (filePath, filename) tuples, including seasonal variants
	objectSourcePaths = []
	objectSourcePaths.append((mainobjectSourcePath, filename))
	objectSeasonPaths = {}

	for season in classes.Configuration.seasons:
		seasonFilename = "object_" + season + ".obj"
		seasonSourcePath = os.path.join(dirpath, seasonFilename)
		if os.path.isfile(seasonSourcePath):
			objectSeasonPaths[season] = sceneryObject.getFilePath(seasonFilename)
			objectSourcePaths.append((seasonSourcePath, seasonFilename))
			displayMessage("S")

	for objectSourcePath, objectFilename in objectSourcePaths:
		# Copy the object file
		shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[1], objectFilename))

		# Open the object
		file = open(objectSourcePath, "rU")
		objectFileContents = file.readlines()
		file.close()

		textureFound = 0
		lineNumber = 1

		for line in objectFileContents:
			result = v8TexturePattern.match(line)
			if result:
				textureFound = textureFound + 1
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if (result.group(1) == ""):
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Object (v8) specifies a blank texture - valid but may not be as intended\n", "warning")
				elif os.path.isfile(textureFile):

					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					lastSlash = result.group(1).rfind("/")
					if (lastSlash > -1):
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)[0:lastSlash])
					else:
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1])
					if not os.path.isdir(destinationTexturePath):
						# Create destination texture path if it doesn't already exist
						os.makedirs(destinationTexturePath)
					if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1))):
						# Copy texture if it doesn't already exist
						shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find texture - object (v8) excluded (" + textureFile + ")\n", "error")
					return

				# Break loop if we've found both v8 textures
				if textureFound == 2:
					break

			result = v8LitTexturePattern.match(line)
			if result:
				textureFound = textureFound + 1
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if os.path.isfile(textureFile):

					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find LIT texture - object (v8) excluded (" + textureFile + ")\n", "error")
					return

				# Break loop if we've found both v8 textures
				if textureFound == 2:
					break

			result = v9NormalTexturePattern.match(line)
			if result:
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if os.path.isfile(textureFile):

					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find NORMAL texture - object (v9) excluded (" + textureFile + ")\n", "error")
					return

			lineNumber += 1

		if textureFound == 0:
			displayMessage("\n" + objectSourcePath + "\n")
			displayMessage("No texture line in file - this error must be corrected\n", "error")
			return

	# Handle the info.txt file
	if not handleInfoFile(mainobjectSourcePath, dirpath, parts, ".obj", sceneryObject, authors, latest): return

	# Copy files
	if not copySupportFiles(mainobjectSourcePath, dirpath, parts, sceneryObject): return

	# Object is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	toc.append(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")
		for season in classes.Configuration.seasons:
			if season in objectSeasonPaths:
				# We have a seasonal virtual path for this season
				librarySeasonFileHandles[season].write("EXPORT_EXCLUDE opensceneryx/" + virtualPath + " " + objectSeasonPaths[season] + "\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryDeprecatedFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryDeprecatedFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")
	for (virtualPath, externalLibrary) in sceneryObject.externalVirtualPaths:
		libraryExternalFileHandle.write("EXPORT_BACKUP " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
	for virtualPath in sceneryObject.extendedVirtualPaths:
		if (virtualPath.startswith("lib/airport/aircraft")):
			libraryExtendedSAFileHandle.write("EXPORT_EXTEND " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		else:
			displayMessage("Unhandled EXPORT_EXTEND for " + virtualPath + "\n", "error")



def handleFacade(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest):
	""" Create an instance of the SceneryObject class for a .fac """

	global v8TexturePattern

	mainobjectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 1)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[1], filename)

	# Locate and check whether the support files exist
	if not checkSupportFiles(mainobjectSourcePath, dirpath, sceneryObject): return

	# Set up paths
	if not createPaths(parts): return

	# Build a list containing (filePath, filename) tuples, including seasonal variants
	objectSourcePaths = []
	objectSourcePaths.append((mainobjectSourcePath, filename))
	objectSeasonPaths = {}

	for season in classes.Configuration.seasons:
		seasonFilename = "facade_" + season + ".fac"
		seasonSourcePath = os.path.join(dirpath, seasonFilename)
		if os.path.isfile(seasonSourcePath):
			objectSeasonPaths[season] = sceneryObject.getFilePath(seasonFilename)
			objectSourcePaths.append((seasonSourcePath, seasonFilename))
			displayMessage("S")

	for objectSourcePath, objectFilename in objectSourcePaths:
		# Copy the facade file
		shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[1], objectFilename))

		# Open the facade
		file = open(objectSourcePath, "rU")
		objectFileContents = file.readlines()
		file.close()

		textureFound = 0

		for line in objectFileContents:
			result = v8TexturePattern.match(line)
			if result:
				textureFound = 1
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if (result.group(1) == ""):
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Facade specifies a blank texture - valid but may not be as intended\n", "warning")
				elif os.path.isfile(textureFile):

					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					lastSlash = result.group(1).rfind("/")
					if (lastSlash > -1):
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)[0:lastSlash])
					else:
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1])
					if not os.path.isdir(destinationTexturePath):
						# Create destination texture path if it doesn't already exist
						os.makedirs(destinationTexturePath)
					if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1))):
						# Copy texture if it doesn't already exist
						shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find texture - facade excluded (" + textureFile + ")\n", "error")
					return

				# Break loop as soon as we find a texture, need look no further
				break

		if not textureFound:
			displayMessage("\n" + objectSourcePath + "\n")
			displayMessage("No texture line in file - this error must be corrected\n", "error")
			return

	# Handle the info.txt file
	if not handleInfoFile(mainobjectSourcePath, dirpath, parts, ".fac", sceneryObject, authors, latest): return

	# Copy files
	if not copySupportFiles(mainobjectSourcePath, dirpath, parts, sceneryObject): return

	# Facade is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	toc.append(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")
		for season in classes.Configuration.seasons:
			if season in objectSeasonPaths:
				# We have a seasonal virtual path for this season
				librarySeasonFileHandles[season].write("EXPORT_EXCLUDE opensceneryx/" + virtualPath + " " + objectSeasonPaths[season] + "\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryDeprecatedFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryDeprecatedFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")
	for (virtualPath, externalLibrary) in sceneryObject.externalVirtualPaths:
		libraryExternalFileHandle.write("EXPORT_BACKUP " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
	for virtualPath in sceneryObject.extendedVirtualPaths:
		if (virtualPath.startswith("lib/airport/aircraft")):
			libraryExtendedSAFileHandle.write("EXPORT_EXTEND " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		else:
			displayMessage("Unhandled EXPORT_EXTEND for " + virtualPath + "\n", "error")



def handleForest(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest):
	""" Create an instance of the SceneryObject class for a .for """

	global v8TexturePattern

	mainobjectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 1)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[1], filename)

	# Locate and check whether the support files exist
	if not checkSupportFiles(mainobjectSourcePath, dirpath, sceneryObject): return

	# Set up paths
	if not createPaths(parts): return

	# Build a list containing (filePath, filename) tuples, including seasonal variants
	objectSourcePaths = []
	objectSourcePaths.append((mainobjectSourcePath, filename))
	objectSeasonPaths = {}

	for season in classes.Configuration.seasons:
		seasonFilename = "forest_" + season + ".for"
		seasonSourcePath = os.path.join(dirpath, seasonFilename)
		if os.path.isfile(seasonSourcePath):
			objectSeasonPaths[season] = sceneryObject.getFilePath(seasonFilename)
			objectSourcePaths.append((seasonSourcePath, seasonFilename))
			displayMessage("S")

	for objectSourcePath, objectFilename in objectSourcePaths:
		# Copy the forest file
		shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[1], objectFilename))

		# Open the object
		file = open(objectSourcePath, "rU")
		objectFileContents = file.readlines()
		file.close()

		textureFound = 0

		for line in objectFileContents:
			result = v8TexturePattern.match(line)
			if result:
				textureFound = 1
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if (result.group(1) == ""):
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Forest specifies a blank texture - valid but may not be as intended\n")
				elif os.path.isfile(textureFile):

					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					lastSlash = result.group(1).rfind("/")
					if (lastSlash > -1):
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)[0:lastSlash])
					else:
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1])
					if not os.path.isdir(destinationTexturePath):
						# Create destination texture path if it doesn't already exist
						os.makedirs(destinationTexturePath)
					if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1))):
						# Copy texture if it doesn't already exist
						shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find texture - forest excluded (" + textureFile + ")\n", "error")
					return

				# Break loop as soon as we find a texture, need look no further
				break

	# Handle the info.txt file
	if not handleInfoFile(mainobjectSourcePath, dirpath, parts, ".for", sceneryObject, authors, latest): return

	# Copy files
	if not copySupportFiles(mainobjectSourcePath, dirpath, parts, sceneryObject): return

	# Forest is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	toc.append(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")
		for season in classes.Configuration.seasons:
			if season in objectSeasonPaths:
				# We have a seasonal virtual path for this season
				librarySeasonFileHandles[season].write("EXPORT_EXCLUDE opensceneryx/" + virtualPath + " " + objectSeasonPaths[season] + "\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryDeprecatedFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryDeprecatedFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")
	for (virtualPath, externalLibrary) in sceneryObject.externalVirtualPaths:
		libraryExternalFileHandle.write("EXPORT_BACKUP " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
	for virtualPath in sceneryObject.extendedVirtualPaths:
		if (virtualPath.startswith("lib/airport/aircraft")):
			libraryExtendedSAFileHandle.write("EXPORT_EXTEND " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		else:
			displayMessage("Unhandled EXPORT_EXTEND for " + virtualPath + "\n", "error")



def handleLine(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest):
	""" Create an instance of the SceneryObject class for a .lin """

	global v8TexturePattern

	mainobjectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 1)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[1], filename)

	# Locate and check whether the support files exist
	if not checkSupportFiles(mainobjectSourcePath, dirpath, sceneryObject): return

	# Set up paths
	if not createPaths(parts): return

	# Build a list containing (filePath, filename) tuples, including seasonal variants
	objectSourcePaths = []
	objectSourcePaths.append((mainobjectSourcePath, filename))
	objectSeasonPaths = {}

	for season in classes.Configuration.seasons:
		seasonFilename = "line_" + season + ".lin"
		seasonSourcePath = os.path.join(dirpath, seasonFilename)
		if os.path.isfile(seasonSourcePath):
			objectSeasonPaths[season] = sceneryObject.getFilePath(seasonFilename)
			objectSourcePaths.append((seasonSourcePath, seasonFilename))
			displayMessage("S")

	for objectSourcePath, objectFilename in objectSourcePaths:
		# Copy the line file
		shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[1], objectFilename))

		# Open the line
		file = open(objectSourcePath, "rU")
		objectFileContents = file.readlines()
		file.close()

		textureFound = 0

		for line in objectFileContents:
			result = v8TexturePattern.match(line)
			if result:
				textureFound = 1
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if (result.group(1) == ""):
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Line specifies a blank texture - valid but may not be as intended\n", "warning")
				elif os.path.isfile(textureFile):

					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					lastSlash = result.group(1).rfind("/")
					if (lastSlash > -1):
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)[0:lastSlash])
					else:
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1])
					if not os.path.isdir(destinationTexturePath):
						# Create destination texture path if it doesn't already exist
						os.makedirs(destinationTexturePath)
					if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1))):
						# Copy texture if it doesn't already exist
						shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find texture - line excluded (" + textureFile + ")\n", "error")
					return

				# Break loop as soon as we find a texture, need look no further
				break

		if not textureFound:
			displayMessage("\n" + objectSourcePath + "\n")
			displayMessage("No texture line in file - this error must be corrected\n", "error")
			return

	# Handle the info.txt file
	if not handleInfoFile(mainobjectSourcePath, dirpath, parts, ".lin", sceneryObject, authors, latest): return

	# Copy files
	if not copySupportFiles(mainobjectSourcePath, dirpath, parts, sceneryObject): return

	# Line is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	toc.append(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.lin\n")
		for season in classes.Configuration.seasons:
			if season in objectSeasonPaths:
				# We have a seasonal virtual path for this season
				librarySeasonFileHandles[season].write("EXPORT_EXCLUDE opensceneryx/" + virtualPath + " " + objectSeasonPaths[season] + "\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryDeprecatedFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryDeprecatedFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.lin\n")
	for (virtualPath, externalLibrary) in sceneryObject.externalVirtualPaths:
		libraryExternalFileHandle.write("EXPORT_BACKUP " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
	for virtualPath in sceneryObject.extendedVirtualPaths:
		if (virtualPath.startswith("lib/airport/aircraft")):
			libraryExtendedSAFileHandle.write("EXPORT_EXTEND " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		else:
			displayMessage("Unhandled EXPORT_EXTEND for " + virtualPath + "\n", "error")



def handlePolygon(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, libraryExtendedSAFileHandle, librarySeasonFileHandles, currentCategory, authors, textures, toc, latest):
	""" Create an instance of the SceneryObject class for a .pol """

	global v8PolygonTexturePattern, scalePattern, layerGroupPattern, surfacePattern

	mainobjectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 1)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.Polygon(parts[1], filename)

	# Locate and check whether the support files exist
	if not checkSupportFiles(mainobjectSourcePath, dirpath, sceneryObject): return

	# Set up paths
	if not createPaths(parts): return

	# Build a list containing (filePath, filename) tuples, including seasonal variants
	objectSourcePaths = []
	objectSourcePaths.append((mainobjectSourcePath, filename))
	objectSeasonPaths = {}

	for season in classes.Configuration.seasons:
		seasonFilename = "polygon_" + season + ".pol"
		seasonSourcePath = os.path.join(dirpath, seasonFilename)
		if os.path.isfile(seasonSourcePath):
			objectSeasonPaths[season] = sceneryObject.getFilePath(seasonFilename)
			objectSourcePaths.append((seasonSourcePath, seasonFilename))
			displayMessage("S")

	for objectSourcePath, objectFilename in objectSourcePaths:
		# Copy the polygon file
		shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[1], objectFilename))

		# Open the polygon
		file = open(objectSourcePath, "rU")
		objectFileContents = file.readlines()
		file.close()

		textureFound = 0
		scaleFound = 0
		layerGroupFound = 0
		surfaceFound = 0

		for line in objectFileContents:
			if not textureFound:
				result = v8PolygonTexturePattern.match(line)
				if result:
					textureFound = 1
					textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
					if (result.group(1) == ""):
						displayMessage("\n" + objectSourcePath + "\n")
						displayMessage("Polygon specifies a blank texture - valid but may not be as intended\n", "warning")
					elif os.path.isfile(textureFile):

						# Look for the texture in the texture Dictionary, create a new one if not found
						texture = textures.get(textureFile)
						if (texture == None):
							texture = classes.SceneryTexture(textureFile)
							textures[textureFile] = texture

						texture.sceneryObjects.append(sceneryObject)
						sceneryObject.sceneryTextures.append(texture)

						lastSlash = result.group(1).rfind("/")
						if (lastSlash > -1):
							destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)[0:lastSlash])
						else:
							destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1])
						if not os.path.isdir(destinationTexturePath):
							# Create destination texture path if it doesn't already exist
							os.makedirs(destinationTexturePath)
						if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1))):
							# Copy texture if it doesn't already exist
							shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
					else:
						displayMessage("\n" + objectSourcePath + "\n")
						displayMessage("Cannot find texture - polygon excluded (" + textureFile + ")\n", "error")
						return

			result = polygonNormalTexturePattern.match(line)
			if result:
				textureFile = os.path.abspath(os.path.join(dirpath, result.group(1)))
				if os.path.isfile(textureFile):
					# Look for the texture in the texture Dictionary, create a new one if not found
					texture = textures.get(textureFile)
					if (texture == None):
						texture = classes.SceneryTexture(textureFile)
						textures[textureFile] = texture

					texture.sceneryObjects.append(sceneryObject)
					sceneryObject.sceneryTextures.append(texture)

					lastSlash = result.group(1).rfind("/")
					if (lastSlash > -1):
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)[0:lastSlash])
					else:
						destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[1])
					if not os.path.isdir(destinationTexturePath):
						# Create destination texture path if it doesn't already exist
						os.makedirs(destinationTexturePath)
					if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1))):
						# Copy texture if it doesn't already exist
						shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[1], result.group(1)))
				else:
					displayMessage("\n" + objectSourcePath + "\n")
					displayMessage("Cannot find NORMAL texture - polygon excluded (" + textureFile + ")\n", "error")
					return

			if not scaleFound:
				result = scalePattern.match(line)
				if result:
					sceneryObject.scaleH = result.group(1)
					sceneryObject.scaleV = result.group(2)
					scaleFound = 1

			if not layerGroupFound:
				result = layerGroupPattern.match(line)
				if result:
					sceneryObject.layerGroupName = result.group(1)
					sceneryObject.layerGroupOffset = result.group(2)
					layerGroupFound = 1

			if not surfaceFound:
				result = surfacePattern.match(line)
				if result:
					sceneryObject.surfaceName = result.group(1)
					surfaceFound = 1


		if not textureFound:
			displayMessage("\n" + objectSourcePath + "\n")
			displayMessage("No texture line in file - this error must be corrected\n", "error")
			return

	# Handle the info.txt file
	if not handleInfoFile(mainobjectSourcePath, dirpath, parts, ".pol", sceneryObject, authors, latest): return

	# Copy files
	if not copySupportFiles(mainobjectSourcePath, dirpath, parts, sceneryObject): return

	# Polygon is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	toc.append(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.pol\n")
		for season in classes.Configuration.seasons:
			if season in objectSeasonPaths:
				# We have a seasonal virtual path for this season
				librarySeasonFileHandles[season].write("EXPORT_EXCLUDE opensceneryx/" + virtualPath + " " + objectSeasonPaths[season] + "\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryDeprecatedFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryDeprecatedFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.pol\n")
	for (virtualPath, externalLibrary) in sceneryObject.externalVirtualPaths:
		libraryExternalFileHandle.write("EXPORT_BACKUP " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
	for virtualPath in sceneryObject.extendedVirtualPaths:
		if (virtualPath.startswith("lib/airport/aircraft")):
			libraryExtendedSAFileHandle.write("EXPORT_EXTEND " + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		else:
			displayMessage("Unhandled EXPORT_EXTEND for " + virtualPath + "\n", "error")



def checkSupportFiles(objectSourcePath, dirpath, sceneryObject):
	""" Check that the info file and screenshot files are present """

	# Locate the info file. If it isn't in the current directory, walk up the folder structure
	# looking for one in all parent folders
	dirPathParts = dirpath.split(os.sep)
	for i in range(len(dirPathParts), 0, -1):
		if os.path.isfile(os.path.join(os.sep.join(dirPathParts[0:i]), "info.txt")):
			sceneryObject.infoFilePath = os.path.join(os.sep.join(dirPathParts[0:i]), "info.txt")
			break

	if sceneryObject.infoFilePath == "":
		displayMessage("\n" + objectSourcePath + "\n")
		displayMessage("No info.txt file found - object excluded\n", "error")
		return 0

	# Locate the screenshot file. If it isn't in the current directory, walk up the folder
	# structure looking for one in all parent folders
	for i in range(len(dirPathParts), 0, -1):
		if os.path.isfile(os.path.join(os.sep.join(dirPathParts[0:i]), "screenshot.jpg")):
			sceneryObject.screenshotFilePath = os.path.join(os.sep.join(dirPathParts[0:i]), "screenshot.jpg")
			break

	if sceneryObject.screenshotFilePath == "":
		displayMessage("\n" + objectSourcePath + "\n")
		displayMessage("No screenshot.jpg file found - using default\n", "note")

	return 1



def createPaths(parts):
	""" Create paths in osx folder and website folder """

	if not os.path.isdir(os.path.join(classes.Configuration.osxFolder, parts[1])):
		os.makedirs(os.path.join(classes.Configuration.osxFolder, parts[1]))
	if not os.path.isdir(os.path.join(classes.Configuration.osxWebsiteFolder, parts[1])):
		os.makedirs(os.path.join(classes.Configuration.osxWebsiteFolder, parts[1]))

	return 1


def copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject):
	""" Copy the support files from the source to the destination """

	if (sceneryObject.screenshotFilePath != ""):
		shutil.copyfile(sceneryObject.screenshotFilePath, os.path.join(classes.Configuration.osxWebsiteFolder, parts[1], "screenshot.jpg"))

	# Copy the logo file.  Logos are used to 'brand' objects that are from a specific
	# collection.  Therefore they are all stored in a single folder (in support) so they
	# can be shared across all the objects in the collection.
	if (sceneryObject.logoFileName != ""):
		if not os.path.isfile(os.path.join(classes.Configuration.supportFolder, "logos", sceneryObject.logoFileName)):
			displayMessage("\n" + objectSourcePath + "\n")
			displayMessage("Logo file couldn't be found (" + sceneryObject.logoFileName + "), omitting\n", "warning")
		else:
			shutil.copyfile(os.path.join(classes.Configuration.supportFolder, "logos", sceneryObject.logoFileName), os.path.join(classes.Configuration.osxWebsiteFolder, "doc", sceneryObject.logoFileName))

	return 1



def handleInfoFile(objectSourcePath, dirpath, parts, suffix, sceneryObject, authors, latest):
	""" Parse the contents of the info file, storing the results in the SceneryObject """

	global exportPattern, titlePattern, shortTitlePattern, authorPattern, textureAuthorPattern, conversionAuthorPattern, modificationAuthorPattern, emailPattern
	global textureEmailPattern, conversionEmailPattern, modificationEmailPattern, urlPattern, textureUrlPattern, conversionUrlPattern, modificationUrlPattern
	global widthPattern, heightPattern, depthPattern, descriptionPattern, excludePattern, animatedPattern
	global exportExtendedPattern, exportPropagatePattern, exportDeprecatedPattern, exportExternalPattern
	global logoPattern, notePattern, sincePattern

	file = open(sceneryObject.infoFilePath)
	websiteInfoFileContents = file.read()
	infoFileContents = websiteInfoFileContents.splitlines()
	file.close()

	# Add the file path to the virtual paths
	sceneryObject.virtualPaths.append(parts[1] + suffix)

	websiteInfoFileContents += "\n"

	for virtualPath in sceneryObject.virtualPaths:
		websiteInfoFileContents = "Export: " + virtualPath + "\n" + websiteInfoFileContents

	# Begin parsing
	for line in infoFileContents:
		# Check for exclusion
		result = excludePattern.match(line)
		if result:
			displayMessage("\n" + objectSourcePath + "\n")
			displayMessage("EXCLUDED, reason: " + result.group(1) + "\n", "note")
			return 0

		# Title
		result = titlePattern.match(line)
		if result:
			sceneryObject.title = result.group(1).replace("\"", "'")
			if (sceneryObject.shortTitle == ""): sceneryObject.shortTitle = sceneryObject.title
			continue

		# Short title
		result = shortTitlePattern.match(line)
		if result:
			sceneryObject.shortTitle = result.group(1).replace("\"", "'")
			continue

		# Main author
		result = authorPattern.match(line)
		if result:
			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue

		# Texture author
		result = textureAuthorPattern.match(line)
		if result:
			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue

		# Conversion author
		result = conversionAuthorPattern.match(line)
		if result:
			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue

		# Modification author
		result = modificationAuthorPattern.match(line)
		if result:
			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue

		# Width
		result = widthPattern.match(line)
		if result:
			sceneryObject.width = result.group(1)
			continue

		# Height
		result = heightPattern.match(line)
		if result:
			sceneryObject.height = result.group(1)
			continue

		# Depth
		result = depthPattern.match(line)
		if result:
			sceneryObject.depth = result.group(1)
			continue

		# Animated
		result = animatedPattern.match(line)
		if result:
			sceneryObject.animated = (result.group(1) == "True" or result.group(1) == "Yes")
			continue

		# Additional export path
		result = exportPattern.match(line)
		if result:
			sceneryObject.virtualPaths.append(result.group(1) + suffix)
			continue

		# Export propagation
		result = exportPropagatePattern.match(line)
		if result:
			# Work with the first virtual path only, this is the one generated from the file hierarchy
			virtualPathParts = sceneryObject.virtualPaths[0].split("/")
			sceneryObject.exportPropagate = int(result.group(1))
			# Only do anything if the value of exportPropagate is valid
			if sceneryObject.exportPropagate < len(virtualPathParts):
				# Iterate from the value of exportPropagate up to the length of the path, publishing the object to every parent between
				for i in range(sceneryObject.exportPropagate + 1, len(virtualPathParts)):
					sceneryObject.virtualPaths.append("/".join(virtualPathParts[0:i]) + suffix)
					websiteInfoFileContents = "Export: " + "/".join(virtualPathParts[0:i]) + suffix + "\n" + websiteInfoFileContents
			continue

		# Export deprecation
		result = exportDeprecatedPattern.match(line)
		if result:
			sceneryObject.deprecatedVirtualPaths.append([result.group(2) + suffix, result.group(1)])
			continue

		# Export to external library
		result = exportExternalPattern.match(line)
		if result:
			sceneryObject.externalVirtualPaths.append([result.group(2) + suffix, result.group(1)])
			continue

		# Export extend
		result = exportExtendedPattern.match(line)
		if result:
			sceneryObject.extendedVirtualPaths.append(result.group(1) + suffix)
			continue

		# Branding logo
		result = logoPattern.match(line)
		if result:
			sceneryObject.logoFileName = result.group(1)
			continue

		# Notes
		result = notePattern.match(line)
		if result:
			sceneryObject.note = result.group(1)
			continue

		# Since
		result = sincePattern.match(line)
		if result:
			sceneryObject.since = result.group(1)
			continue

		# Description
		result = descriptionPattern.match(line)
		if result:
			sceneryObject.description = result.group(1)
			continue

		# Default is to append to the description.  This handles any amount of extra text
		# at the end of the file
		sceneryObject.description += line

	# All Exports go into the website info file

	# Polygon-specific data
	if isinstance(sceneryObject, classes.Polygon):
		websiteInfoFileContents = "Texture Scale H: " + sceneryObject.scaleH + "\n" + websiteInfoFileContents
		websiteInfoFileContents = "Texture Scale V: " + sceneryObject.scaleV + "\n" + websiteInfoFileContents
		websiteInfoFileContents = "Layer Group: " + sceneryObject.layerGroupName + "\n" + websiteInfoFileContents
		websiteInfoFileContents = "Layer Offset: " + sceneryObject.layerGroupOffset + "\n" + websiteInfoFileContents
		websiteInfoFileContents = "Surface Type: " + sceneryObject.surfaceName + "\n" + websiteInfoFileContents

	# Copy the info file to the website folder
	#shutil.copyfile(sceneryObject.infoFilePath, os.path.join(classes.Configuration.osxWebsiteFolder, parts[1], "info.txt"))
	websiteInfoFile = open(os.path.join(classes.Configuration.osxWebsiteFolder, parts[1], "info.txt"), "w")
	websiteInfoFile.write(websiteInfoFileContents)
	websiteInfoFile.close()

	# Handle the tutorial if present
	if os.path.isfile(os.path.join(dirpath, "tutorial.pdf")):
		sceneryObject.tutorial = 1
		shutil.copyfile(os.path.join(dirpath, "tutorial.pdf"), classes.Configuration.osxWebsiteFolder + os.sep + "doc/" + os.sep + sceneryObject.title + " Tutorial.pdf")

	# Store in the latest if it was created for this version
	if LooseVersion(sceneryObject.since) >= LooseVersion(classes.Configuration.sinceVersionTag):
		latest.append(sceneryObject)

	return 1



def buildDocumentation(sitemapXMLFileHandle, sceneryCategory, depth):
	""" Build the documentation for the library.  All folders will have been parsed by this point """

	for sceneryObject in sceneryCategory.getSceneryObjects(0):
		writeXMLSitemapEntry(sitemapXMLFileHandle, "/" + sceneryObject.filePathRoot + "/", "0.5")
		writePDFEntry(sceneryObject)

	# Recurse
	children = sceneryCategory.childSceneryCategories

	newPage = False

	for childCategory in children:
		if (depth == 0):
			writePDFSectionHeading(childCategory.title, newPage)
			newPage = True
		elif (depth > 0):
			writePDFTOCEntry(childCategory.title, depth)

		buildDocumentation(sitemapXMLFileHandle, childCategory, depth + 1)


def writeXMLSitemapEntry(sitemapXMLFileHandle, path, priority):
	""" Write an entry for the sceneryObject into the sitemap XML file """
	xmlContent = "<url>"
	xmlContent += "<loc>https://www.opensceneryx.com" + path + "</loc>"
	#xmlContent += "<lastmod>2005-01-01</lastmod>"
	#xmlContent += "<changefreq>monthly</changefreq>"
	xmlContent += "<priority>" + priority + "</priority>"
	xmlContent += "</url>\n"

	sitemapXMLFileHandle.write(xmlContent)

	return 1


def getHTMLHeader(documentationPath, mainTitle, titleSuffix, includeSearch, includeTabbo):
	""" Get the standard header for all documentation files """

	result = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"\n"
	result += "					 \"https://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
	result += "<html xmlns=\"https://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\"><head><title>" + mainTitle
	if titleSuffix != "":
		result += " - " + titleSuffix
	result += "</title>\n"
	result += "<link rel='stylesheet' href='" + documentationPath + "all.css' type='text/css'/>\n"
	result += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n"
	result += "<!--[if gt IE 6.5]>\n"
	result += "<link rel='stylesheet' type='text/css' href='" + documentationPath + "ie7.css' media='all' />\n"
	result += "<![endif]-->\n"
	result += "<script type='text/javascript' src='https://code.jquery.com/jquery-1.4.2.min.js'></script>\n"
	result += "<script type='text/javascript' src='" + documentationPath + "scripts.js'></script>\n"
	result += "<script type='text/javascript' src='" + documentationPath + "versionInfo.js'></script>\n"

	result += "<script type='text/javascript'>\n"
	result += "var _gaq = _gaq || [];\n"
	result += "_gaq.push(['_setAccount', 'UA-4008328-4']);\n"
	result += "_gaq.push(['_trackPageview']);\n"
	result += "(function() {\n"
	result += "var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;\n"
	result += "ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\n"
	result += "var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);\n"
	result += "})();\n"
	result += "</script>\n"

	result += "</head>\n"
	result += "<body>\n"
	result += "<p class='hide'><a href='#content' accesskey='2'>Skip to main content</a></p>\n"
	result += "<img src='" + documentationPath + "x_banner_web.png' class='banner' alt='OpenSceneryX'>\n"
	result += "<div id='header'>\n"
	if includeSearch:
		result += "<div style='float:right;'>\n"
		result += "Search OpenSceneryx:<br />\n"
		result += "<form action='https://www.google.co.uk/cse' id='cse-search-box' target='_blank'>\n"
		result += "<div>\n"
		result += "<input type='hidden' name='cx' value='partner-pub-5631233433203577:vypgar-6zdh' />\n"
		result += "<input type='hidden' name='ie' value='UTF-8' />\n"
		result += "<input type='text' name='q' size='31' />\n"
		result += "<input type='submit' name='sa' value='Search' />\n"
		result += "</div>\n"
		result += "</form>\n"
		result += "<script type='text/javascript' src='https://www.google.com/coop/cse/brand?form=cse-search-box&amp;lang=en'></script>\n"
		result += "</div>"
	result += "<h1>" + mainTitle + "</h1>\n"
	result += "<p id='version'>Latest version <strong><a href='" + documentationPath + "ReleaseNotes.html'><script type='text/javascript'>document.write(osxVersion);</script></a></strong> created <strong><script type='text/javascript'>document.write(osxVersionDate);</script></strong></p>\n"
	result += "</div>\n"
	result += "<div style='clear:both;'>&nbsp;</div>"

	return result


def getHTMLFooter(documentationPath):
	""" Get the standard footer for all documentation files """

	result = "<div style='clear:both;'>&nbsp;</div>\n"
	result += "<div id='footer'>"

	result += "<div style='margin-top:1em;'>"
	result += "<div style='float:left; margin-right:1em;'><div style='margin:5px; padding: 1px; width: 88px; text-align: center;'><form action='https://www.paypal.com/cgi-bin/webscr' method='post'><input type='hidden' name='cmd' value='_s-xclick'><input type='hidden' name='hosted_button_id' value='J3H6VKZD86BJN'><input type='image' src='https://www.paypal.com/en_GB/i/btn/btn_donate_SM.gif' border='0' name='submit' alt='PayPal - The safer, easier way to pay online.' style=></form></div></div>"
	result += "<div style='margin: 5px; padding: 1px;'>OpenSceneryX is free <strong>and will always remain free</strong> for everyone to use.  However, if you do use it, please consider giving a donation to offset the direct costs such as hosting and domain names.</div>"
	result += "</div>"

	result += "<div style='clear:both;'>&nbsp;</div>\n"

	result += "<div>"
	result += "<div style='float:left; margin-right:1em;'><a rel='license' class='nounderline' href='https://creativecommons.org/licenses/by-nc-nd/3.0/' onclick='window.open(this.href);return false;'><img alt='Creative Commons License' class='icon' src='" + documentationPath + "cc_logo.png' /></a></div>"
	result += "<div style='margin: 5px; padding: 1px;'>The OpenSceneryX library is licensed under a <a rel='license' href='https://creativecommons.org/licenses/by-nc-nd/3.0/' onclick='window.open(this.href);return false;'>Creative Commons Attribution-Noncommercial-No Derivative Works 3.0 License</a>. 'The Work' is defined as the library as a whole and by using the library you signify agreement to these terms. <strong>You must obtain the permission of the author(s) if you wish to distribute individual files from this library for any purpose</strong>, as this constitutes a derivative work, which is forbidden under the licence.</div>"
	result += "</div>"

	result += "</div>"

	result += "</body></html>"
	return result



def getXMLSitemapHeader():
	""" Get the standard sitemap header """

	result = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
	result += "<urlset xmlns:xsi=\"https://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"https://www.sitemaps.org/schemas/sitemap/0.9 https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\" xmlns=\"https://www.sitemaps.org/schemas/sitemap/0.9\">\n"
	return result


def getXMLSitemapFooter():
	""" Get the standard sitemap footer """

	result = "</urlset>\n"
	return result


def getLibraryHeader(versionTag, includeStandard = True, type = "", comment = ""):
	""" Get the standard library.txt header """

	if (includeStandard == True):
		result = "A\n"
		result += "800\n"
		result += "LIBRARY\n"
		result += "\n"
		result += "# Version: v" + versionTag + "\n"
		result += "\n"
	else:
		result = "\n"

	if (comment != ""):
		result += "# " + comment + "\n"
		result += "\n"

	if (type == "private"):
		result += "PRIVATE\n\n"
	elif (type == "deprecated"):
		result += "DEPRECATED\n\n"

	return result

def getSeasonalLibraryContent(compatibility, content):
	result = ""

	# Note there are no 'Summer' regions. This is because we consider the default objects in OpenScenery X to be summer.
	if compatibility == "xplane":
		result += "REGION_DEFINE opensceneryx_nh_spring\n"
		result += "REGION_BITMAP shared_textures/regions/northern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days >= 60\n"
		result += "REGION_DREF sim/time/local_date_days <= 151\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_nh_autumn\n"
		result += "REGION_BITMAP shared_textures/regions/northern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days >= 244\n"
		result += "REGION_DREF sim/time/local_date_days <= 334\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_nh_winter1\n"
		result += "REGION_BITMAP shared_textures/regions/northern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days > 334\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_nh_winter2\n"
		result += "REGION_BITMAP shared_textures/regions/northern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days < 60\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_sh_spring\n"
		result += "REGION_BITMAP shared_textures/regions/southern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days >= 244\n"
		result += "REGION_DREF sim/time/local_date_days <= 334\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_sh_autumn\n"
		result += "REGION_BITMAP shared_textures/regions/southern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days >= 60\n"
		result += "REGION_DREF sim/time/local_date_days <= 151\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_sh_winter\n"
		result += "REGION_BITMAP shared_textures/regions/southern_hemisphere.png\n"
		result += "REGION_DREF sim/time/local_date_days >= 152\n"
		result += "REGION_DREF sim/time/local_date_days <= 243\n"
		result += "\n"
		result += "REGION opensceneryx_nh_spring\n"
		result += "\n"
		result += content["spring"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_nh_autumn\n"
		result += "\n"
		result += content["autumn"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_nh_winter1\n"
		result += "\n"
		result += content["winter"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_nh_winter2\n"
		result += "\n"
		result += content["winter"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_sh_spring\n"
		result += "\n"
		result += content["spring"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_sh_autumn\n"
		result += "\n"
		result += content["autumn"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_sh_winter\n"
		result += "\n"
		result += content["winter"] + "\n"
		result += "\n"

	elif compatibility == "fourseasons":
		result += "REGION_DEFINE opensceneryx_spring\n"
		result += "REGION_ALL\n"
		result += "REGION_DREF nm/four_seasons/season == 10\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_autumn\n"
		result += "REGION_ALL\n"
		result += "REGION_DREF nm/four_seasons/season == 30\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_winter\n"
		result += "REGION_ALL\n"
		result += "REGION_DREF nm/four_seasons/season >= 40\n"
		result += "\n"
		result += "REGION opensceneryx_spring\n"
		result += "\n"
		result += content["spring"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_autumn\n"
		result += "\n"
		result += content["autumn"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_winter\n"
		result += "\n"
		result += content["winter"] + "\n"
		result += "\n"

	elif compatibility == "terramaxx":
		result += "REGION_DEFINE opensceneryx_autumn\n"
		result += "REGION_ALL\n"
		result += "REGION_DREF maxxxp/seasonsxp/is_autumn == 1\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_winter\n"
		result += "REGION_ALL\n"
		result += "REGION_DREF maxxxp/seasonsxp/is_winter == 1\n"
		result += "\n"
		result += "REGION_DEFINE opensceneryx_winter_deep\n"
		result += "REGION_ALL\n"
		result += "REGION_DREF maxxxp/seasonsxp/is_mid_winter == 1\n"
		result += "\n"
		result += "REGION opensceneryx_autumn\n"
		result += "\n"
		result += content["autumn"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_winter\n"
		result += "\n"
		result += content["winter"] + "\n"
		result += "\n"
		result += "REGION opensceneryx_winter_deep\n"
		result += "\n"
		result += content["winter_deep"] + "\n"
		result += "\n"

	return result


def copyThirdParty():
	""" Copy the thirdparty folder into the optional folder """

	sourcePath = os.path.join(classes.Configuration.supportFolder, "thirdparty")
	destPath = os.path.join(classes.Configuration.osxFolder,  "optional")
	contents = os.listdir(sourcePath)

	for item in contents:
		if item[:1] == ".":
			continue

		fullSourcePath = os.path.join(sourcePath, item)
		shutil.copy(fullSourcePath, destPath)


def matchesAny(name, tests):
	""" Utility function to find whether a given string is found in a list """

	for test in tests:
		if fnmatch.fnmatch(name, test):
			return True
	return False



def caseinsensitiveSort(stringList):
	""" Case-insensitive string comparison sort. usage: stringList = caseinsensitive_sort(stringList) """

	tupleList = [(x.lower(), x) for x in stringList]
	tupleList.sort()
	stringList[:] = [x[1] for x in tupleList]


""" The following three functions are by Ned Batchelder and provide natural-order sorting
    http://nedbatchelder.com/blog/200712.html#e20071211T054956 """
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)



def displayMessage(message, type="message"):
	""" Display a message to the user of a given type (determines message colour) """

	if (type == "error"):
		print(f'{Fore.RED}ERROR: {message}{Style.RESET_ALL}', end='')
		osNotify("Error: " + message)
	elif (type == "warning"):
		print(f'{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}', end='')
	elif (type == "note"):
		print(f'{Fore.CYAN}NOTE: {message}{Style.RESET_ALL}', end='')
	elif (type == "message"):
		print(message, end='')

	sys.stdout.flush()


def getInput(message, maxSize):
	""" Get some input from the user """

	return input(message)


def osNotify(message = ""):
	""" Send an operating system notification """
	# On Mac: Requires terminal-notifier to be installed:
	# gem install terminal-notifier
	t = '-title OpenSceneryX Build Script'
	m = '-message {!r}'.format(message)
	i = '-appIcon {!r}'.format(os.path.join(classes.Configuration.supportFolder, "x_print.png"))
	ci = '-contentImage {!r}'.format(os.path.join(classes.Configuration.supportFolder, "x_print.png"))
	os.system('terminal-notifier {}'.format(' '.join([m, t, i, ci])))


def writePDFSectionHeading(title, newPageBefore = 0):
	""" Write a section heading to the PDF """

	if (not classes.Configuration.buildPDF): return

	pdf = classes.Configuration.developerPDF

	if (newPageBefore): pdf.add_page()

	pdf.set_font("DejaVu", "B", 16)
	pdf.set_text_color(0)
	pdf.cell(0, 12, title, 0, 1)

	writePDFTOCEntry(title, 0)


def writePDFText(text):
	""" Write some text to a PDF """

	if (not classes.Configuration.buildPDF): return

	pdf = classes.Configuration.developerPDF

	pdf.columns = 1
	pdf.set_font("DejaVu", "", 10)
	pdf.multi_cell(0, 5, text, 0, 'J', 0, False)


def writePDFEntry(sceneryObject):
	""" Write an entry to a PDF """

	if (not classes.Configuration.buildPDF): return

	# Check for PIL
	if Image is None: return

	pdf = classes.Configuration.developerPDF

	pdf.columns = 2
	imageMaxDimension = 20
	fontSize = 7
	lineHeight = 3

	# First check the image dimensions - we may need to force a new page if this image is too large
	if (sceneryObject.screenshotFilePath == ""):
		screenshotFilePath = "support/screenshot_missing.jpg"
	else:
		screenshotFilePath = sceneryObject.screenshotFilePath

	image = Image.open(screenshotFilePath)

	imageOriginalWidth, imageOriginalHeight = image.size

	if (imageOriginalWidth > imageOriginalHeight):
		imageScaleFactor = imageMaxDimension / float(imageOriginalWidth)
	else:
		imageScaleFactor = imageMaxDimension / float(imageOriginalHeight)

	imageFinalHeight = imageOriginalHeight * imageScaleFactor
	imageFinalWidth = imageOriginalWidth * imageScaleFactor

	# Start a new column now if the image or the virtual path list are going to go beyond the page
	# break trigger region
	if (pdf.get_y() + max(imageFinalHeight, (len(sceneryObject.virtualPaths) + 1) * 2 * lineHeight) > pdf.page_break_trigger): pdf.new_column()

	# Store the starting location
	startX = pdf.get_x()
	startY = pdf.get_y()
	startPage = pdf.page
	startColumn = pdf.current_column

	# Image
	pdf.image(screenshotFilePath, startX, startY, imageFinalWidth, imageFinalHeight, '', sceneryObject.getWebURL())

	# Title
	pdf.set_font("DejaVu", "B", fontSize)
	pdf.set_text_color(0)
	pdf.set_x(startX + imageMaxDimension)
	pdf.cell(0, lineHeight, sceneryObject.title, 0, 1, 'L', False, sceneryObject.getWebURL())

	# Virtual paths
	pdf.set_font("DejaVu", "", fontSize)
	virtualPathIndex = 1
	for virtualPath in sceneryObject.virtualPaths:
		if (virtualPathIndex == 2): pdf.set_text_color(128)
		pdf.set_x(startX + imageMaxDimension)
		pdf.cell(0, lineHeight, virtualPath, 0, 1)
		virtualPathIndex += 1

	# Ensure the next item starts after the image
	imageBottom = startY + imageFinalHeight + lineHeight
	if (pdf.page == startPage and pdf.current_column == startColumn and pdf.get_y() < imageBottom):
		pdf.ln(imageBottom - pdf.get_y())
	else:
		pdf.ln(lineHeight)


def writePDFTOCEntry(title, depth):
	""" Write a PDF TOC entry """

	if (not classes.Configuration.buildPDF): return

	pdf = classes.Configuration.developerPDF
	pdf.toc_entry(title, depth)


def closePDF(path):
	""" Close and save a PDF file """

	if (not classes.Configuration.buildPDF): return

	pdf = classes.Configuration.developerPDF
	pdf.columns = 1

	pdf.set_text_color(0)
	pdf.insert_toc(2, 16, 8, 'DejaVu', 'Table of Contents')
	pdf.output(path, "F")

