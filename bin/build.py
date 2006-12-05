#!/usr/local/bin/python
# Script to build a library release
# Version: $Revision$

# Include common functions
import functions
import os
import sys
import shutil
import classes


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

update = raw_input("Do you want to update the 'files' directory from the repository before release? [Y/n]: ")

if update == "" or update == "Y" or update == "y":
  print "Would svn update trunk/files"
#   svn update trunk/files



print "------------------------"
print "Creating release paths"
print "svn mkdir tags/" + classes.Configuration.versionNumber

if not os.path.isdir("tags/" + classes.Configuration.versionNumber):
  os.mkdir("tags/" + classes.Configuration.versionNumber)
if not os.path.isdir(classes.Configuration.osxFolder):
  os.mkdir(classes.Configuration.osxFolder)
if not os.path.isdir(classes.Configuration.osxFolder + "/doc"):
  os.mkdir(classes.Configuration.osxFolder + "/doc")
if not os.path.isdir(classes.Configuration.osxPlaceholderFolder):
  os.mkdir(classes.Configuration.osxPlaceholderFolder)
if not os.path.isdir(classes.Configuration.osxPlaceholderFolder + "/opensceneryx"):
  os.mkdir(classes.Configuration.osxPlaceholderFolder + "/opensceneryx")

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
functions.writeHTMLHeader(htmlIndexFileHandle, "doc/")
htmlDeveloperFileHandle = open(classes.Configuration.osxFolder + "/doc/DeveloperInstructions.html", "w")
functions.writeHTMLHeader(htmlDeveloperFileHandle, "")


print "------------------------"
print "Copying files"
htmlIndexFileHandle.write("<div id='toc'>\n")
htmlIndexFileHandle.write("<h2>Index</h2>\n")

shutil.copyfile("trunk/support/all.css", classes.Configuration.osxFolder + "/doc/all.css")
shutil.copyfile("trunk/support/cube.gif", classes.Configuration.osxFolder + "/doc/cube.gif")
shutil.copyfile("trunk/support/bullet_object.gif", classes.Configuration.osxFolder + "/doc/bullet_object.gif")
shutil.copyfile("trunk/support/somerights20.png", classes.Configuration.osxFolder + "/doc/somerights20.png")
shutil.copyfile("trunk/support/pdf.gif", classes.Configuration.osxFolder + "/doc/pdf.gif")
shutil.copyfile("trunk/support/placeholder.obj", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.obj")
shutil.copyfile("trunk/support/placeholder.for", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.for")
shutil.copyfile("trunk/support/placeholder.fac", classes.Configuration.osxPlaceholderFolder + "/opensceneryx/placeholder.fac")

htmlIndexFileHandle.write("<h3>Objects</h3>\n")
htmlIndexFileHandle.write("<ul class='objects'>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/objects"):
   for filename in filenames:
     if (filename == "object.obj"):
       functions.handleObject(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")
       
htmlIndexFileHandle.write("<h3>Facades</h3>\n")
#htmlIndexFileHandle.write("<ul class='facades'>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/facades"):
   for filename in filenames:
     if (filename == "facade.fac"):
       functions.handleFacade(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle)
#htmlIndexFileHandle.write("</ul>\n")
       
htmlIndexFileHandle.write("<h3>Forests</h3>\n")
htmlIndexFileHandle.write("<ul class='forests'>\n")
for (dirpath, dirnames, filenames) in os.walk("trunk/files/forests"):
   for filename in filenames:
     if (filename == "forest.for"):
       functions.handleForest(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle)
htmlIndexFileHandle.write("</ul>\n")
htmlIndexFileHandle.write("</div>\n")


htmlIndexFileHandle.write("<div id='content'>\n")
htmlIndexFileHandle.write("<p>The OpenSceneryX project is a library of scenery objects for <a class='tooltip' href='#'>X-Plane v8.50 and above<span>Note that the Placeholder Library requires <strong>X-Plane v8.60</strong>, see the X-Plane Scenery Developers section for more details</span></a>.  It is a collaborative effort by members of the <a href='http://www.x-plane.org'>X-Plane.org</a> community and the aim is to provide a good range of scenery components for authors to use in their scenery packages.</p>\n")


htmlIndexFileHandle.write("<h2>Installation</h2>\n")
htmlIndexFileHandle.write("<p>If you're reading this you have already completed the first step by unzipping the package. You will have a folder titled <tt>OpenSceneryX-" + classes.Configuration.versionNumber + "</tt> in which you found this ReadMe file.  Now do the following:</p>\n")
htmlIndexFileHandle.write("<ol><li>Locate your X-Plane folder on your hard disk.  In Windows, this is likely to be <tt>C:\Program Files\X-Plane</tt> or <tt>C:\Program Files\X-System</tt> or similar. On the Mac, it is likely to be <tt>X-Plane</tt> or <tt>X-System</tt> in your <tt>Applications</tt> folder. Note that the X-Plane folder may have the version appended (e.g. <tt>X-Plane 8.50</tt>).</li>\n")
htmlIndexFileHandle.write("<li>Open the <tt>Custom Scenery</tt> folder inside your <tt>X-Plane</tt> folder.</li>\n")
htmlIndexFileHandle.write("<li>Copy the <tt>OpenSceneryX-" + classes.Configuration.versionNumber + "</tt> folder into the <tt>Custom Scenery</tt> folder.</li>\n")
htmlIndexFileHandle.write("<li>If you have installed OpenSceneryX before, please delete the old folder - It is definitely not advisable to keep more than one version of OpenSceneryX installed.</li>\n")
htmlIndexFileHandle.write("</ol>\n")

htmlIndexFileHandle.write("<h2>Use</h2>\n")
htmlIndexFileHandle.write("<h3>Normal X-Plane Users</h3>\n")
htmlIndexFileHandle.write("<p>If you are a standard user of X-Plane, then you don't do anything else. Installing this library does nothing <strong>on it's own</strong> to the simulator - you won't see new objects dotted about, you won't see any changes to your default scenery, you won't see any new options in X-Plane.  However, scenery packages developed by other people can now use the objects in this library, so if you have installed any scenery package marked 'Requires OpenSceneryX' then that package will come alive with objects.</p>\n")
htmlIndexFileHandle.write("<h3>X-Plane Scenery Developers</h3>\n")
htmlIndexFileHandle.write("<p>If you are a scenery developer, see <a href='doc/DeveloperInstructions.html'>this page for instructions on how to reference the library in your work</a>.</p>\n")

htmlIndexFileHandle.write("<h2>Contributors</h2>\n")
htmlIndexFileHandle.write("<p>Thank you to everyone who has contributed so far!  If you would like to contribute some of your own objects to the library, visit <a href='http://svn.x-plugins.com/xplane/wiki/Scenery/Library'>the project pages</a> or <a href='http://forums.x-plane.org/index.php?showuser=2431'>contact me at the .org</a></p>\n")
htmlIndexFileHandle.write("</div>\n")


file = open("trunk/support/_developerinstructions.html", "r")
fileContents = file.read()
file.close()
htmlDeveloperFileHandle.write(fileContents)




print "------------------------"
print "Finishing and closing files"
functions.writeHTMLFooter(htmlIndexFileHandle, "doc/")
functions.writeHTMLFooter(htmlDeveloperFileHandle, "")
htmlIndexFileHandle.close()
htmlDeveloperFileHandle.close()
libraryFileHandle.close()
libraryPlaceholderFileHandle.close()



print "------------------------"
print "Complete"
print "========================"
print ""