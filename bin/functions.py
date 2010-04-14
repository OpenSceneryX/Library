#!/usr/local/bin/python
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
import pcrt
import sys


def buildCategoryLandingPages(sceneryCategory):
	""" Build all the documentation landing pages for SceneryCategories """
	
	# Only build landing pages where depth >= 2
	if sceneryCategory.depth >= 2:
		htmlFileContent = ""
		
		htmlFileContent += "<div id='breadcrumbs'>\n"
		htmlFileContent += "<ul class='inline'>"
		
		sceneryCategoryAncestors = sceneryCategory.getAncestors(0)
		for sceneryCategoryAncestor in sceneryCategoryAncestors[::-1]:
			if (sceneryCategoryAncestor.url != None):
				htmlFileContent += "<li><a href='" + sceneryCategoryAncestor.url + "'>" + sceneryCategoryAncestor.title + "</a></li>\n"
			else:
				htmlFileContent += "<li>" + sceneryCategoryAncestor.title + "</li>\n"
		htmlFileContent += "<li>" + sceneryCategory.title + "</li>\n"
		htmlFileContent += "</ul>\n"
		htmlFileContent += "</div>\n"

		htmlFileContent += "<div id='content'>\n"
		htmlFileContent += "<a name='content'></a>\n"
		htmlFileContent += "<h2>" + sceneryCategory.title + "</h2>\n"
		
		# Sub-categories in this category
		if len(sceneryCategory.childSceneryCategories) > 0:
			htmlFileContent += "<h3>Sub-categories</h3>\n"
			for childSceneryCategory in sceneryCategory.childSceneryCategories:
				htmlFileContent += "<h4 class='inline'><a href='" + childSceneryCategory.url + "'>" + childSceneryCategory.title + "</a></h4>\n"
		
			htmlFileContent += "<div style='clear:both;'>&nbsp;</div>\n"

		# Objects in this category
		if len(sceneryCategory.getSceneryObjects(0)) > 0:
			htmlFileContent += "<h3>Objects</h3>\n"
			for sceneryObject in sceneryCategory.getSceneryObjects(0):
				htmlFileContent += "<div class='thumbnailcontainer'>\n"
				htmlFileContent += "<h4><a href='/" + sceneryObject.filePathRoot + "/index.html'>" + sceneryObject.title + "</a></h4><a href='/" + sceneryObject.filePathRoot + "/index.html' class='nounderline'>"
				if (sceneryObject.screenshotFilePath != ""):
					htmlFileContent += "<img src='/" + sceneryObject.filePathRoot + "/screenshot.jpg' alt='Screenshot of " + sceneryObject.shortTitle.replace("'", "&apos;") + "' />"
				else:
					htmlFileContent += "<img src='/doc/screenshot_missing.png' alt='No Screenshot Available' />"
				htmlFileContent += "</a>\n"
				htmlFileContent += "</div>\n"
	
			htmlFileContent += "<div style='clear:both;'>&nbsp;</div>\n"
		
		htmlFileHandle = open(classes.Configuration.osxWebsiteFolder + os.sep + "doc" + os.sep + "c_" + sceneryCategory.title + ".html", "w")
		htmlFileHandle.write(getHTMLHeader("/doc/", "OpenSceneryX Object Library for X-Plane&reg;", sceneryCategory.title + " Variants", True, True))
		htmlFileHandle.write(htmlFileContent)
		htmlFileHandle.write(getHTMLSponsoredLinks())
		htmlFileHandle.write("</div>\n")
		htmlFileHandle.write(getHTMLFooter("/doc/"))
		htmlFileHandle.close()

	# Recurse
	children = sceneryCategory.childSceneryCategories
	for childCategory in children:
		buildCategoryLandingPages(childCategory)
		
		

def handleFolder(dirPath, currentCategory, libraryFileHandle, libraryPlaceholderFileHandle, authors, textures):
	""" Parse the contents of a library folder """
	
	contents = os.listdir(dirPath)
	
	# Handle category descriptor first, if present
	if "category.txt" in contents:
		currentCategory = handleCategory(dirPath, currentCategory)
	
	for item in contents:
		fullPath = os.path.join(dirPath, item)
		
		if (item == "object.obj"):
			handleObject(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures)
			continue
		elif (item == "facade.fac"):
			handleFacade(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures)
			continue
		elif (item == "forest.for"):
			handleForest(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures)
			continue
		elif (item == "line.lin"):
			handleLine(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures)
			continue
		elif (item == "polygon.pol"):
			handlePolygon(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures)
			continue
		elif (item == "category.txt"):
			# Do nothing
			continue
		elif os.path.isdir(fullPath):
			if not item == ".svn":
				handleFolder(fullPath, currentCategory, libraryFileHandle, libraryPlaceholderFileHandle, authors, textures)



