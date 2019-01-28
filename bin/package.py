# -*- coding: utf-8 -*-
# Script to build a library release
# Copyright (c) 2007 Austin Goudge
# This script is free to use or modify, provided this copyright message remains at the top of the file.
# If this script is used to generate a scenery library other than OpenSceneryX, recognition MUST be given
# to the author in any documentation accompanying the library.
# Version: $Revision$

# Include common functions
import zipfile
import tarfile
import os
import classes
import sys

print("\n========================")
print("OpenSceneryX Packaging")
print("========================")

if not os.path.isdir("../files") or not os.path.isdir("../builds"):
  print("Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library\n")
  sys.exit()

versionTag = ""
while versionTag == "":
  versionTag = input("Enter the release tag (e.g. 1.0.1): ")

classes.Configuration.init(versionTag, "", False)

os.chdir("..")
os.chdir(classes.Configuration.releaseFolder)

tar = tarfile.TarFile('OpenSceneryX-' + classes.Configuration.versionNumber + ".tar", "w")

for (dirpath, dirnames, filenames) in os.walk("OpenSceneryX-" + classes.Configuration.versionNumber):
  for filename in filenames:
    path = os.path.join(dirpath, filename)
    zip = zipfile.ZipFile(path + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zip.write(path, filename)
    zip.close()
    tar.add(path + '.zip')
    os.remove(path)

tar.close()

print("------------------------")
print("Complete")
print("========================")
print("")