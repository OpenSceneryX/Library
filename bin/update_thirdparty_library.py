# -*- coding: utf-8 -*-
#
# Script to update a third party library that is integrated with OpenSceneryX, when the original author releases a new version
# of the library.
# The script looks for all EXPORT lines in the 3rd party library and finds a matching EXPORT_BACKUP in the latest build of OpenSceneryX.
# It then copies the new referenced file into the appropriate place. It alerts for any new library paths that are in the 3rd party
# library but don't currently exist in OpenSceneryX (which will need adding manually).
#
# Copyright (c) 2019 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
#
# If it's a Seasonal library, some additional manual steps are required:
#
# 1. Remove all except default region at the bottom of the library.txt file
# 2. Replace all EXPORT_EXCLUDE with EXPORT
# 3. If library is organised under subfolders (e.g. FlyAgi_Vegetation), need to search and replace 'Summer/' with ''
#    and move all content from the Summer/ folder up one level.
# 4. Select all and sort lines unique ascending
# 5. Run this script. Careful with this - where multiple items are published to the same path, it will always take the last so may
#    overwrite the correct item with a different one. If an items content changes significantly, check by manually copying in the
#    known correct item.
# 6. Run seasonalise.sh on appropriate paths - i.e. where the items are identical between seasons, apart from textures

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

        libraryFilesPath = f"..{os.sep}files"
        if not os.path.isdir(libraryFilesPath):
            raise classes.BuildError("Error: This script must be run from the 'bin' directory inside a full checkout of the scenery library")

        versionTag = ""
        while versionTag == "":
            versionTag = functions.getInput("Enter the latest OpenSceneryX built library version number (e.g. 1.0.1): ", 10)
        buildLibraryPath = f"..{os.sep}builds{os.sep}{versionTag}{os.sep}OpenSceneryX-{versionTag}{os.sep}library.txt"

        if not os.path.isfile(buildLibraryPath):
            raise classes.BuildError("Error: A library.txt file does not exist for that version")

        thirdPartyLibraryName = ""
        while thirdPartyLibraryName == "":
            thirdPartyLibraryName = functions.getInput("Enter the name of the third party library (e.g. DT_Library). This is used both to locate the folder and to identify library entries in library.txt: ", 20)

        thirdPartyLibraryPath = f"..{os.sep}contributions{os.sep}{thirdPartyLibraryName}{os.sep}library.txt"
        if not os.path.isfile(thirdPartyLibraryPath):
            raise classes.BuildError(f"Error: Cannot find {thirdPartyLibraryName}/library.txt in the contributions folder")

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

        # Build a dict mapping the third party virtual library path to the OpenSceneryX file path
        pattern = fr"^EXPORT_BACKUP\s+{thirdPartyLibraryName}/(.*?)\s+(.*?)$"
        matches = re.findall(pattern, libraryFileContents, re.MULTILINE)
        osxLookupDict = {a:b for a,b in matches}

        # Build a list of all exports in the third party library
        pattern = fr"^EXPORT\s+{thirdPartyLibraryName}/(.*?)\s+(.*?)$"
        matches = re.findall(pattern, thirdPartyLibraryFileContents, re.MULTILINE)

        # Iterate every export in the third party library, looking for a matching OpenSceneryX export
        for match in matches:
            if match[0] in osxLookupDict:
                sourceFilePath = f"..{os.sep}contributions{os.sep}{thirdPartyLibraryName}{os.sep}{match[1]}"
                destinationFilePath = f"{libraryFilesPath}{os.sep}{osxLookupDict[match[0]]}"
                functions.displayMessage(f"Copying updated item {match[1]} to {osxLookupDict[match[0]]}\n", "note")
                shutil.copyfile(sourceFilePath, destinationFilePath)
            else:
                functions.displayMessage(f"New item in this version: {match[1]}\n", "warning")


        functions.displayMessage("------------------------\n")
        functions.displayMessage("Complete\n")
        functions.displayMessage("========================\n")

    except classes.BuildError as e:
        exceptionMessage = e.value


finally:
    if (exceptionMessage != ""):
        print(exceptionMessage)

