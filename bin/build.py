#!/usr/local/bin/python
# Script to build a library release
# Version: $Revision$

# Include common functions
import functions
import os
import sys
import shutil
import classes
import urllib


print "\n========================"
print "OpenSceneryX Release"
print "========================"

if not os.path.isdir("../files") or not os.path.isdir("../../tags"):
  print "Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library\n"
  sys.exit()

versionTag = ""
while versionTag == "":
  versionTag = raw_input("Enter the release tag (e.g. 1.0.1): ")

classes.Configuration.setVersionTag(versionTag)

os.chdir("../..")

update = raw_input("Do you want to update the 'files' directory from the repository before release? [y/N]: ")

if update == "Y" or update == "y":
  print "Would svn update trunk/files"
#   svn update trunk/files



print "------------------------"
print "Creating release paths"
# print "svn mkdir tags/" + classes.Configuration.versionNumber
classes.Configuration.makeFolders()
# status = os.system("svn mkdir tags/" + classes.Configuration.versionNumber)



print "------------------------"
print "Creating library.txt"
libraryFileHandle = open(classes.Configuration.osxFolder + "/library.txt", "w")
libraryPlaceholderFileHandle = open(classes.Configuration.osxPlaceholderFolder + "/library.txt", "w")
functions.writeLibraryHeader(libraryFileHandle)
functions.writeLibraryHeader(libraryPlaceholderFileHandle)



print "------------------------"
print "Creating HTML files"
htmlIndexFileHandle = open(classes.Configuration.osxFolder + "/ReadMe.html", "w")
functions.writeHTMLHeader(htmlIndexFileHandle, "doc/", "OpenSceneryX Object Library for X-Plane")
htmlReleaseNotesFileHandle = open(classes.Configuration.osxFolder + "/doc/ReleaseNotes.html", "w")
functions.writeHTMLHeader(htmlReleaseNotesFileHandle, "", "OpenSceneryX Object Library for X-Plane")
htmlDeveloperFileHandle = open(classes.Configuration.osxDeveloperPackFolder + "/ReadMe.html", "w")
functions.writeHTMLHeader(htmlDeveloperFileHandle, "doc/", "OpenSceneryX Developer Pack")
htmlWebIndexFileHandle = open(classes.Configuration.osxWebsiteFolder + "/index.html", "w")
functions.writeHTMLHeader(htmlWebIndexFileHandle, "doc/", "OpenSceneryX Object Library for X-Plane")
htmlWebReleaseNotesFileHandle = open(classes.Configuration.osxWebsiteFolder + "/doc/ReleaseNotes.html", "w")
functions.writeHTMLHeader(htmlWebReleaseNotesFileHandle, "", "OpenSceneryX Object Library for X-Plane")


print "------------------------"
print "Copying files"
shutil.copyfile("trunk/support/all.css", classes.Configuration.osxFolder + "/doc/all.css")
shutil.copyfile("trunk/support/cube.gif", classes.Configuration.osxFolder + "/doc/cube.gif")
shutil.copyfile("trunk/support/bullet_object.gif", classes.Configuration.osxFolder + "/doc/bullet_object.gif")
shutil.copyfile("trunk/support/somerights20.png", classes.Configuration.osxFolder + "/doc/somerights20.png")
shutil.copyfile("trunk/support/pdf.gif", classes.Configuration.osxFolder + "/doc/pdf.gif")
shutil.copyfile("trunk/support/tutorial.gif", classes.Configuration.osxFolder + "/doc/tutorial.gif")
shutil.copyfile("trunk/support/placeholder.obj", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.obj")
shutil.copyfile("trunk/support/placeholder.for", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.for")
shutil.copyfile("trunk/support/placeholder.fac", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.fac")

shutil.copyfile("trunk/support/all.css", classes.Configuration.osxDeveloperPackFolder + "/doc/all.css")
shutil.copyfile("trunk/support/somerights20.png", classes.Configuration.osxDeveloperPackFolder + "/doc/somerights20.png")
shutil.copyfile("trunk/support/requires_opensceneryx_logo.gif", classes.Configuration.osxPlaceholderFolder + "/requires_opensceneryx_logo.gif")

shutil.copyfile("trunk/support/all.css", classes.Configuration.osxWebsiteFolder + "/doc/all.css")
shutil.copyfile("trunk/support/cube.gif", classes.Configuration.osxWebsiteFolder + "/doc/cube.gif")
shutil.copyfile("trunk/support/bullet_object.gif", classes.Configuration.osxWebsiteFolder + "/doc/bullet_object.gif")
shutil.copyfile("trunk/support/somerights20.png", classes.Configuration.osxWebsiteFolder + "/doc/somerights20.png")
shutil.copyfile("trunk/support/pdf.gif", classes.Configuration.osxWebsiteFolder + "/doc/pdf.gif")
shutil.copyfile("trunk/support/tutorial.gif", classes.Configuration.osxWebsiteFolder + "/doc/tutorial.gif")
shutil.copyfile("trunk/support/favicon.ico", classes.Configuration.osxWebsiteFolder + "/favicon.ico")

authors = []
objects = []
facades = []
forests = []

for (dirpath, dirnames, filenames) in os.walk("trunk/files/objects"):
   for filename in filenames:
     if (filename == "object.obj"):
       functions.handleObject(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, objects, authors)
       
for (dirpath, dirnames, filenames) in os.walk("trunk/files/facades"):
   for filename in filenames:
     if (filename == "facade.fac"):
       functions.handleFacade(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, facades, authors)
       
for (dirpath, dirnames, filenames) in os.walk("trunk/files/forests"):
   for filename in filenames:
     if (filename == "forest.for"):
       functions.handleForest(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, forests, authors)

# authors.sort()
objects.sort()
facades.sort()
forests.sort()

functions.writeHTMLTOC(htmlIndexFileHandle, objects, facades, forests)
functions.writeHTMLTOC(htmlWebIndexFileHandle, objects, facades, forests)

authors = ", ".join(authors[:-1]) + " and " + authors[-1]

file = open("trunk/support/_index.html", "r")
fileContents = file.read()
fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
fileContents = fileContents.replace("${authors}", authors)
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
htmlWebReleaseNotesFileHandle.write(fileContents)

file = open("trunk/support/_webindex.html", "r")
fileContents = file.read()
fileContents = fileContents.replace("${version}", classes.Configuration.versionNumber)
fileContents = fileContents.replace("${authors}", authors)
file.close()
htmlWebIndexFileHandle.write(fileContents)


print "------------------------"
print "Finishing and closing files"
functions.writeHTMLFooter(htmlIndexFileHandle, "doc/")
functions.writeHTMLFooter(htmlDeveloperFileHandle, "doc/")
functions.writeHTMLFooter(htmlReleaseNotesFileHandle, "")
functions.writeHTMLFooter(htmlWebIndexFileHandle, "doc/")
htmlIndexFileHandle.close()
htmlDeveloperFileHandle.close()
libraryFileHandle.close()
libraryPlaceholderFileHandle.close()
htmlWebIndexFileHandle.close()


print "------------------------"
print "Complete"
print "========================"
print ""