def handleCategory(dirpath, currentCategory):
	""" Create an instance of the SceneryCategory class """
	
	sceneryCategory = classes.SceneryCategory(dirpath, currentCategory)
	currentCategory.addSceneryCategory(sceneryCategory)
	
	return sceneryCategory
	
	

def handleObject(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures):
	""" Create an instance of the SceneryObject class for a .obj """
	
	objectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 2)

	displayMessage(".")
	
	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[2], filename)

	# Locate and check whether the support files exist 
	if not checkSupportFiles(objectSourcePath, dirpath, sceneryObject): return
	
	# Handle the info.txt file
	if not handleInfoFile(objectSourcePath, dirpath, parts, ".obj", sceneryObject, authors): return
	
	# Set up paths and copy files
	if not copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject): return

	# Copy the object file
	shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))

	# Open the object
	file = open(objectSourcePath, "rU")
	objectFileContents = file.readlines()
	file.close()

	# Define the regex patterns:
	v7TexturePattern = re.compile("([^\s]*)\s+// Texture")
	v8TexturePattern = re.compile("TEXTURE\s+(.*)")
	v8LitTexturePattern = re.compile("TEXTURE_LIT\s+(.*)")
	textureFound = 0
	
	for line in objectFileContents:
		result = v7TexturePattern.match(line)
		if result:
			textureFound = 1
			textureFile = os.path.abspath(os.path.join(dirpath, result.group(1) + ".png"))
			litTextureFile = os.path.join(dirpath, result.group(1) + "LIT.png")
			if (result.group(1) == ""):
				displayMessage("\n" + objectSourcePath + "\n")
				displayMessage("Object (v7) specifies a blank texture - valid but may not be as intended\n", "warning")
			elif os.path.isfile(textureFile):
			
				# Look for the texture in the texture Dictionary, create a new one if not found
				texture = textures.get(textureFile)
				if (texture == None):
					texture = classes.SceneryTexture(textureFile)
					textures[textureFile] = texture
				
				texture.sceneryObjects.append(sceneryObject)
				sceneryObject.sceneryTextures.append(texture)

				shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1) + ".png"))
				if os.path.isfile(litTextureFile):
					shutil.copyfile(litTextureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1) + "LIT.png"))
			else:
				displayMessage("\n" + objectSourcePath + "\n")
				displayMessage("Cannot find texture - object (v7) excluded (" + textureFile + ")\n", "error")
				return
			
			# Break loop as soon as we find a v7 texture, need look no further
			break

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
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)[0:lastSlash])
				else:
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2])
				if not os.path.isdir(destinationTexturePath): 
					# Create destination texture path if it doesn't already exist
					os.makedirs(destinationTexturePath)
				if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1))):
					# Copy texture if it doesn't already exist
					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
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

				shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
			else:
				displayMessage("\n" + objectSourcePath + "\n")
				displayMessage("Cannot find LIT texture - object (v8) excluded (" + textureFile + ")\n", "error")
				return

			# Break loop if we've found both v8 textures
			if textureFound == 2:
				break

	if textureFound == 0:
		displayMessage("\n" + objectSourcePath + "\n")
		displayMessage("No texture line in file - this error must be corrected\n", "error")
		return
		
	# Object is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")





def handleFacade(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures):
	""" Create an instance of the SceneryObject class for a .fac """

	objectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 2)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[2], filename)
	
	# Locate and check whether the support files exist 
	if not checkSupportFiles(objectSourcePath, dirpath, sceneryObject): return
	
	# Handle the info.txt file
	if not handleInfoFile(objectSourcePath, dirpath, parts, ".fac", sceneryObject, authors): return
	
	# Set up paths and copy files
	if not copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject): return

	# Copy the facade file
	shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
	
	# Open the facade
	file = open(objectSourcePath, "rU")
	objectFileContents = file.readlines()
	file.close()

	# Define the regex patterns:
	v8TexturePattern = re.compile("TEXTURE\s+(.*)")
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
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)[0:lastSlash])
				else:
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2])
				if not os.path.isdir(destinationTexturePath): 
					# Create destination texture path if it doesn't already exist
					os.makedirs(destinationTexturePath)
				if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1))):
					# Copy texture if it doesn't already exist
					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
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
		
	# Facade is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")





