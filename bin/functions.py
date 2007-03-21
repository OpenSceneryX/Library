#!/usr/local/bin/python

# functions.py
# Common functions
# Version: $Revision$

import os
import shutil
import re
import urllib
import classes


def handleObject(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, objects, authors):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split("/", 2)

  print "Handling object: " + objectSourcePath
  
  # Create an instance of the SceneryObject class
  sceneryObject = classes.SceneryObject(parts[2], filename)

  # Handle the info.txt file
  if handleInfoFile(dirpath, parts, ".obj", sceneryObject, authors):
    objects.append(sceneryObject)

    # Set up paths and copy files
    if not os.path.isdir(os.path.join(classes.Configuration.osxFolder, parts[2])): os.makedirs(os.path.join(classes.Configuration.osxFolder, parts[2]))
    if not copySupportFiles(dirpath, parts): return
    shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
  
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
          shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
       
      result = litTexturePattern.match(line)
      if result:
        textureFile = os.path.join(dirpath, result.group(1))
        if os.path.isfile(textureFile):
          shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
  
    # Write to the library.txt file
    for virtualPath in sceneryObject.virtualPaths:
      libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
      libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")
  



def handleFacade(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, facades, authors):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split("/", 2)

  print "Handling facade: " + objectSourcePath

  # Create an instance of the SceneryObject class
  sceneryObject = classes.SceneryObject(parts[2], filename)
  
  # Handle the info.txt file
  if handleInfoFile(dirpath, parts, ".fac", sceneryObject, authors):
    facades.append(sceneryObject)

    # Set up paths and copy files
    if not os.path.isdir(os.path.join(classes.Configuration.osxFolder, parts[2])): os.makedirs(os.path.join(classes.Configuration.osxFolder, parts[2]))
    if not copySupportFiles(dirpath, parts): return
    shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
  
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
          shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
          break
  
    # Write to the library.txt file
    for virtualPath in sceneryObject.virtualPaths:
      libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
      libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")





def handleForest(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, forests, authors):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split("/", 2)

  print "Handling forest: " + objectSourcePath
  
  # Create an instance of the SceneryObject class
  sceneryObject = classes.SceneryObject(parts[2], filename)

  # Handle the info.txt file
  if handleInfoFile(dirpath, parts, ".for", sceneryObject, authors):
    forests.append(sceneryObject)
  
    # Set up paths and copy files
    if not os.path.isdir(os.path.join(classes.Configuration.osxFolder, parts[2])): os.makedirs(os.path.join(classes.Configuration.osxFolder, parts[2]))
    if not copySupportFiles(dirpath, parts): return
    shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
  
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
          shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
          break
  
    # Write to the library.txt file
    for virtualPath in sceneryObject.virtualPaths:
      libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
      libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")





def copySupportFiles(dirpath, parts):
  if not os.path.isfile(os.path.join(dirpath, "info.txt")):
    print "  ERROR: No info.txt file found - object excluded"
    return 0
    
  if not os.path.isfile(os.path.join(dirpath, "screenshot.jpg")):
    print "  ERROR: No screenshot.jpg file found - object excluded"
    return 0

  shutil.copyfile(os.path.join(dirpath, "info.txt"), os.path.join(classes.Configuration.osxFolder, parts[2], "info.txt"))
  shutil.copyfile(os.path.join(dirpath, "screenshot.jpg"), os.path.join(classes.Configuration.osxFolder, parts[2], "screenshot.jpg"))
      
  return 1
  
  
  
  
  
