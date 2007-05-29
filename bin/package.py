#!/usr/local/bin/python
# Script to build a library release
# Version: $Revision$

# Include common functions
import zipfile
import tarfile
import os
import classes


print "\n========================"
print "OpenSceneryX Packaging"
print "========================"

if not os.path.isdir("../files") or not os.path.isdir("../../tags"):
  print "Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library\n"
  sys.exit()

versionTag = ""
while versionTag == "":
  versionTag = raw_input("Enter the release tag (e.g. 1.0.1): ")

classes.Configuration.setVersionTag(versionTag)

os.chdir("../..")
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

tar = tarfile.TarFile('OpenSceneryX-Website-' + classes.Configuration.versionNumber + ".tar", "w")

for (dirpath, dirnames, filenames) in os.walk("OpenSceneryX-Website-" + classes.Configuration.versionNumber):
  for filename in filenames:
    path = os.path.join(dirpath, filename)
    tar.add(path)
    
tar.close()

print "------------------------"
print "Complete"
print "========================"
print ""