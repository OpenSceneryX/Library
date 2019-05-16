# -*- coding: utf-8 -*-
#
# Script to check a library build against a third party library file to ensure every item has been incuded.
#
# Copyright (c) 2018 Austin Goudge
#
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

	exceptionMessage = ""
	showTraceback = 0

	try:
		functions.displayMessage("========================\n")
		functions.displayMessage("OpenSceneryX Check Third Party\n")
		functions.displayMessage("========================\n")

		os.chdir("..")

		if not os.path.isdir("files") or not os.path.isdir("builds"):
			functions.displayMessage("This script must be run from the 'bin' directory inside a full checkout of the scenery library\n", "error")
			sys.exit()

		versionTag = ""
		thirdPartyLibrary = ""
		while versionTag == "" or not os.path.isdir("builds/" + versionTag + "/OpenSceneryX-" + versionTag):
			versionTag = functions.getInput("Enter the latest release version (e.g. 1.0.1): ", 10)
		while thirdPartyLibrary == "" or not os.path.isfile(thirdPartyLibrary.replace("\ ", " ")):
			thirdPartyLibrary = functions.getInput("Enter the path to the third party library: ", 10).strip()

		classes.Configuration.init(versionTag, "", 'n')

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Checking for missing virtual paths\n")

		osxPaths = []

		with open("builds/" + versionTag + "/OpenSceneryX-" + versionTag + "/library.txt", "r") as file:
			for line in file:
				if line.startswith("EXPORT_BACKUP "):
					parts = line.split(" ")
					osxPaths.append(parts[1])

		with open("builds/" + versionTag + "/OpenSceneryX-" + versionTag + "/partials/extend_forests.txt", "r") as file:
			for line in file:
				if line.startswith("EXPORT "):
					parts = line.split(" ")
					osxPaths.append(parts[1])

		with open(thirdPartyLibrary.replace("\ ", " ")) as file:
			for line in file:
				if line.startswith("EXPORT "):
					parts = line.split(" ")
					if parts[1] not in osxPaths:
						functions.displayMessage(parts[1] + "\n", "warning")

		functions.displayMessage("------------------------\n")
		functions.displayMessage("Complete\n")
		functions.displayMessage("========================\n")

		functions.osNotify("Third Party Library check completed")

	except classes.BuildError as e:
		exceptionMessage = e.value


finally:
	if (exceptionMessage != ""):
		print(exceptionMessage)

