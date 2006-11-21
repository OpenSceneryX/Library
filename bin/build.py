#!/usr/local/bin/python
# Script to build a library release
# Version: $Revision$

# Include common functions
import functions
import os
import sys
import shutil
import classes
import datetime

classes.Configuration.versionNumber = ""
classes.Configuration.versionDate = datetime.datetime.now().strftime("%c")

print "\n========================"
print "OpenSceneryX Release"
print "========================"

if not os.path.isdir("../files") or not os.path.isdir("../../tags"):
  print "Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library\n"
  sys.exit()

while classes.Configuration.versionNumber == "":
  classes.Configuration.versionNumber = raw_input("Enter the release number (e.g. 1-0-1): ")

os.chdir("../..")
osxFolder = "tags/" + classes.Configuration.versionNumber + "/OpenSceneryX-" + classes.Configuration.versionNumber
osxPlaceholderFolder = "tags/" + classes.Configuration.versionNumber + "/OpenSceneryX-Placeholder-" + classes.Configuration.versionNumber

update = raw_input("Do you want to update the 'files' directory from the repository before release? [Y/n]: ")

if update == "" or update == "Y" or update == "y":
  print "Would svn update trunk/files"
#   svn update trunk/files

print "------------------------"
print "Creating release paths"
print "svn mkdir tags/" + classes.Configuration.versionNumber

if not os.path.isdir("tags/" + classes.Configuration.versionNumber):
  os.mkdir("tags/" + classes.Configuration.versionNumber)
if not os.path.isdir(osxFolder):
  os.mkdir(osxFolder)
if not os.path.isdir(osxFolder + "/doc"):
  os.mkdir(osxFolder + "/doc")
if not os.path.isdir(osxPlaceholderFolder):
  os.mkdir(osxPlaceholderFolder)

# status = os.system("svn mkdir tags/" + classes.Configuration.versionNumber)

print "------------------------"
print "Creating library.txt"
libraryFileHandle = open(osxFolder + "/library.txt", "w")
libraryFileHandle.write("A\n")
libraryFileHandle.write("800\n")
libraryFileHandle.write("LIBRARY\n")
libraryPlaceholderFileHandle = open(osxPlaceholderFolder + "/library.txt", "w")
libraryPlaceholderFileHandle.write("A\n")
libraryPlaceholderFileHandle.write("800\n")
libraryPlaceholderFileHandle.write("LIBRARY\n")
 
print "------------------------"
print "Creating index.html"
htmlIndexFileHandle = open(osxFolder + "/ReadMe.html", "w")
htmlIndexFileHandle.write("<html><head><title>OpenSceneryX Library for X-Plane</title>\n")
htmlIndexFileHandle.write("<link rel='stylesheet' href='doc/all.css' type='text/css'>\n")
htmlIndexFileHandle.write("<body>\n")
htmlIndexFileHandle.write("<div id='header'>\n")
htmlIndexFileHandle.write("<h1>OpenSceneryX Object Library for X-Plane</h1>\n")
htmlIndexFileHandle.write("<p id='version'><strong>Version:</strong> " + classes.Configuration.versionNumber + " <strong>Created:</strong> " + classes.Configuration.versionDate + "</p>\n")
htmlIndexFileHandle.write("</div>\n")
htmlIndexFileHandle.write("<div id='content'>\n")
htmlIndexFileHandle.write("<p>The OpenSceneryX project is a collaborative effort by members of the <a href='http://www.x-plane.org'>X-Plane.org</a> community.  The aim is to provide a good range of scenery components as a library for use in scenery packages.</p>\n")

htmlIndexFileHandle.write("<h2>Installation</h2>\n")
htmlIndexFileHandle.write("<p>If you're reading this you have already completed the first step by unzipping the package. You will have a folder titled <tt>OpenSceneryX-" + classes.Configuration.versionNumber + "</tt> in which you found this ReadMe file.  Now do the following:\n")
htmlIndexFileHandle.write("<ol><li>Locate your X-Plane folder on your hard disk.  In Windows, this is likely to be <tt>C:\Program Files\X-Plane</tt> or <tt>C:\Program Files\X-System</tt> or similar. On the Mac, it is likely to be <tt>X-Plane</tt> or <tt>X-System</tt> in your <tt>Applications</tt> folder. Note that the X-Plane folder may have the version appended (e.g. <tt>X-Plane 8.50</tt>).</li>\n")
htmlIndexFileHandle.write("<li>Open the <tt>Custom Scenery</tt> folder inside your <tt>X-Plane</tt> folder.</li>\n")
htmlIndexFileHandle.write("<li>Copy the <tt>OpenSceneryX-" + classes.Configuration.versionNumber + "</tt> folder into the <tt>Custom Scenery</tt> folder.</li>\n")
htmlIndexFileHandle.write("</ol></p>\n")

htmlIndexFileHandle.write("<h2>Contributors</h2>\n")
htmlIndexFileHandle.write("<p>Thank you to everyone who has contributed so far!  If you would like to contribute some of your own objects to the library, visit <a href='http://svn.x-plugins.com/xplane/wiki/Scenery/Library'>the project pages</a> or <a href='http://forums.x-plane.org/index.php?showuser=2431'>contact me at the .org</a></p>\n")

htmlIndexFileHandle.write("<h2>Contents</h2>\n")

print "------------------------"
print "Copying files"
shutil.copyfile("trunk/support/all.css", osxFolder + "/doc/all.css")
shutil.copyfile("trunk/support/cube.gif", osxFolder + "/doc/cube.gif")
shutil.copyfile("trunk/support/placeholder.obj", osxPlaceholderFolder + "/placeholder.obj")
shutil.copyfile("trunk/support/placeholder.for", osxPlaceholderFolder + "/placeholder.for")
shutil.copyfile("trunk/support/placeholder.fac", osxPlaceholderFolder + "/placeholder.fac")

htmlIndexFileHandle.write("<h3>Objects</h3>\n")
htmlIndexFileHandle.write("<ul>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/objects"):
   for filename in filenames:
     if (filename == "object.obj"):
       functions.handleObject(dirpath, filename, osxFolder, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")
       
htmlIndexFileHandle.write("<h3>Facades</h3>\n")
htmlIndexFileHandle.write("<ul>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/facades"):
   for filename in filenames:
     if (filename == "facade.fac"):
       functions.handleFacade(dirpath, filename, osxFolder, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")
       
htmlIndexFileHandle.write("<h3>Forests</h3>\n")
htmlIndexFileHandle.write("<ul>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/forests"):
   for filename in filenames:
     if (filename == "forest.for"):
       functions.handleForest(dirpath, filename, osxFolder, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle)
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
libraryPlaceholderFileHandle.close()

print "------------------------"
print "Complete"
print "========================"
print ""