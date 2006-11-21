#!/usr/local/bin/python

# functions.py
# Common functions
# Version: $Revision$

import os
import shutil
import re
import urllib
import classes


def handleObject(dirpath, filename, destinationRoot, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split("/", 2)

  print "Handling object: " + objectSourcePath
  
  # Set up paths and copy files
  if not os.path.isdir(os.path.join(destinationRoot, parts[2])): os.makedirs(os.path.join(destinationRoot, parts[2]))
  if not copySupportFiles(dirpath, destinationRoot, parts): return
  shutil.copyfile(objectSourcePath, os.path.join(destinationRoot, parts[2], filename))

  # Open the object
  file = open(objectSourcePath, "r")
  objectFileContents = file.readlines()
  file.close()

  # Define the regex patterns:
  texturePattern = re.compile("TEXTURE\s+(.*)")
  litTexturePattern = re.compile("TEXTURE_LIT\s+(.*)")

  for line in objectFileContents:
    result = texturePattern.match(line)
    if result:
      textureFile = os.path.join(dirpath, result.group(1))
      if os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(destinationRoot, parts[2], result.group(1)))
     
    result = litTexturePattern.match(line)
    if result:
      textureFile = os.path.join(dirpath, result.group(1))
      if os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(destinationRoot, parts[2], result.group(1)))

  # Handle the info.txt file
  virtualPaths = handleInfoFile(dirpath, destinationRoot, htmlIndexFileHandle, parts, ".obj")
  
  # Write to the library.txt file
  for virtualPath in virtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + os.path.join(parts[2], filename) + "\n")
    libraryPlaceholderFileHandle.write("EXPORT opensceneryx/" + virtualPath + " placeholder.obj\n")




def handleFacade(dirpath, filename, destinationRoot, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle):
  print "facades not handled yet: " + os.path.join(dirpath, filename)





def handleForest(dirpath, filename, destinationRoot, libraryFileHandle, libraryPlaceholderFileHandle, htmlIndexFileHandle):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split("/", 2)

  print "Handling forest: " + objectSourcePath
  
  # Set up paths and copy files
  if not os.path.isdir(os.path.join(destinationRoot, parts[2])): os.makedirs(os.path.join(destinationRoot, parts[2]))
  if not copySupportFiles(dirpath, destinationRoot, parts): return
  shutil.copyfile(objectSourcePath, os.path.join(destinationRoot, parts[2], filename))

  # Open the object
  file = open(objectSourcePath, "r")
  objectFileContents = file.readlines()
  file.close()

  # Define the regex patterns:
  texturePattern = re.compile("TEXTURE\s+(.*)")

  for line in objectFileContents:
    result = texturePattern.match(line)
    if result:
      textureFile = os.path.join(dirpath, result.group(1))
      if os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(destinationRoot, parts[2], result.group(1)))
        break

  # Handle the info.txt file
  virtualPaths = handleInfoFile(dirpath, destinationRoot, htmlIndexFileHandle, parts, ".for")
  
  # Write to the library.txt file
  for virtualPath in virtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + os.path.join(parts[2], filename) + "\n")
    libraryPlaceholderFileHandle.write("EXPORT opensceneryx/" + virtualPath + " placeholder.for\n")





def copySupportFiles(dirpath, destinationRoot, parts):
  if not os.path.isfile(os.path.join(dirpath, "info.txt")):
    print "  ERROR: No info.txt file found - object excluded"
    return 0
    
  if not os.path.isfile(os.path.join(dirpath, "screenshot.jpg")):
    print "  ERROR: No screenshot.jpg file found - object excluded"
    return 0

  shutil.copyfile(os.path.join(dirpath, "info.txt"), os.path.join(destinationRoot, parts[2], "info.txt"))
  shutil.copyfile(os.path.join(dirpath, "screenshot.jpg"), os.path.join(destinationRoot, parts[2], "screenshot.jpg"))

  return 1
  
  
  
  
  