def handleInfoFile(dirpath, parts, suffix, sceneryObject, authors):
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
  excludePattern = re.compile("Exclude:\s+(.*)")
  
  # Define the variables to capture the data
  sceneryObject.virtualPaths.append(parts[2] + suffix)
  
  for line in infoFileContents:
    result = excludePattern.match(line)
    if result:
      print "  EXCLUDED, reason: " + result.group(1)
      return 0
      
    result = titlePattern.match(line)
    if result:
      sceneryObject.title = result.group(1)
      continue

    result = authorPattern.match(line)
    if result:
      sceneryObject.author = result.group(1)
      if not sceneryObject.author in authors:
        authors.append(sceneryObject.author)
      continue
      
    result = emailPattern.match(line)
    if result:
      sceneryObject.email = result.group(1)
      continue
      
    result = urlPattern.match(line)
    if result:
      sceneryObject.url = result.group(1)
      continue
      
    result = widthPattern.match(line)
    if result:
      sceneryObject.width = result.group(1)
      continue

    result = heightPattern.match(line)
    if result:
      sceneryObject.height = result.group(1)
      continue

    result = depthPattern.match(line)
    if result:
      sceneryObject.depth = result.group(1)
      continue

    result = descriptionPattern.match(line)
    if result:
      sceneryObject.description = result.group(1)
      continue

    result = exportPattern.match(line)
    if result:
      sceneryObject.virtualPaths.append(result.group(1) + suffix)
      print "  Additional virtual path added: " + result.group(1) + suffix
      continue

  if os.path.isfile(os.path.join(dirpath, "tutorial.pdf")):
    sceneryObject.tutorial = 1
    shutil.copyfile(os.path.join(dirpath, "tutorial.pdf"), classes.Configuration.osxFolder + "/doc/" + sceneryObject.title + " Tutorial.pdf")
    
  htmlFileHandle = open(classes.Configuration.osxFolder + "/doc/" + sceneryObject.title + ".html", "w")
  writeHTMLHeader(htmlFileHandle, "", "OpenSceneryX Object Library for X-Plane")
  htmlFileHandle.write("<div id='content'>\n")
  htmlFileHandle.write("<h2>" + sceneryObject.title + "</h2>\n")
  htmlFileHandle.write("<p class='virtualPath'>\n")
  for virtualPath in sceneryObject.virtualPaths:
    htmlFileHandle.write(virtualPath + "<br />\n")
  htmlFileHandle.write("</p>\n")
  htmlFileHandle.write("<img class='screenshot' src='../" + os.path.join(parts[2], "screenshot.jpg") + "'>\n")
  htmlFileHandle.write("<ul class='mainItemDetails'>\n")
  if (not sceneryObject.author == ""):
    htmlFileHandle.write("<li><span class='fieldTitle'>Author:</span> <span class='fieldValue'>" + sceneryObject.author + "</span></li>\n")
  if (not sceneryObject.email == ""):
    htmlFileHandle.write("<li><span class='fieldTitle'>Email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.email + "'>" + sceneryObject.email + "</a></span></li>\n")
  if (not sceneryObject.url == ""):
    htmlFileHandle.write("<li><span class='fieldTitle'>URL:</span> <span class='fieldValue'><a href='" + sceneryObject.url + "'>" + sceneryObject.url + "</a></span></li>\n")
  if (not sceneryObject.description == ""):
    htmlFileHandle.write("<li><span class='fieldTitle'>Description:</span> <span class='fieldValue'>" + sceneryObject.description + "</span></li>\n")
  
  if (not sceneryObject.width == "" and not sceneryObject.height == "" and not sceneryObject.depth == ""):
    htmlFileHandle.write("<li><span class='fieldTitle'>Dimensions:</span>\n")
    htmlFileHandle.write("<ul class='dimensions'>\n")
    htmlFileHandle.write("<li id='width'><span class='fieldTitle'>w:</span> " + sceneryObject.width + "</li>\n")
    htmlFileHandle.write("<li id='height'><span class='fieldTitle'>h:</span> " + sceneryObject.height + "</li>\n")
    htmlFileHandle.write("<li id='depth'><span class='fieldTitle'>d:</span> " + sceneryObject.depth + "</li>\n")
    htmlFileHandle.write("</ul>\n")
    htmlFileHandle.write("</li>\n")

  if (sceneryObject.tutorial):
    htmlFileHandle.write("<li><span class='fieldTitle'>Tutorial:</span> <span class='fieldValue'><a href='" + urllib.pathname2url(sceneryObject.title + " Tutorial.pdf") + "' class='nounderline' title='View Tutorial' target='_blank'><img src='../doc/pdf.gif' class='icon' alt='PDF File Icon' /></a>&nbsp;<a href='" + urllib.pathname2url(sceneryObject.title + " Tutorial.pdf") + "' title='View Tutorial' target='_blank'>View Tutorial</a></span></li>\n")
    
  htmlFileHandle.write("</ul>\n")
  htmlFileHandle.write("</div>")

  writeHTMLFooter(htmlFileHandle, "")

  htmlFileHandle.close()
  
  return 1





def writeHTMLHeader(fileHandle, documentationPath, title):
  fileHandle.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"\n")
  fileHandle.write("          \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
  fileHandle.write("<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\"><head><title>OpenSceneryX Library for X-Plane</title>\n")
  fileHandle.write("<link rel='stylesheet' href='" + documentationPath + "all.css' type='text/css'/>\n")
  fileHandle.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>")
  fileHandle.write("</head>\n")
  fileHandle.write("<body>\n")
  fileHandle.write("<div id='header'>\n")
  fileHandle.write("<h1>" + title + "</h1>\n")
  fileHandle.write("<p id='version'><strong>Library Version:</strong> <a href='" + documentationPath + "ReleaseNotes.html'>" + classes.Configuration.versionNumber + "</a> - <strong>Built on: </strong>" + classes.Configuration.versionDate + "</p>\n")
  fileHandle.write("</div>\n")






def writeHTMLFooter(fileHandle, documentationPath):
  fileHandle.write("<div id='footer'>")
  fileHandle.write("<div style='float:left; margin-right:1em;'><a rel='license' class='nounderline' href='http://creativecommons.org/licenses/by-nc-nd/2.5/'><img alt='Creative Commons License' class='icon' src='" + documentationPath + "somerights20.png'/></a></div>")
  fileHandle.write("The OpenSceneryX library is licensed under a <a rel='license' href='http://creativecommons.org/licenses/by-nc-nd/2.5/'>Creative Commons Attribution-Noncommercial-No Derivative Works 2.5  License</a>. 'The Work' is defined as the library as a whole and by using the library you signify agreement to these terms. <strong>You must obtain the permission of the author(s) if you wish to distribute individual files from this library for any purpose</strong>, as this constitutes a derivative work under the licence.")
  fileHandle.write("<!-- <rdf:RDF xmlns='http://web.resource.org/cc/' xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>")
  fileHandle.write("<Work rdf:about=''>")
  fileHandle.write("<license rdf:resource='http://creativecommons.org/licenses/by-nc-nd/2.5/' />")
  fileHandle.write("<dc:type rdf:resource='http://purl.org/dc/dcmitype/InteractiveResource' />")
  fileHandle.write("</Work>")
  fileHandle.write("<License rdf:about='http://creativecommons.org/licenses/by-nc-nd/2.5/'>")
  fileHandle.write("<permits rdf:resource='http://web.resource.org/cc/Reproduction'/>")
  fileHandle.write("<permits rdf:resource='http://web.resource.org/cc/Distribution'/>")
  fileHandle.write("<requires rdf:resource='http://web.resource.org/cc/Notice'/>")
  fileHandle.write("<requires rdf:resource='http://web.resource.org/cc/Attribution'/>")
  fileHandle.write("<prohibits rdf:resource='http://web.resource.org/cc/CommercialUse'/>")
  fileHandle.write("</License></rdf:RDF> --></div>")
  fileHandle.write("</body></html>")






def writeLibraryHeader(fileHandle):
  fileHandle.write("A\n")
  fileHandle.write("800\n")
  fileHandle.write("LIBRARY\n")