def handleForest(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures):
	""" Create an instance of the SceneryObject class for a .for """
	
	objectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 2)

	displayMessage(".")
	
	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[2], filename)

	# Locate and check whether the support files exist 
	if not checkSupportFiles(objectSourcePath, dirpath, sceneryObject): return
	
	# Handle the info.txt file
	if not handleInfoFile(objectSourcePath, dirpath, parts, ".for", sceneryObject, authors): return
	
	# Set up paths and copy files
	if not copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject): return

	# Copy the forest file
	shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))

	# Open the object
	file = open(objectSourcePath, "rU")
	objectFileContents = file.readlines()
	file.close()

	# Define the regex patterns:
	v8TexturePattern = re.compile("TEXTURE\s+(.*)")
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
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)[0:lastSlash])
				else:
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2])
				if not os.path.isdir(destinationTexturePath): 
					# Create destination texture path if it doesn't already exist
					os.makedirs(destinationTexturePath)
				if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1))):
					# Copy texture if it doesn't already exist
					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
			else:
				displayMessage("\n" + objectSourcePath + "\n")
				displayMessage("Cannot find texture - forest excluded (" + textureFile + ")\n", "error")
				return

			# Break loop as soon as we find a texture, need look no further
			break

	if not textureFound:
		displayMessage("\n" + objectSourcePath + "\n")
		displayMessage("No texture line in file - this error must be corrected\n", "error")
		return
		
	# Forest is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")




def handleLine(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures):
	""" Create an instance of the SceneryObject class for a .lin """
	
	objectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 2)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[2], filename)
	
	# Locate and check whether the support files exist 
	if not checkSupportFiles(objectSourcePath, dirpath, sceneryObject): return
	
	# Handle the info.txt file
	if not handleInfoFile(objectSourcePath, dirpath, parts, ".lin", sceneryObject, authors): return
	
	# Set up paths and copy files
	if not copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject): return

	# Copy the line file
	shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
	
	# Open the line
	file = open(objectSourcePath, "rU")
	objectFileContents = file.readlines()
	file.close()

	# Define the regex patterns:
	v8TexturePattern = re.compile("TEXTURE\s+(.*)")
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
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)[0:lastSlash])
				else:
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2])
				if not os.path.isdir(destinationTexturePath): 
					# Create destination texture path if it doesn't already exist
					os.makedirs(destinationTexturePath)
				if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1))):
					# Copy texture if it doesn't already exist
					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
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
		
	# Line is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.lin\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.lin\n")


def handlePolygon(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors, textures):
	""" Create an instance of the SceneryObject class for a .pol """
	
	objectSourcePath = os.path.join(dirpath, filename)
	parts = dirpath.split(os.sep, 2)

	displayMessage(".")

	# Create an instance of the SceneryObject class
	sceneryObject = classes.SceneryObject(parts[2], filename)
	
	# Locate and check whether the support files exist 
	if not checkSupportFiles(objectSourcePath, dirpath, sceneryObject): return
	
	# Handle the info.txt file
	if not handleInfoFile(objectSourcePath, dirpath, parts, ".pol", sceneryObject, authors): return
	
	# Set up paths and copy files
	if not copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject): return

	# Copy the polygon file
	shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
	
	# Open the polygon
	file = open(objectSourcePath, "rU")
	objectFileContents = file.readlines()
	file.close()

	# Define the regex patterns:
	v8TexturePattern = re.compile("(?:TEXTURE|TEXTURE_NOWRAP)\s+(.*)")
	textureFound = 0
	
	for line in objectFileContents:
		result = v8TexturePattern.match(line)
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
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)[0:lastSlash])
				else:
					destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2])
				if not os.path.isdir(destinationTexturePath): 
					# Create destination texture path if it doesn't already exist
					os.makedirs(destinationTexturePath)
				if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1))):
					# Copy texture if it doesn't already exist
					shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
			else:
				displayMessage("\n" + objectSourcePath + "\n")
				displayMessage("Cannot find texture - polygon excluded (" + textureFile + ")\n", "error")
				return

			# Break loop as soon as we find a texture, need look no further
			break

	if not textureFound:
		displayMessage("\n" + objectSourcePath + "\n")
		displayMessage("No texture line in file - this error must be corrected\n", "error")
		return
		
	# Line is valid, append it to the current category
	currentCategory.addSceneryObject(sceneryObject)

	# Write to the library.txt file
	for virtualPath in sceneryObject.virtualPaths:
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.lin\n")
	for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
		libraryFileHandle.write("# Deprecated v" + virtualPathVersion + "\n")
		libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
		libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.lin\n")



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



	
def copySupportFiles(objectSourcePath, dirpath, parts, sceneryObject):
	""" Copy the support files from the source to the destination """
	
	if not os.path.isdir(os.path.join(classes.Configuration.osxFolder, parts[2])): 
		os.makedirs(os.path.join(classes.Configuration.osxFolder, parts[2]))
	if not os.path.isdir(os.path.join(classes.Configuration.osxWebsiteFolder, parts[2])): 
		os.makedirs(os.path.join(classes.Configuration.osxWebsiteFolder, parts[2]))

	# Copy the info file
	shutil.copyfile(sceneryObject.infoFilePath, os.path.join(classes.Configuration.osxFolder, parts[2], "info.txt"))
	
	if (sceneryObject.screenshotFilePath != ""):
		shutil.copyfile(sceneryObject.screenshotFilePath, os.path.join(classes.Configuration.osxWebsiteFolder, parts[2], "screenshot.jpg"))
	
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
	
	
	
