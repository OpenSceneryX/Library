#!/usr/local/bin/python
# Script to build a library release
# Copyright (c) 2007 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
# If this script is used to generate a scenery library other than OpenSceneryX, recognition MUST be given
# to the author in any documentation accompanying the library.
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
		functions.displayMessage("========================\n")
		functions.displayMessage("OpenSceneryX Release\n")
		functions.displayMessage("========================\n")
		
		if not os.path.isdir("../files") or not os.path.isdir("../../tags"):
			raise classes.BuildError("Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library")
		
		versionTag = ""
		while versionTag == "":
			versionTag = functions.getInput("Enter the release tag (e.g. 1.0.1): ", 10)
		
		classes.Configuration.setVersionTag(versionTag)
		
		os.chdir("../..")
		
		update = functions.getInput("Do you want to update the \'files\' directory from the repository before release? [y/N]: ", 1)
		
		if update == "Y" or update == "y":
			print "Would svn update trunk/files"
		#		svn update trunk/files
		
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating release paths\n")
		# print "svn mkdir tags/" + classes.Configuration.versionNumber
		classes.Configuration.makeFolders()
		# status = os.system("svn mkdir tags/" + classes.Configuration.versionNumber)
		
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating library.txt\n")
		libraryFileHandle = open(classes.Configuration.osxFolder + "/library.txt", "w")
		libraryPlaceholderFileHandle = open(classes.Configuration.osxPlaceholderFolder + "/library.txt", "w")
		libraryFileHandle.write(functions.getLibraryHeader())
		libraryPlaceholderFileHandle.write(functions.getLibraryHeader())
		
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating HTML files\n")
		
		htmlIndexFileHandle = open(classes.Configuration.osxFolder + "/ReadMe.html", "w")
		htmlIndexFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX Object Library for X-Plane&reg;", ""))
		htmlReleaseNotesFileHandle = open(classes.Configuration.osxFolder + "/doc/ReleaseNotes.html", "w")
		htmlReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", ""))
		jsVersionInfoFileHandle = open(classes.Configuration.osxFolder + "/doc/versionInfo.js", "w")

		htmlDeveloperFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/ReadMe.html", "w")
		htmlDeveloperFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX Developer Pack", ""))
		htmlDeveloperReleaseNotesFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/doc/ReleaseNotes.html", "w")
		htmlDeveloperReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", ""))
		jsDeveloperVersionInfoFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/doc/versionInfo.js", "w")
		
		htmlWebIndexFileHandle = open(classes.Configuration.osxWebsiteFolder + "/index.html", "w")
		htmlWebIndexFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX Object Library for X-Plane&reg;", ""))
		htmlWebReleaseNotesFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/ReleaseNotes.html", "w")
		htmlWebReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", ""))
		jsWebVersionInfoFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/versionInfo.js", "w")
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Copying files\n")
		shutil.copyfile("trunk/support/all.css", classes.Configuration.osxFolder + "/doc/all.css")
		shutil.copyfile("trunk/support/tabbo.css", classes.Configuration.osxFolder + "/doc/tabbo.css")
		shutil.copyfile("trunk/support/tabbo.js", classes.Configuration.osxFolder + "/doc/tabbo.js")
		shutil.copyfile("trunk/support/cc_logo.png", classes.Configuration.osxFolder + "/doc/cc_logo.png")
		
		shutil.copyfile("trunk/support/all.css", classes.Configuration.osxDeveloperPackFolder + "/doc/all.css")
		shutil.copyfile("trunk/support/tabbo.css", classes.Configuration.osxDeveloperPackFolder + "/doc/tabbo.css")
		shutil.copyfile("trunk/support/tabbo.js", classes.Configuration.osxDeveloperPackFolder + "/doc/tabbo.js")
		shutil.copyfile("trunk/support/cc_logo.png", classes.Configuration.osxDeveloperPackFolder + "/doc/cc_logo.png")
		shutil.copyfile("trunk/support/enhancedby_opensceneryx_logo.gif", classes.Configuration.osxPlaceholderFolder + "/enhancedby_opensceneryx_logo.gif")
		
		shutil.copyfile("trunk/support/all.css", classes.Configuration.osxWebsiteFolder + "/doc/all.css")
		shutil.copyfile("trunk/support/tabbo.css", classes.Configuration.osxWebsiteFolder + "/doc/tabbo.css")
		shutil.copyfile("trunk/support/tabbo.js", classes.Configuration.osxWebsiteFolder + "/doc/tabbo.js")
		shutil.copyfile("trunk/support/cube.gif", classes.Configuration.osxWebsiteFolder + "/doc/cube.gif")
		shutil.copyfile("trunk/support/bullet_object.gif", classes.Configuration.osxWebsiteFolder + "/doc/bullet_object.gif")
		shutil.copyfile("trunk/support/cc_logo.png", classes.Configuration.osxWebsiteFolder + "/doc/cc_logo.png")
		shutil.copyfile("trunk/support/pdf.gif", classes.Configuration.osxWebsiteFolder + "/doc/pdf.gif")
		shutil.copyfile("trunk/support/tutorial.gif", classes.Configuration.osxWebsiteFolder + "/doc/tutorial.gif")
		shutil.copyfile("trunk/support/animated.gif", classes.Configuration.osxWebsiteFolder + "/doc/animated.gif")
		shutil.copyfile("trunk/support/variations.gif", classes.Configuration.osxWebsiteFolder + "/doc/variations.gif")
		shutil.copyfile("trunk/support/favicon.ico", classes.Configuration.osxWebsiteFolder + "/favicon.ico")
		shutil.copyfile("trunk/support/screenshot_missing.png", classes.Configuration.osxWebsiteFolder + "/doc/screenshot_missing.png")
		
		shutil.copyfile("trunk/support/placeholder.obj", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.obj")
		shutil.copyfile("trunk/support/placeholder.for", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.for")
		shutil.copyfile("trunk/support/placeholder.fac", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.fac")
		
		authors = []
		rootCategory = classes.SceneryCategory("")
		# 'textures' contains a dictionary where the key is the texture filepath
		# and the value is a SceneryTexture object
		textures = {}
		
		functions.handleFolder("trunk/files", rootCategory, libraryFileHandle, libraryPlaceholderFileHandle, authors, textures)
		
		functions.caseinsensitive_sort(authors)
		rootCategory.sort()
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building Category Landing Pages\n")
		functions.buildCategoryLandingPages(rootCategory, 0)
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building Object Documentation\n")
		functions.buildDocumentation(rootCategory, 0)
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building ancilliary files\n")
		toc = functions.getHTMLTOC(rootCategory)
		htmlWebIndexFileHandle.write(toc)
		
		authors = ", ".join(authors[:-1]) + " and " + authors[-1]
		
		file = open("trunk/support/_index.html", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		fileContents = fileContents.replace("${authors}", authors)
		fileContents = fileContents.replace("${objectCount}", str(rootCategory.getSceneryObjectCount(1)))
		file.close()
		htmlIndexFileHandle.write(fileContents)
		
		file = open("trunk/support/_developerinstructions.html", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		file.close()
		htmlDeveloperFileHandle.write(fileContents)
		
		file = open("trunk/support/_releasenotes.html", "r")
		fileContents = file.read()
		file.close()
		htmlReleaseNotesFileHandle.write(fileContents)
		htmlDeveloperReleaseNotesFileHandle.write(fileContents)
		htmlWebReleaseNotesFileHandle.write(fileContents)
		
		file = open("trunk/support/_webindex.html", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		fileContents = fileContents.replace("${authors}", authors)
		fileContents = fileContents.replace("${objectCount}", str(rootCategory.getSceneryObjectCount(1)))
		file.close()
		htmlWebIndexFileHandle.write(fileContents)
		
		file = open("trunk/support/_versionInfo.js", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		fileContents = fileContents.replace("${versionDate}", classes.Configuration.versionDate)
		file.close()
		jsVersionInfoFileHandle.write(fileContents)
		jsDeveloperVersionInfoFileHandle.write(fileContents)
		jsWebVersionInfoFileHandle.write(fileContents)
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Finishing and closing files\n")
		htmlIndexFileHandle.write(functions.getHTMLFooter("doc/"))
		htmlDeveloperFileHandle.write(functions.getHTMLFooter("doc/"))
		htmlReleaseNotesFileHandle.write(functions.getHTMLFooter(""))
		htmlWebIndexFileHandle.write(functions.getHTMLFooter("doc/"))
		
		htmlIndexFileHandle.close()
		htmlDeveloperFileHandle.close()
		libraryFileHandle.close()
		libraryPlaceholderFileHandle.close()
		htmlWebIndexFileHandle.close()
		jsVersionInfoFileHandle.close()
		jsDeveloperVersionInfoFileHandle.close()
		jsWebVersionInfoFileHandle.close()
		
		
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
