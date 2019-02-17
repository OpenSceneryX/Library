# -*- coding: utf-8 -*-
# Script to update a third party library that is integrated with OpenSceneryX, when
# the original author releases a new version of the library
# Copyright (c) 2019 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.

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
    import re

    exceptionMessage = ""
    showTraceback = 0

    try:
        functions.displayMessage("==========================\n")
        functions.displayMessage("Update Third Party Library\n")
        functions.displayMessage("==========================\n")

        libraryFilesPath = ".." + os.sep + "files"
        if not os.path.isdir(libraryFilesPath):
            raise classes.BuildError("Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library")

        versionTag = ""
        while versionTag == "":
            versionTag = functions.getInput("Enter the library version number (e.g. 1.0.1): ", 10)
        buildLibraryPath = ".." + os.sep + "builds" + os.sep + versionTag + os.sep + "OpenSceneryX-" + versionTag + os.sep + "library.txt"

        if not os.path.isfile(buildLibraryPath):
            raise classes.BuildError("Error: A library.txt file does not exist for that version")

        thirdPartyLibraryName = ""
        while thirdPartyLibraryName == "":
            thirdPartyLibraryName = functions.getInput("Enter the name of the third party library (e.g. DT_Library): ", 20)

        thirdPartyLibraryPath = ".." + os.sep + "contributions" + os.sep + thirdPartyLibraryName + os.sep + "library.txt"
        if not os.path.isfile(thirdPartyLibraryPath):
            raise classes.BuildError("Error: Cannot find " + thirdPartyLibraryName + "/library.txt in the contributions folder")

        classes.Configuration.init(versionTag, "", 'n')

        functions.displayMessage("------------------------\n")
        functions.displayMessage("Working\n")
        functions.displayMessage("BEWARE - TEXTURES MUST BE COPIED MANUALLY AND SHARED TEXTURE PATHS ARE NOT HANDLED (YET)\n", "error")

        file = open(buildLibraryPath)
        libraryFileContents = file.read()
        file.close()

        file = open(thirdPartyLibraryPath)
        thirdPartyLibraryFileContents = file.read()
        file.close()

        # Build a dict mapping the third party file path to the OpenSceneryX virtual library path
        pattern = r"^EXPORT_BACKUP\s+{}/(.*?)\s+(.*?)$".format(thirdPartyLibraryName)
        matches = re.findall(pattern, libraryFileContents, re.MULTILINE)
        osxLookupDict = {a:b for a,b in matches}

        # Build a list of all exports in the third party library
        pattern = r"^EXPORT\s+{}/(.*?)\s+(.*?)$".format(thirdPartyLibraryName)
        matches = re.findall(pattern, thirdPartyLibraryFileContents, re.MULTILINE)

        # Iterate every export in the third party library, looking for a matching OpenSceneryX export
        for match in matches:
            # TODO: Compare contents of new and old, ignoring texture lines, and only replace if they differ.
            #       Perhaps pay attention to texture filename, only ignore path.
            if match[1] in osxLookupDict:
                sourceFilePath = ".." + os.sep + "contributions" + os.sep + thirdPartyLibraryName + os.sep + match[1]
                destinationFilePath = libraryFilesPath + os.sep + osxLookupDict[match[1]]
                functions.displayMessage("Copying updated item {} to {}\n".format(match[1], osxLookupDict[match[1]]), "note")
                # TODO: Enable this line
                #shutil.copyfile(sourceFilePath, destinationFilePath)
            else:
                functions.displayMessage("New item in this version: {}\n".format(match[1]), "warning")


        functions.displayMessage("------------------------\n")
        functions.displayMessage("Complete\n")
        functions.displayMessage("========================\n")

    except classes.BuildError as e:
        exceptionMessage = e.value


finally:
    if (exceptionMessage != ""):
        print(exceptionMessage)