def handleInfoFile(objectSourcePath, dirpath, parts, suffix, sceneryObject, authors):
	""" Parse the contents of the info file, storing the results in the SceneryObject """
	
	file = open(sceneryObject.infoFilePath)
	infoFileContents = file.readlines()
	file.close()
	
	# define the regex patterns:
	exportPattern = re.compile("Export:\s+(.*)")
	titlePattern = re.compile("Title:\s+(.*)")
	shortTitlePattern = re.compile("Short Title:\s+(.*)")
	authorPattern = re.compile("Author:\s+(.*)")
	textureAuthorPattern = re.compile("Author, texture:\s+(.*)")
	conversionAuthorPattern = re.compile("Author, conversion:\s+(.*)")
	emailPattern = re.compile("Email:\s+(.*)")
	textureEmailPattern = re.compile("Email, texture:\s+(.*)")
	conversionEmailPattern = re.compile("Email, conversion:\s+(.*)")
	urlPattern = re.compile("URL:\s+(.*)")
	textureUrlPattern = re.compile("URL, texture:\s+(.*)")
	conversionUrlPattern = re.compile("URL, conversion:\s+(.*)")
	widthPattern = re.compile("Width:\s+(.*)")
	heightPattern = re.compile("Height:\s+(.*)")
	depthPattern = re.compile("Depth:\s+(.*)")
	descriptionPattern = re.compile("Description:\s+(.*)")
	excludePattern = re.compile("Exclude:\s+(.*)")
	animatedPattern = re.compile("Animated:\s+(.*)")
	exportPropagatePattern = re.compile("Export Propagate:\s+(.*)")
	exportDeprecatedPattern = re.compile("Export Deprecated v(.*):\s+(.*)")
	logoPattern = re.compile("Logo:\s+(.*)")
	notePattern = re.compile("Note:\s+(.*)")
	
	# Add the file path to the virtual paths
	sceneryObject.virtualPaths.append(parts[2] + suffix)
	
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
			if sceneryObject.author == "":
				sceneryObject.author = result.group(1)
			else:
				sceneryObject.author = sceneryObject.author + " and " + result.group(1)
				
			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue
		
		# Texture author
		result = textureAuthorPattern.match(line)
		if result:
			if sceneryObject.textureAuthor == "":
				sceneryObject.textureAuthor = result.group(1)
			else:
				sceneryObject.textureAuthor = sceneryObject.textureAuthor + " and " + result.group(1)

			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue
			
		# Conversion author
		result = conversionAuthorPattern.match(line)
		if result:
			if sceneryObject.conversionAuthor == "":
				sceneryObject.conversionAuthor = result.group(1)
			else:
				sceneryObject.conversionAuthor = sceneryObject.conversionAuthor + " and " + result.group(1)

			if not result.group(1) in authors:
				authors.append(result.group(1))
			continue
		
		# Main author email
		result = emailPattern.match(line)
		if result:
			sceneryObject.email = result.group(1)
			continue
		
		# Texture author email
		result = textureEmailPattern.match(line)
		if result:
			sceneryObject.textureEmail = result.group(1)
			continue
		
		# Conversion author email
		result = conversionEmailPattern.match(line)
		if result:
			sceneryObject.conversionEmail = result.group(1)
			continue
		
		# Main author URL
		result = urlPattern.match(line)
		if result:
			sceneryObject.url = result.group(1)
			continue
		
		# Texture author URL
		result = textureUrlPattern.match(line)
		if result:
			sceneryObject.textureUrl = result.group(1)
			continue
		
		# Conversion author URL
		result = conversionUrlPattern.match(line)
		if result:
			sceneryObject.conversionUrl = result.group(1)
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
			continue
		
		# Export deprecation
		result = exportDeprecatedPattern.match(line)
		if result:
			sceneryObject.deprecatedVirtualPaths.append([result.group(2) + suffix, result.group(1)])
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
		
		# Description
		result = descriptionPattern.match(line)
		if result:
			sceneryObject.description = result.group(1)
			continue

		# Default is to append to the description.  This handles any amount of extra text
		# at the end of the file 
		sceneryObject.description += line
	
	# Handle the tutorial if present
	if os.path.isfile(os.path.join(dirpath, "tutorial.pdf")):
		sceneryObject.tutorial = 1
		shutil.copyfile(os.path.join(dirpath, "tutorial.pdf"), classes.Configuration.osxWebsiteFolder + os.sep + "doc/" + os.sep + sceneryObject.title + " Tutorial.pdf")
	
	return 1