def handleInfoFile(dirpath, destinationRoot, htmlIndexFileHandle, parts, suffix):
   # open the info file
  file = open(os.path.join(dirpath, "info.txt"))
  infoFileContents = file.readlines()
  file.close()
  
  # define the regex patterns:
  texturePattern = re.compile("TEXTURE\s+(.*)")
  litTexturePattern = re.compile("TEXTURE_LIT\s+(.*)")
  exportPattern = re.compile("Export:\s+(.*)")
  titlePattern = re.compile("Title:\s+(.*)")
  authorPattern = re.compile("Author:\s+(.*)")
  emailPattern = re.compile("Email:\s+(.*)")
  urlPattern = re.compile("URL:\s+(.*)")
  widthPattern = re.compile("Width:\s+(.*)")
  heightPattern = re.compile("Height:\s+(.*)")
  depthPattern = re.compile("Depth:\s+(.*)")
  descriptionPattern = re.compile("Description:\s+(.*)")

  # Define the variables to capture the data
  virtualPaths = [parts[2] + suffix]
  title = ""
  author = ""
  email = ""
  url = ""
  width = ""
  height = ""
  depth = ""
  description = ""
  
  for line in infoFileContents:
    result = titlePattern.match(line)
    if result:
      title = result.group(1)
      continue

    result = authorPattern.match(line)
    if result:
      author = result.group(1)
      continue
      
    result = emailPattern.match(line)
    if result:
      email = result.group(1)
      continue
      
    result = urlPattern.match(line)
    if result:
      url = result.group(1)
      continue
      
    result = widthPattern.match(line)
    if result:
      width = result.group(1)
      continue

    result = heightPattern.match(line)
    if result:
      height = result.group(1)
      continue

    result = depthPattern.match(line)
    if result:
      depth = result.group(1)
      continue

    result = descriptionPattern.match(line)
    if result:
      description = result.group(1)
      continue

    result = exportPattern.match(line)
    if result:
      virtualPaths.append(result.group(1) + suffix)
      print "  Additional virtual path added: " + result.group(1) + suffix
      continue

  htmlIndexFileHandle.write("<li><a href='doc/" + urllib.pathname2url(title) + ".html" + "'>" + title + "</a></li>")
  
  htmlFileHandle = open(destinationRoot + "/doc/" + title + ".html", "w")
  htmlFileHandle.write("<html><head><title>OpenSceneryX Object Library for X-Plane - " + title + "</title>\n")
  htmlFileHandle.write("<link rel='stylesheet' href='../doc/all.css' type='text/css'>\n")
  htmlFileHandle.write("<body>\n")
  htmlFileHandle.write("<div id='header'>\n")
  htmlFileHandle.write("<h1>OpenSceneryX Object Library for X-Plane</h1>\n")
  htmlFileHandle.write("<p id='version'>Version: " + classes.Configuration.versionNumber + " - " + classes.Configuration.versionDate + "</p>\n")
  htmlFileHandle.write("</div>\n")
  htmlFileHandle.write("<div id='content'>\n")
  htmlFileHandle.write("<h2>" + title + "</h2>\n")
  htmlFileHandle.write("<p class='virtualPath'>\n")
  for virtualPath in virtualPaths:
    htmlFileHandle.write(virtualPath + "<br />\n")
  htmlFileHandle.write("</p>\n")
  htmlFileHandle.write("<img class='screenshot' src='../" + os.path.join(parts[2], "screenshot.jpg") + "'>\n")
  htmlFileHandle.write("<ul class='mainItemDetails'>\n")
  if (not author == ""): htmlFileHandle.write("<li><span class='fieldTitle'>Author:</span> <span class='fieldValue'>" + author + "</span></li>\n")
  if (not email == ""): htmlFileHandle.write("<li><span class='fieldTitle'>Email:</span> <span class='fieldValue'><a href='mailto:" + email + "'>" + email + "</a></span></li>\n")
  if (not url == ""): htmlFileHandle.write("<li><span class='fieldTitle'>URL:</span> <span class='fieldValue'><a href='" + url + "'>" + url + "</a></span></li>\n")
  if (not description == ""): htmlFileHandle.write("<li><span class='fieldTitle'>Description:</span> <span class='fieldValue'>" + description + "</span></li>\n")
  
  if (not width == "" and not height == "" and not depth == ""):
    htmlFileHandle.write("<li><span class='fieldTitle'>Dimensions:</span>\n")
    htmlFileHandle.write("<ul class='dimensions'>\n")
    htmlFileHandle.write("<li id='width'><span class='fieldTitle'>w:</span> " + width + "</li>\n")
    htmlFileHandle.write("<li id='height'><span class='fieldTitle'>h:</span> " + height + "</li>\n")
    htmlFileHandle.write("<li id='depth'><span class='fieldTitle'>d:</span> " + depth + "</li>\n")
    htmlFileHandle.write("</ul>\n")
    htmlFileHandle.write("</li>\n")

  htmlFileHandle.write("</ul>\n")

  htmlFileHandle.write("</div>")

  file = open("trunk/support/_footer.html", "r")
  fileContents = file.read()
  file.close()
  htmlFileHandle.write(fileContents)

  htmlFileHandle.write("</body></html>")
  htmlFileHandle.close()
  
  return virtualPaths
