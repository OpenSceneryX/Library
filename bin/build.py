#!/usr/local/bin/python
# Script to build a library release
# Version: $Revision$

# Include common functions
import functions
import os
import sys
import shutil

version = ""

print "\n========================"
print "OpenScenery Release"
print "========================"

if not os.path.isdir("../files") or not os.path.isdir("../../tags"):
  print "Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library\n"
  sys.exit()

while version == "":
  version = raw_input("Enter the release number (e.g. 1-0-1): ")

os.chdir("../..")


update = raw_input("Do you want to update the 'files' directory from the repository before release? [Y/n]: ")

if update == "" or update == "Y" or update == "y":
  print "Would svn update trunk/files"
#   svn update trunk/files

print "------------------------"
print "Creating release tag"
print "svn mkdir tags/" + version

if not os.path.isdir("tags/" + version):
  os.mkdir("tags/" + version)
if not os.path.isdir("tags/" + version + "/doc"):
  os.mkdir("tags/" + version + "/doc")

# status = os.system("svn mkdir tags/" + version)

print "------------------------"
print "Creating library.txt"
libraryFileHandle = open("tags/" + version + "/library.txt", "w")
libraryFileHandle.write("A\n")
libraryFileHandle.write("800\n")
libraryFileHandle.write("LIBRARY\n")
 
print "------------------------"
print "Creating index.html"
htmlIndexFileHandle = open("tags/" + version + "/index.html", "w")
htmlIndexFileHandle.write("<html><head><title>OpenScenery Library for X-Plane</title>\n")
htmlIndexFileHandle.write("<link rel='stylesheet' href='doc/all.css' type='text/css'>\n")
htmlIndexFileHandle.write("<body>\n")
htmlIndexFileHandle.write("<h1>OpenScenery Object Library for X-Plane</h1>\n")
htmlIndexFileHandle.write("<div id='content'>\n")
htmlIndexFileHandle.write("<p>The OpenScenery project is a collaborative effort by members of the <a href='http://www.x-plane.org'>X-Plane.org</a> community.  The aim is to provide a good range of scenery components as a library for use in scenery packages.</p>\n")
htmlIndexFileHandle.write("<p>Thank you to everyone who has contributed so far!  If you would like to contribute some of your own objects to the library, visit <a href='http://svn.x-plugins.com/xplane/wiki/Scenery/Library'>the project pages</a> or <a href='http://forums.x-plane.org/index.php?showuser=2431'>contact me at the .org</a></p>\n")

print "------------------------"
print "Copying files"
shutil.copyfile("trunk/support/all.css", "tags/" + version + "/doc/all.css")
shutil.copyfile("trunk/support/cube.gif", "tags/" + version + "/doc/cube.gif")

htmlIndexFileHandle.write("<h2>Objects</h2>\n")
htmlIndexFileHandle.write("<ul>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/objects"):
   for filename in filenames:
     if (filename == "object.obj"):
       functions.handleObject(dirpath, filename, "tags/" + version, libraryFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")
       
htmlIndexFileHandle.write("<h2>Facades</h2>\n")
htmlIndexFileHandle.write("<ul>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/facades"):
   for filename in filenames:
     if (filename == "facade.fac"):
       functions.handleFacade(dirpath, filename, "tags/" + version, libraryFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")
       
htmlIndexFileHandle.write("<h2>Forests</h2>\n")
htmlIndexFileHandle.write("<ul>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/forests"):
   for filename in filenames:
     if (filename == "forest.for"):
       functions.handleForest(dirpath, filename, "tags/" + version, libraryFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")

print "------------------------"
print "Finishing and closing files"
htmlIndexFileHandle.write("</div>\n")
file = open("trunk/support/_footer.html", "r")
fileContents = file.read()
file.close()
htmlIndexFileHandle.write(fileContents)
htmlIndexFileHandle.write("</body></html>")
htmlIndexFileHandle.close()
libraryFileHandle.close()

print "------------------------"
print "Complete"
print "========================"
print ""