def buildDocumentation(sceneryCategory, depth):
	""" Build the documentation for the library.  All folders will have been parsed by this point """
	
	for sceneryObject in sceneryCategory.getSceneryObjects(0):
		writeHTMLDocFile(sceneryObject)
		
	# Recurse
	children = sceneryCategory.childSceneryCategories
	for childCategory in children:
		buildDocumentation(childCategory, depth + 1)



def writeHTMLDocFile(sceneryObject):
	""" Write a documentation file for the given SceneryObject to disk """
	htmlFileContent = ""
	
	# Breadcrumbs
	htmlFileContent += "<div id='breadcrumbs'>\n"
	htmlFileContent += "<ul class='inline'>"
	
	sceneryCategoryAncestors = sceneryObject.sceneryCategory.getAncestors(1)
	for sceneryCategoryAncestor in sceneryCategoryAncestors[::-1]:
		if (sceneryCategoryAncestor.url != None):
			htmlFileContent += "<li><a href='" + sceneryCategoryAncestor.url + "'>" + sceneryCategoryAncestor.title + "</a></li>\n"
		else:
			htmlFileContent += "<li>" + sceneryCategoryAncestor.title + "</li>\n"
	htmlFileContent += "<li>" + sceneryObject.title + "</li>\n"
	htmlFileContent += "</ul>\n"
	htmlFileContent += "</div>\n"
	
	# Content
	htmlFileContent += "<div id='content'>\n"
	htmlFileContent += "<a name='content'></a>\n"
	htmlFileContent += "<h2>" + sceneryObject.title + "</h2>\n"
	htmlFileContent += "<div class='virtualPath'>\n"
	htmlFileContent += "<h3>Virtual Paths</h3>\n"
	
	for virtualPath in sceneryObject.virtualPaths:
		htmlFileContent += virtualPath + "<br />\n"
		
	htmlFileContent += "</div>\n"
	
	# Paths
	if (not sceneryObject.deprecatedVirtualPaths == []):
		htmlFileContent += "<div class='deprecatedVirtualPath'>\n"
		htmlFileContent += "<h3>Deprecated Paths</h3>\n"
		for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
			htmlFileContent += "<strong>From v" + virtualPathVersion + "</strong>: " + virtualPath + "<br />\n"
		htmlFileContent += "</div>\n"
	if (sceneryObject.screenshotFilePath != ""):
		htmlFileContent += "<img class='screenshot' src='/" + sceneryObject.filePathRoot + "/screenshot.jpg" + "' alt='Screenshot of " + 			sceneryObject.shortTitle.replace("'", "&apos;") + "' />\n"
	else:
		htmlFileContent += "<img class='screenshot' src='/doc/screenshot_missing.png' alt='No Screenshot Available' />\n"

	# Logo
	if (sceneryObject.logoFileName != ""):
		htmlFileContent += "<div class='objectlogocontainer'>\n"
		htmlFileContent += "<img src='" + sceneryObject.logoFileName + "' alt='Object branding logo' />\n"		
		htmlFileContent += "</div>\n"

	# Main information
	htmlFileContent += "<ul class='mainItemDetails'>\n"
	
	# Author
	if (not sceneryObject.author == ""):
		htmlFileContent += "<li><span class='fieldTitle'>Original Author:</span> "
		if (not sceneryObject.url == ""):
			htmlFileContent += "<span class='fieldValue'><a href='" + sceneryObject.url + "' onclick='window.open(this.href);return false;'>" + sceneryObject.author + "</a></span>"
			if (not sceneryObject.email == ""):
				htmlFileContent += ", <span class='fieldTitle'>email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.email + "'>" + sceneryObject.email + "</a></span>"
		elif (not sceneryObject.email == ""):
			htmlFileContent += "<span class='fieldValue'><a href='mailto:" + sceneryObject.email + "'>" + sceneryObject.author + "</a></span>"
		else:
			htmlFileContent += "<span class='fieldValue'>" + sceneryObject.author + "</span>"
		htmlFileContent += "</li>\n"
		
	# Texture author
	if (not sceneryObject.textureAuthor == ""):
		htmlFileContent += "<li><span class='fieldTitle'>Original Texture Author:</span> "
		if (not sceneryObject.textureUrl == ""):
			htmlFileContent += "<span class='fieldValue'><a href='" + sceneryObject.textureUrl + "' onclick='window.open(this.href);return false;'>" + sceneryObject.textureAuthor + "</a></span>"
			if (not sceneryObject.textureEmail == ""):
				htmlFileContent += ", <span class='fieldTitle'>email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.textureEmail + "'>" + sceneryObject.textureEmail + "</a></span>"
		elif (not sceneryObject.textureEmail == ""):
			htmlFileContent += "<span class='fieldValue'><a href='mailto:" + sceneryObject.textureEmail + "'>" + sceneryObject.textureAuthor + "</a></span>"
		else:
			htmlFileContent += "<span class='fieldValue'>" + sceneryObject.textureAuthor + "</span>"
		htmlFileContent += "</li>\n"
		
	# Conversion author
	if (not sceneryObject.conversionAuthor == ""):
		htmlFileContent += "<li><span class='fieldTitle'>Object Conversion By:</span> "
		if (not sceneryObject.conversionUrl == ""):
			htmlFileContent += "<span class='fieldValue'><a href='" + sceneryObject.conversionUrl + "' onclick='window.open(this.href);return false;'>" + sceneryObject.conversionAuthor + "</a></span>"
			if (not sceneryObject.conversionEmail == ""):
				htmlFileContent += ", <span class='fieldTitle'>email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.conversionEmail + "'>" + sceneryObject.conversionEmail + "</a></span>"
		elif (not sceneryObject.conversionEmail == ""):
			htmlFileContent += "<span class='fieldValue'><a href='mailto:" + sceneryObject.conversionEmail + "'>" + sceneryObject.conversionAuthor + "</a></span>"
		else:
			htmlFileContent += "<span class='fieldValue'>" + sceneryObject.conversionAuthor + "</span>"
		htmlFileContent += "</li>\n"
	
	# Description
	if (not sceneryObject.description == ""):
		htmlFileContent += "<li><span class='fieldTitle'>Description:</span> <span class='fieldValue'>" + sceneryObject.description + "</span></li>\n"
		
	# Note
	if (not sceneryObject.note == ""):
		htmlFileContent += "<li class='note'><span class='fieldTitle'>Important Note:</span> <span class='fieldValue'>" + sceneryObject.note + "</span></li>\n"
	
	# Dimensions
	if (not sceneryObject.width == "" and not sceneryObject.height == "" and not sceneryObject.depth == ""):
		htmlFileContent += "<li><span class='fieldTitle'>Dimensions:</span>\n"
		htmlFileContent += "<ul class='dimensions'>\n"
		htmlFileContent += "<li id='width'><span class='fieldTitle'>w:</span> " + sceneryObject.width + "</li>\n"
		htmlFileContent += "<li id='height'><span class='fieldTitle'>h:</span> " + sceneryObject.height + "</li>\n"
		htmlFileContent += "<li id='depth'><span class='fieldTitle'>d:</span> " + sceneryObject.depth + "</li>\n"
		htmlFileContent += "</ul>\n"
		htmlFileContent += "</li>\n"

	# Tutorial
	if (sceneryObject.tutorial):
		htmlFileContent += "<li><span class='fieldTitle'>Tutorial:</span> <span class='fieldValue'><a href='" + urllib.quote(sceneryObject.title + " Tutorial.pdf") + "' class='nounderline' title='View Tutorial' onclick='window.open(this.href);return false;'><img src='../doc/pdf.gif' class='icon' alt='PDF File Icon' /></a>&nbsp;<a href='" + urllib.quote(sceneryObject.title + " Tutorial.pdf") + "' title='View Tutorial' onclick='window.open(this.href);return false;'>View Tutorial</a></span></li>\n"
	
	# Texture references
	for texture in sceneryObject.sceneryTextures:
		if len(texture.sceneryObjects) > 1:
			# This scenery object shares a texture with other objects
			htmlFileContent += "<li><span class='fieldTitle'>Texture '" + texture.fileName + "' shared with:</span>"
			htmlFileContent += "<ul>"
			for sharedTextureObject in texture.sceneryObjects:
				htmlFileContent += "<li><span class='fieldValue'><a href='/" + sharedTextureObject.filePathRoot + "/index.html'>" + sharedTextureObject.title + "</a></span></li>"
			htmlFileContent += "</ul></li>"
		
	htmlFileContent += "</ul>\n"
	htmlFileContent += "<div style='clear:both;'>&nbsp;</div>";

	# Write the file contents
	htmlFileHandle = open(classes.Configuration.osxWebsiteFolder + os.sep + sceneryObject.filePathRoot + os.sep + "index.html", "w")
	htmlFileHandle.write(getHTMLHeader("/doc/", "OpenSceneryX Object Library for X-Plane&reg;", sceneryObject.title, True, True))
	htmlFileHandle.write(htmlFileContent)
	htmlFileHandle.write(getHTMLSponsoredLinks())
	htmlFileHandle.write("</div>")
	htmlFileHandle.write(getHTMLFooter("/doc/"))
	htmlFileHandle.close()
	
	return 1



