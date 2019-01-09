# -*- coding: utf-8 -*-
# Script to build a library release
# Copyright (c) 2007 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
# If this script is used to generate a scenery library other than OpenSceneryX, recognition MUST be given
# to the author in any documentation accompanying the library.
# Version: $Revision$

import sys
import traceback
import random

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

	exceptionMessage = ""
	showTraceback = 0

	try:
		functions.displayMessage("========================\n")
		functions.displayMessage("OpenSceneryX Release\n")
		functions.displayMessage("========================\n")

		if not os.path.isdir("../files") or not os.path.isdir("../builds"):
			functions.displayMessage("This script must be run from the 'bin' directory inside a full checkout of the scenery library\n", "error")
			sys.exit()

		versionTag = ""
		while versionTag == "":
			versionTag = functions.getInput("Enter the library version number (e.g. 1.0.1): ", 10)

		sinceVersionTag = ""
		sinceVersionTag = functions.getInput("Version number to build latest objects from [" + versionTag + "]: ", 10)
		if sinceVersionTag == "":
			sinceVersionTag = versionTag

		buildPDF = functions.getInput("Build PDF? [y/N]: ", 1)

		classes.Configuration.init(versionTag, sinceVersionTag, buildPDF)

		if Image is None:
			functions.displayMessage("This script depends on PIL and fpdf for building the developer documentation.  Please ensure they are installed ('pip install Pillow' and 'pip install fpdf').\n", "error")

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating release paths\n")

		os.chdir("..")
		classes.Configuration.makeFolders()

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating library.txt\n")

		libraryFileHandle = open(classes.Configuration.osxFolder + "/library.txt", "w")
		libraryPlaceholderFileHandle = open(classes.Configuration.osxPlaceholderFolder + "/library.txt", "w")
		libraryExternalFileHandle = open(classes.Configuration.osxFolder + "/TEMP-external.txt", "w")
		libraryDeprecatedFileHandle = open(classes.Configuration.osxFolder + "/TEMP-deprecated.txt", "w")
		libraryFileHandle.write(functions.getLibraryHeader(versionTag))
		libraryPlaceholderFileHandle.write(functions.getLibraryHeader(versionTag, True))
		libraryExternalFileHandle.write(functions.getLibraryHeader(versionTag, False, "", "Third party libraries integrated with OpenSceneryX"))
		libraryDeprecatedFileHandle.write(functions.getLibraryHeader(versionTag, False, "deprecated"))

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Creating HTML files and sitemap.xml \n")

		htmlIndexFileHandle = open(classes.Configuration.osxFolder + "/ReadMe.html", "w")
		htmlIndexFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX", "", False, False))
		htmlReleaseNotesFileHandle = open(classes.Configuration.osxFolder + "/doc/ReleaseNotes.html", "w")
		htmlReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX - Release Notes", "", False, False))
		jsVersionInfoFileHandle = open(classes.Configuration.osxFolder + "/doc/versionInfo.js", "w")
		versionInfoFileHandle = open(classes.Configuration.osxFolder + "/version.txt", "w")

		htmlDeveloperFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/ReadMe.html", "w")
		htmlDeveloperFileHandle.write(functions.getHTMLHeader("doc/", "OpenSceneryX Developer Pack", "", False, False))
		htmlDeveloperReleaseNotesFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/doc/ReleaseNotes.html", "w")
		htmlDeveloperReleaseNotesFileHandle.write(functions.getHTMLHeader("", "OpenSceneryX - Release Notes", "", False, False))
		jsDeveloperVersionInfoFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/doc/versionInfo.js", "w")

		htmlWebReleaseNotesFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/ReleaseNotes.html", "w")
		jsWebVersionInfoFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/versionInfo.js", "w")

		sitemapXMLFileHandle = open(classes.Configuration.osxWebsiteFolder + "/library-sitemap.xml", "w")
		sitemapXMLFileHandle.write(functions.getXMLSitemapHeader())
		functions.writeXMLSitemapEntry(sitemapXMLFileHandle, "/", "1.0")

		latestItemsFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/latestitems.tsv", "w")

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Copying files\n")

		# Main OSX Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/all.css", classes.Configuration.osxFolder + "/doc/all.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/ie7.css", classes.Configuration.osxFolder + "/doc/ie7.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/cc_logo.png", classes.Configuration.osxFolder + "/doc/cc_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/x_banner_web.png", classes.Configuration.osxFolder + "/doc/x_banner_web.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/twitter_follow.png", classes.Configuration.osxFolder + "/doc/twitter_follow.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/yt_logo.png", classes.Configuration.osxFolder + "/doc/yt_logo.png")

		# Developer Pack Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/all.css", classes.Configuration.osxDeveloperPackFolder + "/doc/all.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/ie7.css", classes.Configuration.osxDeveloperPackFolder + "/doc/ie7.css")
		shutil.copyfile(classes.Configuration.supportFolder + "/cc_logo.png", classes.Configuration.osxDeveloperPackFolder + "/doc/cc_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/x_banner_web.png", classes.Configuration.osxDeveloperPackFolder + "/doc/x_banner_web.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/yt_logo.png", classes.Configuration.osxDeveloperPackFolder + "/doc/yt_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/twitter_follow.png", classes.Configuration.osxDeveloperPackFolder + "/doc/twitter_follow.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/pdf.gif", classes.Configuration.osxDeveloperPackFolder + "/doc/pdf.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/enhancedby_opensceneryx_logo.png", classes.Configuration.osxPlaceholderFolder + "/enhancedby_opensceneryx_logo.png")

		# Website Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/robots.txt", classes.Configuration.osxWebsiteFolder + "/robots.txt")
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
		shutil.copyfile(classes.Configuration.supportFolder + "/001_52.png", classes.Configuration.osxWebsiteFolder + "/doc/001_52.png")

		shutil.copyfile(classes.Configuration.supportFolder + "/osx.gif", classes.Configuration.osxWebsiteFolder + "/extras/osx.gif")
		shutil.copyfile(classes.Configuration.supportFolder + "/enhancedby_opensceneryx_logo.png", classes.Configuration.osxWebsiteFolder + "/extras/enhancedby_opensceneryx_logo.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/twitter_follow.png", classes.Configuration.osxWebsiteFolder + "/extras/twitter_follow.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/x.png", classes.Configuration.osxWebsiteFolder + "/extras/x.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/yt_logo.png", classes.Configuration.osxWebsiteFolder + "/extras/yt_logo.png")

		# Placeholder items for main package
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.agp", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.agp")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.dcl", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.dcl")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.fac", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.for", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.lin", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.net", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.net")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.obj", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.png", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.pol", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.pol")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.str", classes.Configuration.osxFolder + "/placeholders/invisible/placeholder.str")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder_decal.png", classes.Configuration.osxFolder + "/placeholders/visible/placeholder_decal.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.agp", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.agp")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.dcl", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.dcl")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.fac", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.for", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.lin", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.net", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.net")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.obj", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.png", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.pol", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.pol")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.str", classes.Configuration.osxFolder + "/placeholders/visible/placeholder.str")
		# Need to copy them to the placeholder path so that the monolithic zip install works out of the box too
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder_decal.png", classes.Configuration.osxFolder + "/opensceneryx/placeholder_decal.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.agp", classes.Configuration.osxFolder + "/opensceneryx/placeholder.agp")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.dcl", classes.Configuration.osxFolder + "/opensceneryx/placeholder.dcl")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.fac", classes.Configuration.osxFolder + "/opensceneryx/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.for", classes.Configuration.osxFolder + "/opensceneryx/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.lin", classes.Configuration.osxFolder + "/opensceneryx/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.net", classes.Configuration.osxFolder + "/opensceneryx/placeholder.net")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.obj", classes.Configuration.osxFolder + "/opensceneryx/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.png", classes.Configuration.osxFolder + "/opensceneryx/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.pol", classes.Configuration.osxFolder + "/opensceneryx/placeholder.pol")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/visible/placeholder.str", classes.Configuration.osxFolder + "/opensceneryx/placeholder.str")

		# Placeholder Library Folder
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.agp", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.agp")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.dcl", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.dcl")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.fac", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.fac")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.for", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.for")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.lin", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.lin")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.net", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.net")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.obj", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.obj")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.png", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.png")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.pol", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.pol")
		shutil.copyfile(classes.Configuration.supportFolder + "/placeholders/invisible/placeholder.str", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.str")


		functions.displayMessage("------------------------\n")
		functions.displayMessage("Building Library\n")

		authors = []
		rootCategory = classes.SceneryCategory("", None)
		# 'textures' contains a dictionary where the key is the texture filepath
		# and the value is a SceneryTexture object
		textures = {}

		# toc contains a multi-dimensional dictionary of all library content in the virtual path structure
		toc = []

		# latest contains an array of the new SceneryObjects in this version
		latest = []

		functions.handleFolder("files", rootCategory, libraryFileHandle, libraryPlaceholderFileHandle, libraryExternalFileHandle, libraryDeprecatedFileHandle, authors, textures, toc, latest)

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
		versionInfoFileHandle.write(classes.Configuration.versionNumber + " " + classes.Configuration.versionDate)

		random.shuffle(latest)
		for item in latest:
			latestItemsFileHandle.write(item.title + "\t" + item.getWebURL(False) + "\n")

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Finishing and closing files\n")
		htmlIndexFileHandle.write(functions.getHTMLFooter("doc/"))
		htmlDeveloperFileHandle.write(functions.getHTMLFooter("doc/"))
		htmlReleaseNotesFileHandle.write(functions.getHTMLFooter(""))
		sitemapXMLFileHandle.write(functions.getXMLSitemapFooter())

		htmlIndexFileHandle.close()
		htmlDeveloperFileHandle.close()
		libraryExternalFileHandle.close()
		libraryDeprecatedFileHandle.close()

		# Append the deprecated paths to the library
		file = open(classes.Configuration.osxFolder + "/TEMP-deprecated.txt", "r")
		fileContents = file.read()
		libraryFileHandle.write(fileContents)
		file.close()
		os.remove(classes.Configuration.osxFolder + "/TEMP-deprecated.txt")

		# Append the 3rd party paths to the library
		file = open(classes.Configuration.osxFolder + "/TEMP-external.txt", "r")
		fileContents = file.read()
		libraryFileHandle.write(fileContents)
		file.close()
		os.remove(classes.Configuration.osxFolder + "/TEMP-external.txt")

		# Append the backup paths to the library
		functions.writeBackupLibraries(libraryFileHandle)

		libraryFileHandle.close()
		libraryPlaceholderFileHandle.close()
		sitemapXMLFileHandle.close()
		jsVersionInfoFileHandle.close()
		jsDeveloperVersionInfoFileHandle.close()
		jsWebVersionInfoFileHandle.close()
		versionInfoFileHandle.close()
		latestItemsFileHandle.close()

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Writing Developer PDF\n")

		functions.closePDF(classes.Configuration.osxDeveloperPackFolder + "/doc/Reference.pdf")


		functions.displayMessage("------------------------\n")
		functions.displayMessage("Complete\n")
		functions.displayMessage("========================\n")

		functions.osNotify("OpenSceneryX build completed")

	except classes.BuildError as e:
		exceptionMessage = e.value


finally:
	if (exceptionMessage != ""):
		print(exceptionMessage)

