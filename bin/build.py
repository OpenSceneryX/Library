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
	from PIL import Image

except ImportError:
	Image = None

try:
	# Include common functions
	import os
	import shutil
	import urllib
	import pcrt
	
	exceptionMessage = ""
	showTraceback = 0
	
	try:
		functions.growlRegister()

		functions.displayMessage("========================\n")
		functions.displayMessage("OpenSceneryX Release\n")
		functions.displayMessage("========================\n")
		
		if not os.path.isdir("../files") or not os.path.isdir("../builds"):
			functions.displayMessage("This script must be run from the 'bin' directory inside a full checkout of the scenery library\n", "error")
			sys.exit()
		
		versionTag = ""
		while versionTag == "":
			versionTag = functions.getInput("Enter the release tag (e.g. 1.0.1): ", 10)
		
		os.chdir("..")
		
		buildPDF = functions.getInput("Build PDF? [y/N]: ", 1)
		
		classes.Configuration.init(versionTag, buildPDF)
		
		if Image is None:
			functions.displayMessage("This script depends on PIL and fpdf for building the developer documentation.  Please ensure they are installed ('pip install Pillow' and 'pip install fpdf').\n", "error")
					
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating release paths\n")
		# print "svn mkdir tags/" + classes.Configuration.versionNumber
		classes.Configuration.makeFolders()
		# status = os.system("svn mkdir tags/" + classes.Configuration.versionNumber)
		
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating library.txt\n")
		libraryFileHandle = open(classes.Configuration.osxFolder + "/library.txt", "w")
		libraryPlaceholderFileHandle = open(classes.Configuration.osxPlaceholderFolder + "/library.txt", "w")
		libraryFileHandle.write(functions.getLibraryHeader(versionTag, False))
		libraryPlaceholderFileHandle.write(functions.getLibraryHeader(versionTag, True))
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating HTML files and sitemap.xml \n")
		
		htmlIndexFileHandle = open(classes.Configuration.osxFolder + "/ReadMe.html", "w")
		htmlIndexFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX Object Library for X-Plane&reg;", "", False, False))
		htmlReleaseNotesFileHandle = open(classes.Configuration.osxFolder + "/doc/ReleaseNotes.html", "w")
		htmlReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg; - Release Notes for Latest Version", "", False, False))
		jsVersionInfoFileHandle = open(classes.Configuration.osxFolder + "/doc/versionInfo.js", "w")

		htmlDeveloperFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/ReadMe.html", "w")
		htmlDeveloperFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX Developer Pack", "", False, False))
		htmlDeveloperReleaseNotesFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/doc/ReleaseNotes.html", "w")
		htmlDeveloperReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg; - Release Notes", "", False, False))
		jsDeveloperVersionInfoFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/doc/versionInfo.js", "w")
		
		htmlWebReleaseNotesFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/ReleaseNotes.html", "w")
		jsWebVersionInfoFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/versionInfo.js", "w")
		
		sitemapXMLFileHandle = open(classes.Configuration.osxWebsiteFolder + "/library-sitemap.xml", "w")
		sitemapXMLFileHandle.write(functions.getXMLSitemapHeader())
		functions.writeXMLSitemapEntry(sitemapXMLFileHandle, "/", "1.0")
		functions.writeXMLSitemapEntry(sitemapXMLFileHandle, "/doc/ReleaseNotes.html", "0.9")
				
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Copying files\n")
		
		# Main OSX Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/all.css", classes.Configuration.osxFolder + "/doc/all.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/ie7.css", classes.Configuration.osxFolder + "/doc/ie7.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/cc_logo.png", classes.Configuration.osxFolder + "/doc/cc_logo.png")
		
		# Developer Pack Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/all.css", classes.Configuration.osxDeveloperPackFolder + "/doc/all.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/ie7.css", classes.Configuration.osxDeveloperPackFolder + "/doc/ie7.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/cc_logo.png", classes.Configuration.osxDeveloperPackFolder + "/doc/cc_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/pdf.gif", classes.Configuration.osxDeveloperPackFolder + "/doc/pdf.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/enhancedby_opensceneryx_logo.png", classes.Configuration.osxPlaceholderFolder + "/enhancedby_opensceneryx_logo.png")
		
		# Website Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/all.css", classes.Configuration.osxWebsiteFolder + "/doc/all.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/ie7.css", classes.Configuration.osxWebsiteFolder + "/doc/ie7.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/tabbo.css", classes.Configuration.osxWebsiteFolder + "/doc/tabbo.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/tabbo.js", classes.Configuration.osxWebsiteFolder + "/doc/tabbo.js")
		shutil.copyfile(classes.Configuration.supportFolder + "/scripts.js", classes.Configuration.osxWebsiteFolder + "/doc/scripts.js")
		shutil.copyfile(classes.Configuration.supportFolder + "/cube.gif", classes.Configuration.osxWebsiteFolder + "/doc/cube.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/bullet_object.gif", classes.Configuration.osxWebsiteFolder + "/doc/bullet_object.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/cc_logo.png", classes.Configuration.osxWebsiteFolder + "/doc/cc_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/pdf.gif", classes.Configuration.osxWebsiteFolder + "/doc/pdf.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/tutorial.gif", classes.Configuration.osxWebsiteFolder + "/doc/tutorial.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/animated.gif", classes.Configuration.osxWebsiteFolder + "/doc/animated.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/variations.gif", classes.Configuration.osxWebsiteFolder + "/doc/variations.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/note.gif", classes.Configuration.osxWebsiteFolder + "/doc/note.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/screenshot_missing.png", classes.Configuration.osxWebsiteFolder + "/doc/screenshot_missing.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/glass_numbers_1.png", classes.Configuration.osxWebsiteFolder + "/doc/glass_numbers_1.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/glass_numbers_2.png", classes.Configuration.osxWebsiteFolder + "/doc/glass_numbers_2.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/glass_numbers_3.png", classes.Configuration.osxWebsiteFolder + "/doc/glass_numbers_3.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/plus.png", classes.Configuration.osxWebsiteFolder + "/doc/plus.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/minus.png", classes.Configuration.osxWebsiteFolder + "/doc/minus.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/001_52.png", classes.Configuration.osxWebsiteFolder + "/doc/001_52.png")

		shutil.copyfile(classes.Configuration.supportFolder + "/osx.gif", classes.Configuration.osxWebsiteFolder + "/extras/osx.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/enhancedby_opensceneryx_logo.png", classes.Configuration.osxWebsiteFolder + "/extras/enhancedby_opensceneryx_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/twitter_follow.png", classes.Configuration.osxWebsiteFolder + "/extras/twitter_follow.png")
		
		# Placeholder items for main package
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.png", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.obj", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.for", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.fac", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.lin", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.pol", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.pol")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.png", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.obj", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.for", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.fac", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.lin", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.pol", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.pol")
		# Need to copy them to the placeholder path so that the monolithic zip install works out of the box too
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.png", classes.Configuration.osxFolder + "/opensceneryx/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.obj", classes.Configuration.osxFolder + "/opensceneryx/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.for", classes.Configuration.osxFolder + "/opensceneryx/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.fac", classes.Configuration.osxFolder + "/opensceneryx/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.lin", classes.Configuration.osxFolder + "/opensceneryx/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.pol", classes.Configuration.osxFolder + "/opensceneryx/placeholder.pol")

		# Placeholder Library Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.png", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.obj", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.for", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.fac", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.lin", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.pol", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.pol")
		
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building Library\n")

		authors = []
		rootCategory = classes.SceneryCategory("", None)
		# 'textures' contains a dictionary where the key is the texture filepath
		# and the value is a SceneryTexture object
		textures = {}
		
		# toc contains a multi-dimensional dictionary of all library content in the virtual path structure
		toc = []
		
		functions.handleFolder("files", rootCategory, libraryFileHandle, libraryPlaceholderFileHandle, authors, textures, toc)
		
		functions.caseinsensitiveSort(authors)
		rootCategory.sort()
		
		functions.displayMessage("\n------------------------\n")
		functions.displayMessage("Building Category Landing Pages\n")
		functions.buildCategoryLandingPages(sitemapXMLFileHandle, rootCategory)
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building Object Documentation\n")
		functions.buildDocumentation(sitemapXMLFileHandle, rootCategory, 0)
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building ancilliary files\n")
		
		authors = ", ".join(authors[:-1]) + " and " + authors[-1]
		
		file = open(classes.Configuration.supportFolder + "/_index.html", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		fileContents = fileContents.replace("${authors}", authors)
		fileContents = fileContents.replace("${objectCount}", str(rootCategory.getSceneryObjectCount(1)))
		file.close()
		htmlIndexFileHandle.write(fileContents)
		
		file = open(classes.Configuration.supportFolder + "/_developerinstructions.html", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		file.close()
		htmlDeveloperFileHandle.write(fileContents)
		
		file = open(classes.Configuration.supportFolder + "/_releasenotes.html", "r")
		fileContents = file.read()
		file.close()
		htmlReleaseNotesFileHandle.write("<div id='content'><a name='content'></a>" + fileContents + "</div>")
		htmlDeveloperReleaseNotesFileHandle.write("<div id='content'><a name='content'></a>" + fileContents + "</div>")
		htmlWebReleaseNotesFileHandle.write(fileContents)
		
		file = open(classes.Configuration.supportFolder + "/_versionInfo.js", "r")
		fileContents = file.read()
		fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
		fileContents = fileContents.replace("${versionDate}", classes.Configuration.versionDate)
		fileContents = fileContents.replace("${authors}", authors)
		fileContents = fileContents.replace("${objectCount}", str(rootCategory.getSceneryObjectCount(1)))
		file.close()
		jsVersionInfoFileHandle.write(fileContents)
		jsDeveloperVersionInfoFileHandle.write(fileContents)
		jsWebVersionInfoFileHandle.write(fileContents)
		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Finishing and closing files\n")
		htmlIndexFileHandle.write(functions.getHTMLFooter("doc/"))
		htmlDeveloperFileHandle.write(functions.getHTMLFooter("doc/"))
		htmlReleaseNotesFileHandle.write(functions.getHTMLFooter(""))

		functions.writeBackupLibraries(libraryFileHandle)

		sitemapXMLFileHandle.write(functions.getXMLSitemapFooter())

		htmlIndexFileHandle.close()
		htmlDeveloperFileHandle.close()
		libraryFileHandle.close()
		libraryPlaceholderFileHandle.close()
		sitemapXMLFileHandle.close()
		jsVersionInfoFileHandle.close()
		jsDeveloperVersionInfoFileHandle.close()
		jsWebVersionInfoFileHandle.close()
		
		functions.closePDF(classes.Configuration.osxDeveloperPackFolder + "/doc/Reference.pdf")

		
		functions.displayMessage("------------------------\n")
		functions.displayMessage("Complete\n")
		functions.displayMessage("========================\n")
		
		functions.growlNotify("OpenSceneryX build completed")
		
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