def getHTMLHeader(documentationPath, mainTitle, titleSuffix, includeSearch, includeTabbo):
	""" Get the standard header for all documentation files """
	
	result = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"\n"
	result += "					 \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
	result += "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\"><head><title>" + mainTitle
	if titleSuffix != "":
		result += " - " + titleSuffix
	result += "</title>\n"
	result += "<link rel='stylesheet' href='" + documentationPath + "all.css' type='text/css'/>\n"
	result += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n"
	result += "<!--[if gt IE 6.5]>\n"
	result += "<link rel='stylesheet' type='text/css' href='" + documentationPath + "ie7.css' media='all' />\n"
	result += "<![endif]-->\n"
	result += "<script type='text/javascript' src='http://code.jquery.com/jquery-1.4.2.min.js'></script>\n"
	result += "<script type='text/javascript' src='" + documentationPath + "scripts.js'></script>\n"
	result += "<script type='text/javascript' src='" + documentationPath + "versionInfo.js'></script>\n"
	result += "</head>\n"
	result += "<body>\n"
	result += "<p class='hide'><a href='#content' accesskey='2'>Skip to main content</a></p>\n"
	result += "<div id='header'>\n"
	if includeSearch:
		result += "<div style='float:right;'>\n"
		result += "Search OpenSceneryx:<br />\n"
		result += "<form action='http://www.google.co.uk/cse' id='cse-search-box' target='_blank'>\n"
		result += "<div>\n"
		result += "<input type='hidden' name='cx' value='partner-pub-5631233433203577:vypgar-6zdh' />\n"
		result += "<input type='hidden' name='ie' value='UTF-8' />\n"
		result += "<input type='text' name='q' size='31' />\n"
		result += "<input type='submit' name='sa' value='Search' />\n"
		result += "</div>\n"
		result += "</form>\n"
		result += "<script type='text/javascript' src='http://www.google.com/coop/cse/brand?form=cse-search-box&amp;lang=en'></script>\n"
		result += "</div>"
	result += "<h1>" + mainTitle + "</h1>\n"
	result += "<p id='version'><strong>Library Version:</strong> <a href='" + documentationPath + "ReleaseNotes.html'><script type='text/javascript'>document.write(osxVersion);</script></a> - <strong>Built on: </strong><script type='text/javascript'>document.write(osxVersionDate);</script></p>\n"
	result += "</div>\n"
	result += "<div style='clear:both;'>&nbsp;</div>"

	return result



