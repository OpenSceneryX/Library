#!/usr/local/bin/python
# Script to update alpilotx's Forests with a new version.  Note this only updates
# the forest definitions, the texture needs to be done manually
# Copyright (c) 2008 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
# Version: $Revision$

import sys
import traceback

try:
	import classes
	import functions
	
except:
	traceback.print_exc()
	sys.exit()
	
try:
	# Include common functions
	import os
	import shutil
	import urllib
	import pcrt
	import re
	
	exceptionMessage = ""
	showTraceback = 0
	
	try:
		functions.displayMessage("======================\n")
		functions.displayMessage("alpilotx Forest Update\n")
		functions.displayMessage("======================\n")
		
		if not os.path.isdir(".." + os.sep + "files"):
			raise classes.BuildError("Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library")

		if not os.path.isdir(".." + os.sep + ".." + os.sep + "submissions" + os.sep + "alpilotx"):
			raise classes.BuildError("Error: The 'submissions' folder must contain an 'alpilotx' folder containing the source files")

		os.chdir(".." + os.sep + "..")
		
		europeUS = ""
		
		while (europeUS != "e" and europeUS != "u"):
			europeUS = functions.getInput("Europe or US? [e/u]: ", 1)
			
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Working\n")
		
		if (europeUS == "e"):
			mappingFile = "europe_forest_mapping.txt"
			continentTitle = "European"
		else:
			mappingFile = "us_forest_mapping.txt"
			continentTitle = "USA"
		
		file = open("trunk" + os.sep + "bin" + os.sep + mappingFile)
		mappingFileContents = file.readlines()
		file.close()

		mappingPattern = re.compile("(.*)\t(.*)")
		texturePattern = re.compile("TEXTURE\s+(.*)")
		
		for line in mappingFileContents:
			result = mappingPattern.match(line)
			if result:
				src = "submissions" + os.sep + "alpilotx" + os.sep + result.group(1)
				dest = "trunk" + os.sep + "files" + os.sep + result.group(2)
		
			functions.displayMessage("Copying from: " + src + " to: " + dest + "\n", "note")
			
			file = open(src)
			treeFileContents = file.read()
			file.close()
			
			treeFileContents = texturePattern.sub(r"TEXTURE ../../../\1", treeFileContents)
			
			destFileParts = dest.split("/")
			
			# Create destination folders
			destFolder = "/".join(destFileParts[:-1])
			if not os.path.isdir(destFolder):
				os.makedirs(destFolder)

			# Create category file
			categoryFile = "/".join(destFileParts[:-2]) + "/category.txt"
			regionTitle = destFileParts[-3].replace("_", " ").title()
			file = open(categoryFile, "w")
			file.write("Title: " + continentTitle + ", " + regionTitle + "\n")
			file.write("=====================\n\n")
			file.close()
			
			# Create forest file
			file = open(dest, "w")
			file.write(treeFileContents)
			file.close()
			
			# Create info file
			infoFile = "/".join(destFileParts[:-1]) + "/info.txt"
			treeType = destFileParts[-2].replace("_", " ").title()
			file = open(infoFile, "w")
			file.write("Title: " + continentTitle + " Forest, " + regionTitle + ", " + treeType + "\n")
			file.write("Short Title: " + treeType + "\n")
			file.write("=====================\n")
			file.write("Author: Andras Fabian\n")
			file.write("URL: http://www.alpilotx.de/\n")
			file.write("Author, texture: Albert Laubi\n")
			file.write("Author, texture: Sergio Santagada\n")
			file.write("Revision: $Revision$\n")
			file.write("Date: $Date$\n")
			file.write("=====================\n")
			file.write("Description: A forest of trees.  See <a href='http://www.alpilotx.de/mambo/index.php?option=com_content&task=view&id=34&Itemid=43' onclick='window.open(this.href);return false;'>this page</a> for documentation containing a map of the " + continentTitle + " areas.\n")
			file.close()

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Complete\n")
		functions.displayMessage("========================\n")
		
	except classes.BuildError, e:
		exceptionMessage = e.value
	else:
		showTraceback = 1
	
finally:
	pcrt.reset()
	if (exceptionMessage != ""):
		print exceptionMessage
		
	if (showTraceback == 1):
		traceback.print_exc()
