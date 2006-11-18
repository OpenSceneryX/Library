#!/usr/local/bin/python

# functions.py
# Common functions
# Version: $Revision $

import os
import shutil
import re
import urllib

def handleObject(dirpath, filename, destinationRoot, libraryFileHandle, htmlIndexFileHandle):
  objectSourcePath = os.path.join(dirpath, filename)
  print "handling object: " + objectSourcePath
  parts = dirpath.split("/", 2)
  
  if not os.path.isdir(os.path.join(destinationRoot, parts[2])):
    os.makedirs(os.path.join(destinationRoot, parts[2]))
    
  shutil.copyfile(objectSourcePath, os.path.join(destinationRoot, parts[2], filename))
  shutil.copyfile(os.path.join(dirpath, "info.txt"), os.path.join(destinationRoot, parts[2], "info.txt"))
  shutil.copyfile(os.path.join(dirpath, "screenshot.jpg"), os.path.join(destinationRoot, parts[2], "screenshot.jpg"))

  # open the object
  file = open(objectSourcePath, "r")
  objectFileContents = file.readlines()
  file.close()

  # open the info file
  file = open(os.path.join(dirpath, "info.txt"))
  infoFileContents = file.readlines()
  file.close()
  
  # define the regex patterns:
  texturePattern = re.compile("TEXTURE\s+(.*)")
  litTexturePattern = re.compile("TEXTURE_LIT\s+(.*)")
  exportOverridePattern = re.compile("Export:\s+(.*)")
  titlePattern = re.compile("Title:\s+(.*)")
  authorPattern = re.compile("Author:\s+(.*)")
  emailPattern = re.compile("Email:\s+(.*)")
  dimensionsPattern = re.compile("Dimensions:\s+(.*)")
  descriptionPattern = re.compile("Description:\s+(.*)")

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

  overrideVirtualPath = parts[2] + ".obj"
  title = ""
  author = ""
  email = ""
  dimensions = ""
  description = ""
  
  for line in infoFileContents:
    result = titlePattern.match(line)
    if result:
      title = result.group(1)

    result = authorPattern.match(line)
    if result:
      author = result.group(1)
      
    result = emailPattern.match(line)
    if result:
      email = result.group(1)

    result = dimensionsPattern.match(line)
    if result:
      dimensions = result.group(1)

    result = descriptionPattern.match(line)
    if result:
      description = result.group(1)

    result = exportOverridePattern.match(line)
    if result:
      overrideVirtualPath = os.path.join(dirpath, result.group(1)) + ".obj"
      print "  Virtual path overridden: " + overrideVirtualPath
      break

  libraryFileHandle.write("EXPORT openscenery/" + overrideVirtualPath + "\n")
  htmlIndexFileHandle.write("<li><a href='doc/" + urllib.pathname2url(title) + ".html" + "'>" + title + "</a></li>")
  
  htmlFileHandle = open(destinationRoot + "/doc/" + title + ".html", "w")
  htmlFileHandle.write("<html><head><title>OpenScenery Object Library for X-Plane - " + title + "</title>\n")
  htmlFileHandle.write("<link rel='stylesheet' href='../doc/all.css' type='text/css'>\n")
  htmlFileHandle.write("<body>\n")
  htmlFileHandle.write("<h1>OpenScenery Object Library for X-Plane</h1>\n")
  htmlFileHandle.write("<div id='content'>\n")

  htmlFileHandle.write("<h2>" + title + "</h2>\n")
  htmlFileHandle.write("<img src='../" + os.path.join(parts[2], "screenshot.jpg") + "'>")
  htmlFileHandle.write("<p><span class='fieldTitle'>Author:</span> <span class='fieldValue'>" + author + "</span></p>\n")
  htmlFileHandle.write("<p><span class='fieldTitle'>Email:</span> <span class='fieldValue'>" + email + "</span></p>\n")
  htmlFileHandle.write("<p><span class='fieldTitle'>Dimensions:</span> <span class='fieldValue'>" + dimensions + "</span></p>\n")
  htmlFileHandle.write("<p><span class='fieldTitle'>Description:</span> <span class='fieldValue'>" + description + "</span></p>\n")
  htmlFileHandle.write("<p><span class='fieldTitle'>File Path:</span> <span class='fieldValue'>" + objectSourcePath + "</span></p>\n")
  htmlFileHandle.write("<p><span class='fieldTitle'>Virtual Path:</span> <span class='fieldValue'>" + overrideVirtualPath + "</span></p>\n")

  htmlFileHandle.write("</div></body></html>")
  htmlFileHandle.close()


def handleFacade(dirpath, filename, destinationRoot, libraryFileHandle, htmlIndexFileHandle):
  print "facades not handled yet: " + os.path.join(dirpath, filename)





def handleForest(dirpath, filename, destinationRoot, libraryFileHandle, htmlIndexFileHandle):
  print "forests not handled yet: " + os.path.join(dirpath, filename)