def getHTMLSponsoredLinks():
	""" Get the sponsored links area """
	
	result = "<div id='google'>\n"
	result += "<script type='text/javascript'><!--\n"
	result += "google_ad_client = 'pub-5631233433203577';\n"
	result += "/* 728x15, created 18/03/08 */\n"
	result += "google_ad_slot = '0268115694';\n"
	result += "google_ad_width = 728;\n"
	result += "google_ad_height = 30;\n"
	result += "//-->\n"
	result += "</script>\n"
	result += "<script type='text/javascript' src='http://pagead2.googlesyndication.com/pagead/show_ads.js'>\n"
	result += "</script>"
	result += "</div>"
	return result


def getHTMLFooter(documentationPath):
	""" Get the standard footer for all documentation files """
	
	result = "<div id='footer'>"
	result += "<div style='float:left; margin-right:1em;'><a rel='license' class='nounderline' href='http://creativecommons.org/licenses/by-nc-nd/3.0/' onclick='window.open(this.href);return false;'><img alt='Creative Commons License' class='icon' src='" + documentationPath + "cc_logo.png' /></a></div>"
	result += "The OpenSceneryX library is licensed under a <a rel='license' href='http://creativecommons.org/licenses/by-nc-nd/3.0/' onclick='window.open(this.href);return false;'>Creative Commons Attribution-Noncommercial-No Derivative Works 3.0 License</a>. 'The Work' is defined as the library as a whole and by using the library you signify agreement to these terms. <strong>You must obtain the permission of the author(s) if you wish to distribute individual files from this library for any purpose</strong>, as this constitutes a derivative work, which is forbidden under the licence."
	result += "</div>"
	result += "<script src='http://www.google-analytics.com/urchin.js' type='text/javascript'></script>"
	result += "<script type='text/javascript'>"
	result += "_uacct = 'UA-4008328-4';"
	result += "urchinTracker();"
	result += "</script>"
	result += "</body></html>"
	return result



