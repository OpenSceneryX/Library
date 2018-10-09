#!/usr/local/bin/python
# Script to add a new set of Bertrand Augras aircraft using a new livery 
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
	
	exceptionMessage = ""
	showTraceback = 0
	
	try:
		functions.displayMessage("=================================\n")
		functions.displayMessage("Bertrand Augras Aircraft Addition\n")
		functions.displayMessage("=================================\n")
		
		filesFolder = "files"
		
		if not os.path.isdir("../" + filesFolder):
			raise classes.BuildError("Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library")

		os.chdir("../..")
		
		sourceTextureFolder = ""
		while sourceTextureFolder == "":
			sourceTextureFolder = functions.getInput("Enter the name of the source texture folder inside the shared_textures folder (e.g. bertrand_augras/aeroflot): ", 100)
			lastSlash = sourceTextureFolder.rfind("/")
			if not os.path.isdir("trunk/" + filesFolder + "/objects/shared_textures/" + sourceTextureFolder):
				functions.displayMessage("The " + "/objects/shared_textures/" + sourceTextureFolder + " folder doesn't exist, please enter another\n", "error")
				sourceTextureFolder = ""
			elif lastSlash == -1:
				functions.displayMessage("The specified folder cannot be in the root of shared_textures\n", "error")
				sourceTextureFolder = ""
			elif not os.path.isfile("trunk/" + filesFolder + "/objects/shared_textures/" + sourceTextureFolder + "/texture.png"):
				functions.displayMessage("The specified folder does not contain a 'texture.png' file\n", "error")
				sourceTextureFolder = ""
			elif not os.path.isfile("trunk/" + filesFolder + "/objects/shared_textures/" + sourceTextureFolder + "/texture_LIT.png"):
				functions.displayMessage("The specified folder does not contain a 'texture_LIT.png' file\n", "error")
				sourceTextureFolder = ""
			else:
				liveryFolderName = sourceTextureFolder[lastSlash + 1:]
	
		functions.displayMessage("liveryFolderName: " + liveryFolderName + "\n", "note")
		
		liveryTitle = ""
		while liveryTitle == "":
			liveryTitle = functions.getInput("Enter the livery title for use in the info.txt file (e.g. Aeroflot): ", 100)

		textureAuthor = ""
		while textureAuthor == "":
			textureAuthor = functions.getInput("Enter the texture author for use in the info.txt file (e.g. Bertrand Augras): ", 100)

		textureURL = ""
		while textureURL == "":
			textureURL = functions.getInput("Enter the texture author URL for use in the info.txt file (e.g. https://forums.x-plane.org/index.php?showuser=3814): ", 100)


		aircraftPaths = ["objects/aircraft/jets/heavy/a310", "objects/aircraft/jets/heavy/a320", "objects/aircraft/jets/heavy/a340", "objects/aircraft/jets/heavy/a380", "objects/aircraft/jets/heavy/b737-700", "objects/aircraft/jets/heavy/b747-400", "objects/aircraft/jets/heavy/b757-200", "objects/aircraft/jets/heavy/md11", "objects/aircraft/jets/heavy/md90-50", "objects/aircraft/jets/regional_commuter/avro-rj70", "objects/aircraft/jets/regional_commuter/erj-145", "objects/aircraft/props/regional_commuter/atr-42", "objects/aircraft/props/regional_commuter/beech-b1900", "objects/aircraft/props/regional_commuter/dornier-d328", "objects/aircraft/props/regional_commuter/emb-120", "objects/aircraft/props/regional_commuter/fokker-50", "objects/aircraft/props/regional_commuter/saab-340"]

		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Working\n")
		
		for aircraftPath in aircraftPaths:
			fullDestinationPath = "trunk/" + filesFolder + "/" + aircraftPath + "/" + liveryFolderName
			fullAeroflotPath = "trunk/" + filesFolder + "/" + aircraftPath + "/aeroflot"
			
			if os.path.isdir(fullDestinationPath):
				functions.displayMessage(fullDestinationPath + " already exists, skipping\n", "warning")
			else:
				# Create the destination folder
				os.mkdir(fullDestinationPath)
				
				# Create the modified info.txt file
				sourceFile = open(fullAeroflotPath + "/info.txt", "r")
				destinationFile = open(fullDestinationPath + "/info.txt", "w")
				fileContents = sourceFile.read()
				fileContents = fileContents.replace("Aeroflot", liveryTitle)
				fileContents = fileContents.replace("aeroflot", liveryFolderName)
				fileContents = fileContents.replace("URL: https://forums.x-plane.org/index.php?showuser=3814\n", "URL: https://forums.x-plane.org/index.php?showuser=3814\nAuthor, texture: " + textureAuthor + "\nURL, texture: " + textureURL + "\n")
				sourceFile.close()
				destinationFile.write(fileContents)
				destinationFile.close()
				
				# Create the modified object.obj file
				sourceFile = open(fullAeroflotPath + "/object.obj", "r")
				destinationFile = open(fullDestinationPath + "/object.obj", "w")
				fileContents = sourceFile.read()
				fileContents = fileContents.replace("bertrand_augras/aeroflot", sourceTextureFolder)
				sourceFile.close()
				destinationFile.write(fileContents)
				destinationFile.close()


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