def getHTMLTOC(rootCategory):
	""" Get the table of contents for the home page """
	
	result = "<div id='toc'>\n"
	result += "<h2>Contents</h2>\n"
	result += "<ul id='menu1' class='menu noaccordion'>\n"
	
	for mainSceneryCategory in rootCategory.childSceneryCategories:
		result += "<li>\n"
		result += "<a href='#'>" + mainSceneryCategory.title + "</a>\n"
		result += "<ul class='hide'>\n"

		if len(mainSceneryCategory.childSceneryCategories) > 0:
			for subSceneryCategory in mainSceneryCategory.childSceneryCategories:
				result += "<li>\n"

				result += "<a href='" + subSceneryCategory.url + "'>" + subSceneryCategory.title + "</a>\n"
				#result += "<ul>\n"
				
				#if len(subSceneryCategory.childSceneryCategories) > 0:
				#	# We have another level of categorisation, show a category list where each link takes the user to a
				#	# landing page for that category
				#	for subsubSceneryCategory in subSceneryCategory.childSceneryCategories:
				#		result += "<li><a href='" + subsubSceneryCategory.url + "'>" + subsubSceneryCategory.title + "</a>"
				#		result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/variations.gif' alt='Multiple Variants Available' /><span>Multiple variants available</span></a>"
				#		result += "</li>\n"
	
				#	# Also show the list of objects directly in this category
				#	sceneryObjects = subSceneryCategory.getSceneryObjects(0)
				#	result += getHTMLSceneryObjects(sceneryObjects)
					
				#else:
				#	# No more category levels, show the list of objects
				#	sceneryObjects = subSceneryCategory.getSceneryObjects(1)
				#	result += getHTMLSceneryObjects(sceneryObjects)

				#result += "</ul>\n"
				result += "</li>\n"
				
		else:
			# No categorisation, show the list of objects
			result += "<ul class='inline'>\n"
			sceneryObjects = mainSceneryCategory.getSceneryObjects(1)
			result += getHTMLSceneryObjects(sceneryObjects)				 
			result += "</ul>\n"

		result += "</ul>\n"
		result += "</li>\n"
		
	result += "</ul>\n"
	
	result += "<div id='twitter'>\n"
	result += "<script src='http://widgets.twimg.com/j/2/widget.js'></script>\n"
	result += "<script>\n"
	result += "new TWTR.Widget({\n"
	result += "  version: 2,\n"
	result += "  type: 'profile',\n"
	result += "  rpp: 4,\n"
	result += "  interval: 6000,\n"
	result += "  width: 'auto',\n"
	result += "  height: 300,\n"
	result += "  theme: {\n"
	result += "    shell: {\n"
	result += "      background: '#eeeeff',\n"
	result += "      color: '#333333'\n"
	result += "    },\n"
	result += "    tweets: {\n"
	result += "      background: '#eeeeff',\n"
	result += "      color: '#333333',\n"
	result += "      links: '#4aed05'\n"
	result += "    }\n"
	result += "  },\n"
	result += "  features: {\n"
	result += "    scrollbar: false,\n"
	result += "    loop: false,\n"
	result += "    live: false,\n"
	result += "    hashtags: true,\n"
	result += "    timestamp: true,\n"
	result += "    avatars: false,\n"
	result += "    behavior: 'all'\n"
	result += "  }\n"
	result += "}).render().setUser('opensceneryx').start();\n"
	result += "</script>\n"
	result += "</div>\n"

	result += "</div>\n"

	return result



def getHTMLSceneryObjects(sceneryObjects):
	""" Display a group of scenery objects in the Table of Contents """
	
	result = ""
	for sceneryObject in sceneryObjects:
		result += "<li><a href='/" + sceneryObject.filePathRoot + "/index.html'>" + sceneryObject.shortTitle + "</a>"
	 
		if (sceneryObject.note != ""):
			result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/note.gif' alt='Important Usage Notes' /><span>There are important usage notes for this object</span></a>"

		if (sceneryObject.tutorial):
			result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/tutorial.gif' alt='Tutorial Available' /><span>Tutorial available</span></a>"

		if (sceneryObject.animated):
			result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/animated.gif' alt='Animated' /><span>Animated</span></a>"

		result += "</li>\n"
		
	return result



def getLibraryHeader(versionTag):
	""" Get the standard library.txt header """
	
	result = "A\n"
	result += "800\n"
	result += "LIBRARY\n"
	result += "\n"
	result += "# Version: v" + versionTag + "\n"
	result += "\n"
	return result



def matchesAny(name, tests):
	""" Utility function to find whether a given string is found in a list """
	
	for test in tests:
		if fnmatch.fnmatch(name, test):
			return True
	return False



def caseinsensitive_sort(stringList):
	""" Case-insensitive string comparison sort. usage: stringList = caseinsensitive_sort(stringList) """
	
	tupleList = [(x.lower(), x) for x in stringList]
	tupleList.sort()
	stringList[:] = [x[1] for x in tupleList]



def displayMessage(message, type="message"):
	""" Display a message to the user of a given type (determines message colour) """
	
	if (type == "error"):
		pcrt.fg(pcrt.RED)
		print "ERROR: " + message,
		pcrt.fg(pcrt.WHITE)
	elif (type == "warning"):
		pcrt.fg(pcrt.YELLOW)
		print "WARNING: " + message,
		pcrt.fg(pcrt.WHITE)
	elif (type == "note"):
		pcrt.fg(pcrt.CYAN)
		print "NOTE: " + message,
		pcrt.fg(pcrt.WHITE)
	elif (type == "message"):
		pcrt.fg(pcrt.WHITE)
		print message,

	sys.stdout.flush()


def getInput(message, maxSize):
	""" Get some input from the user """
	
	return raw_input(message)
