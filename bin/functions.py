#!/usr/local/bin/python

# functions.py
# Common functions
# Version: $Revision$

import os
import shutil
import re
import urllib
import classes
import fnmatch
import pcrt


def buildCategoryLandingPages(sceneryCategory, depth):
  # Only build landing pages where depth >= 3
  if depth >= 3:
    # Build a landing page
    htmlFileContent = ""
    htmlFileContent += "<div id='content'>\n"
    htmlFileContent += "<h2>" + sceneryCategory.title + " Variants</h2>\n"
    
    for sceneryObject in sceneryCategory.getSceneryObjects(1):
      htmlFileContent += "<h3><a href='" + urllib.pathname2url(sceneryObject.title + ".html") + "'>" + sceneryObject.title + "</a></h3><a href='" + urllib.pathname2url(sceneryObject.title + ".html") + "' class='nounderline'>"
      if (sceneryObject.screenshotFilePath != ""):
        htmlFileContent += "<img src='../" + sceneryObject.filePathRoot + "/screenshot.jpg' />"
      else:
        htmlFileContent += "<img src='screenshot_missing.png' />"
      htmlFileContent += "</a>\n"
      
    htmlFileContent += "</div>\n"

    htmlFileHandle = open(classes.Configuration.osxFolder + os.sep + "doc" + os.sep + "c_" + sceneryCategory.title + ".html", "w")
    htmlFileHandle.write(getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", sceneryCategory.title + " Variants"))
    htmlFileHandle.write(htmlFileContent)
    htmlFileHandle.write(getHTMLFooter(""))
    htmlFileHandle.close()

    htmlFileHandle = open(classes.Configuration.osxWebsiteFolder + os.sep + "doc" + os.sep + "c_" + sceneryCategory.title + ".html", "w")
    htmlFileHandle.write(getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", sceneryCategory.title + " Variants"))
    htmlFileHandle.write(htmlFileContent)
    htmlFileHandle.write(getHTMLFooter(""))
    htmlFileHandle.close()

  # Recurse
  children = sceneryCategory.childSceneryCategories
  for childCategory in children:
    buildCategoryLandingPages(childCategory, depth + 1)
    
    

def handleFolder(dirPath, currentCategory, libraryFileHandle, libraryPlaceholderFileHandle, authors):
  contents = os.listdir(dirPath)
  
  # Handle category descriptor first, if present
  if "category.txt" in contents:
    currentCategory = handleCategory(dirPath, currentCategory)
  
  for item in contents:
    fullPath = os.path.join(dirPath, item)
    
    if (item == "object.obj"):
      handleObject(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors)
      continue
    elif (item == "facade.fac"):
      handleFacade(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors)
      continue
    elif (item == "forest.for"):
      handleForest(dirPath, item, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors)
      continue
    elif (item == "category.txt"):
      # Do nothing
      continue
    elif os.path.isdir(fullPath):
      if not item == ".svn":
        handleFolder(fullPath, currentCategory, libraryFileHandle, libraryPlaceholderFileHandle, authors)



def handleCategory(dirpath, currentCategory):
  # Create an instance of the SceneryCategory class
  sceneryCategory = classes.SceneryCategory(dirpath)
  currentCategory.addSceneryCategory(sceneryCategory)
  
  return sceneryCategory
  
  

def handleObject(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split(os.sep, 2)

  displayMessage("Handling object: " + objectSourcePath + "\n")
  
  # Create an instance of the SceneryObject class
  sceneryObject = classes.SceneryObject(parts[2], filename)

  # Locate and check whether the support files exist 
  if not checkSupportFiles(dirpath, sceneryObject): return
  
  # Handle the info.txt file
  if not handleInfoFile(dirpath, parts, ".obj", sceneryObject, authors): return
  
  # Set up paths and copy files
  if not copySupportFiles(dirpath, parts, sceneryObject): return

  # Copy the object file
  shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))

  # Open the object
  file = open(objectSourcePath, "rU")
  objectFileContents = file.readlines()
  file.close()

  # Define the regex patterns:
  v7TexturePattern = re.compile("([^\s]*)\s+// Texture")
  v8TexturePattern = re.compile("TEXTURE\s+(.*)")
  v8LitTexturePattern = re.compile("TEXTURE_LIT\s+(.*)")
  textureFound = 0
  
  for line in objectFileContents:
    result = v7TexturePattern.match(line)
    if result:
      textureFound = 1
      textureFile = os.path.join(dirpath, result.group(1) + ".png")
      litTextureFile = os.path.join(dirpath, result.group(1) + "LIT.png")
      if (result.group(1) == ""):
        displayMessage("Object (v7) specifies a blank texture - valid but may not be as intended\n", "warning")
      elif os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1) + ".png"))
        if os.path.isfile(litTextureFile):
          shutil.copyfile(litTextureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1) + "LIT.png"))
      else:
        displayMessage("Cannot find texture - object (v7) excluded (" + textureFile + ")\n", "error")
        return
      
      # Break loop as soon as we find a v7 texture, need look no further
      break

    result = v8TexturePattern.match(line)
    if result:
      textureFound = textureFound + 1
      textureFile = os.path.join(dirpath, result.group(1))
      if (result.group(1) == ""):
        displayMessage("Object (v8) specifies a blank texture - valid but may not be as intended\n", "warning")
      elif os.path.isfile(textureFile):
        destinationTexturePath = os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)[0:result.group(1).rfind("/")]) 
        if not os.path.isdir(destinationTexturePath): 
          # Create destination texture path if it doesn't already exist
          os.makedirs(destinationTexturePath)
        if not os.path.isfile(os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1))):
          # Copy texture if it doesn't already exist
          shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
      else:
        displayMessage("Cannot find texture - object (v8) excluded (" + textureFile + ")\n", "error")
        return
        
      # Break loop if we've found both v8 textures
      if textureFound == 2:
        break

    result = v8LitTexturePattern.match(line)
    if result:
      textureFound = textureFound + 1
      textureFile = os.path.join(dirpath, result.group(1))
      if os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
      else:
        displayMessage("Cannot find LIT texture - object (v8) excluded (" + textureFile + ")\n", "error")
        return

      # Break loop if we've found both v8 textures
      if textureFound == 2:
        break

  if textureFound == 0:
    displayMessage("No texture line in file - this error must be corrected\n", "error")
    return
    
  # Object is valid, add it to the current category
  currentCategory.addSceneryObject(sceneryObject)

  # Write to the library.txt file
  for virtualPath in sceneryObject.virtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
    libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")
  for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
    libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.obj\n")




def handleFacade(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split(os.sep, 2)

  displayMessage("Handling facade: " + objectSourcePath + "\n")

  # Create an instance of the SceneryObject class
  sceneryObject = classes.SceneryObject(parts[2], filename)
  
  # Locate and check whether the support files exist 
  if not checkSupportFiles(dirpath, sceneryObject): return
  
  # Handle the info.txt file
  if not handleInfoFile(dirpath, parts, ".fac", sceneryObject, authors): return
  
  # Set up paths and copy files
  if not copySupportFiles(dirpath, parts, sceneryObject): return

  # Copy the facade file
  shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))
  
  # Open the facade
  file = open(objectSourcePath, "rU")
  objectFileContents = file.readlines()
  file.close()

  # Define the regex patterns:
  v8TexturePattern = re.compile("TEXTURE\s+(.*)")
  textureFound = 0
  
  for line in objectFileContents:
    result = v8TexturePattern.match(line)
    if result:
      textureFound = 1
      textureFile = os.path.join(dirpath, result.group(1))
      if (result.group(1) == ""):
        displayMessage("Facade specifies a blank texture - valid but may not be as intended\n", "warning")
      elif os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
      else:
        displayMessage("Cannot find texture - facade excluded (" + textureFile + ")\n", "error")
        return

      # Break loop as soon as we find a texture, need look no further
      break

  if not textureFound:
    displayMessage("No texture line in file - this error must be corrected\n", "error")
    return
    
  # Facade is valid, append it to the current category
  currentCategory.addSceneryObject(sceneryObject)

  # Write to the library.txt file
  for virtualPath in sceneryObject.virtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
    libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")
  for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
    libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.fac\n")





def handleForest(dirpath, filename, libraryFileHandle, libraryPlaceholderFileHandle, currentCategory, authors):
  objectSourcePath = os.path.join(dirpath, filename)
  parts = dirpath.split(os.sep, 2)

  displayMessage("Handling forest: " + objectSourcePath + "\n")
  
  # Create an instance of the SceneryObject class
  sceneryObject = classes.SceneryObject(parts[2], filename)

  # Locate and check whether the support files exist 
  if not checkSupportFiles(dirpath, sceneryObject): return
  
  # Handle the info.txt file
  if not handleInfoFile(dirpath, parts, ".for", sceneryObject, authors): return
  
  # Set up paths and copy files
  if not copySupportFiles(dirpath, parts, sceneryObject): return

  # Copy the forest file
  shutil.copyfile(objectSourcePath, os.path.join(classes.Configuration.osxFolder, parts[2], filename))

  # Open the object
  file = open(objectSourcePath, "rU")
  objectFileContents = file.readlines()
  file.close()

  # Define the regex patterns:
  v8TexturePattern = re.compile("TEXTURE\s+(.*)")
  textureFound = 0
  
  for line in objectFileContents:
    result = v8TexturePattern.match(line)
    if result:
      textureFound = 1
      textureFile = os.path.join(dirpath, result.group(1))
      if (result.group(1) == ""):
        displayMessage("Forest specifies a blank texture - valid but may not be as intended\n")
      elif os.path.isfile(textureFile):
        shutil.copyfile(textureFile, os.path.join(classes.Configuration.osxFolder, parts[2], result.group(1)))
      else:
        displayMessage("Cannot find texture - forest excluded (" + textureFile + ")\n", "error")
        return

      # Break loop as soon as we find a texture, need look no further
      break

  if not textureFound:
    displayMessage("No texture line in file - this error must be corrected\n", "error")
    return
    
  # Forest is valid, append it to the current category
  currentCategory.addSceneryObject(sceneryObject)

  # Write to the library.txt file
  for virtualPath in sceneryObject.virtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
    libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")
  for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
    libraryFileHandle.write("EXPORT opensceneryx/" + virtualPath + " " + sceneryObject.getFilePath() + "\n")
    libraryPlaceholderFileHandle.write("EXPORT_BACKUP opensceneryx/" + virtualPath + " opensceneryx/placeholder.for\n")





def checkSupportFiles(dirpath, sceneryObject):
  # Locate the info file. If it isn't in the current directory, walk up the folder structure looking for one in all parent
  # folders
  dirPathParts = dirpath.split(os.sep)
  for i in range(len(dirPathParts), 0, -1):
    if os.path.isfile(os.path.join(os.sep.join(dirPathParts[0:i]), "info.txt")):
      sceneryObject.infoFilePath = os.path.join(os.sep.join(dirPathParts[0:i]), "info.txt")
      break

  if sceneryObject.infoFilePath == "":
    # displayMessage("No info.txt file found - object excluded", "error")
    displayMessage("No info.txt file found - object excluded\n", "error")
    return 0
    
  # Locate the screenshot file. If it isn't in the current directory, walk up the folder structure looking for one in all # parent folders
  for i in range(len(dirPathParts), 0, -1):
    if os.path.isfile(os.path.join(os.sep.join(dirPathParts[0:i]), "screenshot.jpg")):
      sceneryObject.screenshotFilePath = os.path.join(os.sep.join(dirPathParts[0:i]), "screenshot.jpg")
      break

  if sceneryObject.screenshotFilePath == "":
    displayMessage("No screenshot.jpg file found - using default\n", "note")
  
  return 1



  
def copySupportFiles(dirpath, parts, sceneryObject):
  if not os.path.isdir(os.path.join(classes.Configuration.osxFolder, parts[2])): 
    os.makedirs(os.path.join(classes.Configuration.osxFolder, parts[2]))
  if not os.path.isdir(os.path.join(classes.Configuration.osxWebsiteFolder, parts[2])): 
    os.makedirs(os.path.join(classes.Configuration.osxWebsiteFolder, parts[2]))

  shutil.copyfile(sceneryObject.infoFilePath, os.path.join(classes.Configuration.osxFolder, parts[2], "info.txt"))
  
  if (sceneryObject.screenshotFilePath != ""):
    shutil.copyfile(sceneryObject.screenshotFilePath, os.path.join(classes.Configuration.osxFolder, parts[2], "screenshot.jpg"))
    shutil.copyfile(sceneryObject.screenshotFilePath, os.path.join(classes.Configuration.osxWebsiteFolder, parts[2], "screenshot.jpg"))
  
  return 1
  
  
  
def handleInfoFile(dirpath, parts, suffix, sceneryObject, authors):
  file = open(sceneryObject.infoFilePath)
  infoFileContents = file.readlines()
  file.close()
  
  # define the regex patterns:
  exportPattern = re.compile("Export:\s+(.*)")
  titlePattern = re.compile("Title:\s+(.*)")
  shortTitlePattern = re.compile("Short Title:\s+(.*)")
  authorPattern = re.compile("Author:\s+(.*)")
  textureAuthorPattern = re.compile("Author, texture:\s+(.*)")
  conversionAuthorPattern = re.compile("Author, conversion:\s+(.*)")
  emailPattern = re.compile("Email:\s+(.*)")
  textureEmailPattern = re.compile("Email, texture:\s+(.*)")
  conversionEmailPattern = re.compile("Email, conversion:\s+(.*)")
  urlPattern = re.compile("URL:\s+(.*)")
  textureUrlPattern = re.compile("URL, texture:\s+(.*)")
  conversionUrlPattern = re.compile("URL, conversion:\s+(.*)")
  widthPattern = re.compile("Width:\s+(.*)")
  heightPattern = re.compile("Height:\s+(.*)")
  depthPattern = re.compile("Depth:\s+(.*)")
  descriptionPattern = re.compile("Description:\s+(.*)")
  excludePattern = re.compile("Exclude:\s+(.*)")
  animatedPattern = re.compile("Animated:\s+(.*)")
  exportPropagatePattern = re.compile("Export Propagate:\s+(.*)")
  exportDeprecatedPattern = re.compile("Export Deprecated v(.*):\s+(.*)")
  
  # Add the file path to the virtual paths
  sceneryObject.virtualPaths.append(parts[2] + suffix)
  
  for line in infoFileContents:
    result = excludePattern.match(line)
    if result:
      displayMessage("EXCLUDED, reason: " + result.group(1) + "\n", "note")
      return 0
      
    result = titlePattern.match(line)
    if result:
      sceneryObject.title = result.group(1).replace("\"", "'")
      if (sceneryObject.shortTitle == ""): sceneryObject.shortTitle = sceneryObject.title
      continue

    result = shortTitlePattern.match(line)
    if result:
      sceneryObject.shortTitle = result.group(1).replace("\"", "'")
      continue

    result = authorPattern.match(line)
    if result:
      sceneryObject.author = result.group(1)
      if not sceneryObject.author in authors:
        authors.append(sceneryObject.author)
      continue
      
    result = textureAuthorPattern.match(line)
    if result:
      sceneryObject.textureAuthor = result.group(1)
      if not sceneryObject.textureAuthor in authors:
        authors.append(sceneryObject.textureAuthor)
      continue
      
    result = conversionAuthorPattern.match(line)
    if result:
      sceneryObject.conversionAuthor = result.group(1)
      if not sceneryObject.conversionAuthor in authors:
        authors.append(sceneryObject.conversionAuthor)
      continue
      
    result = emailPattern.match(line)
    if result:
      sceneryObject.email = result.group(1)
      continue
      
    result = textureEmailPattern.match(line)
    if result:
      sceneryObject.textureEmail = result.group(1)
      continue
      
    result = conversionEmailPattern.match(line)
    if result:
      sceneryObject.conversionEmail = result.group(1)
      continue
      
    result = urlPattern.match(line)
    if result:
      sceneryObject.url = result.group(1)
      continue
      
    result = textureUrlPattern.match(line)
    if result:
      sceneryObject.textureUrl = result.group(1)
      continue
      
    result = conversionUrlPattern.match(line)
    if result:
      sceneryObject.conversionUrl = result.group(1)
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

    result = animatedPattern.match(line)
    if result:
      sceneryObject.animated = (result.group(1) == "True" or result.group(1) == "Yes")
      continue

    result = exportPattern.match(line)
    if result:
      sceneryObject.virtualPaths.append(result.group(1) + suffix)
      continue

    result = exportPropagatePattern.match(line)
    if result:
      # Work with the first virtual path only, this is the one generated from the file hierarchy
      virtualPathParts = sceneryObject.virtualPaths[0].split("/")
      sceneryObject.exportPropagate = int(result.group(1))
      # Only do anything if the value of exportPropagate is valid
      if sceneryObject.exportPropagate < len(virtualPathParts):
        # Iterate from the value of exportPropagate up to the length of the path, publishing the object to every parent between
        for i in range(sceneryObject.exportPropagate + 1, len(virtualPathParts)):
          sceneryObject.virtualPaths.append("/".join(virtualPathParts[0:i]) + suffix)
      continue

    result = exportDeprecatedPattern.match(line)
    if result:
      sceneryObject.deprecatedVirtualPaths.append([result.group(2) + suffix, result.group(1)])
      continue

    result = descriptionPattern.match(line)
    if result:
      sceneryObject.description = "<p>" + result.group(1) + "</p>"
      continue

    # Default is to append to the description
    sceneryObject.description += "<p>" + line + "</p>"
    
    
  if os.path.isfile(os.path.join(dirpath, "tutorial.pdf")):
    sceneryObject.tutorial = 1
    shutil.copyfile(os.path.join(dirpath, "tutorial.pdf"), classes.Configuration.osxFolder + os.sep + "doc" + os.sep + sceneryObject.title + " Tutorial.pdf")
    shutil.copyfile(os.path.join(dirpath, "tutorial.pdf"), classes.Configuration.osxWebsiteFolder + os.sep + "doc/" + os.sep + sceneryObject.title + " Tutorial.pdf")


  htmlFileContent = ""
  htmlFileContent += "<div id='content'>\n"
  htmlFileContent += "<h2>" + sceneryObject.title + "</h2>\n"
  htmlFileContent += "<div class='virtualPath'>\n"
  htmlFileContent += "<h3>Virtual Paths</h3>\n"
  for virtualPath in sceneryObject.virtualPaths:
    htmlFileContent += virtualPath + "<br />\n"
  htmlFileContent += "</div>\n"
  if (not sceneryObject.deprecatedVirtualPaths == []):
    htmlFileContent += "<div class='deprecatedVirtualPath'>\n"
    htmlFileContent += "<h3>Deprecated Paths</h3>\n"
    for (virtualPath, virtualPathVersion) in sceneryObject.deprecatedVirtualPaths:
      htmlFileContent += "<strong>From v" + virtualPathVersion + "</strong>: " + virtualPath + "<br />\n"
    htmlFileContent += "</div>\n"
  if (sceneryObject.screenshotFilePath != ""):
    htmlFileContent += "<img class='screenshot' src='../" + os.path.join(parts[2], "screenshot.jpg") + "'>\n"
  else:
    htmlFileContent += "<img class='screenshot' src='screenshot_missing.png'>\n"
  htmlFileContent += "<ul class='mainItemDetails'>\n"
  if (not sceneryObject.author == ""):
    htmlFileContent += "<li><span class='fieldTitle'>Original Author:</span> "
    if (not sceneryObject.url == ""):
      htmlFileContent += "<span class='fieldValue'><a href='" + sceneryObject.url + "' target='_blank'>" + sceneryObject.author + "</a></span>"
      if (not sceneryObject.email == ""):
        htmlFileContent += ", <span class='fieldTitle'>email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.email + "'>" + sceneryObject.email + "</a></span>"
    elif (not sceneryObject.email == ""):
      htmlFileContent += "<span class='fieldValue'><a href='mailto:" + sceneryObject.email + "'>" + sceneryObject.author + "</a></span>"
    else:
      htmlFileContent += "<span class='fieldValue'>" + sceneryObject.author + "</span>"

    htmlFileContent += "</li>\n"
    
  if (not sceneryObject.textureAuthor == ""):
    htmlFileContent += "<li><span class='fieldTitle'>Original Texture Author:</span> "
    if (not sceneryObject.textureUrl == ""):
      htmlFileContent += "<span class='fieldValue'><a href='" + sceneryObject.textureUrl + "' target='_blank'>" + sceneryObject.textureAuthor + "</a></span>"
      if (not sceneryObject.textureEmail == ""):
        htmlFileContent += ", <span class='fieldTitle'>email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.textureEmail + "'>" + sceneryObject.textureEmail + "</a></span>"
    elif (not sceneryObject.textureEmail == ""):
      htmlFileContent += "<span class='fieldValue'><a href='mailto:" + sceneryObject.textureEmail + "'>" + sceneryObject.textureAuthor + "</a></span>"
    else:
      htmlFileContent += "<span class='fieldValue'>" + sceneryObject.textureAuthor + "</span>"

    htmlFileContent += "</li>\n"
    
  if (not sceneryObject.conversionAuthor == ""):
    htmlFileContent += "<li><span class='fieldTitle'>Object Conversion By:</span> "
    if (not sceneryObject.conversionUrl == ""):
      htmlFileContent += "<span class='fieldValue'><a href='" + sceneryObject.conversionUrl + "' target='_blank'>" + sceneryObject.conversionAuthor + "</a></span>"
      if (not sceneryObject.conversionEmail == ""):
        htmlFileContent += ", <span class='fieldTitle'>email:</span> <span class='fieldValue'><a href='mailto:" + sceneryObject.conversionEmail + "'>" + sceneryObject.conversionEmail + "</a></span>"
    elif (not sceneryObject.conversionEmail == ""):
      htmlFileContent += "<span class='fieldValue'><a href='mailto:" + sceneryObject.conversionEmail + "'>" + sceneryObject.conversionAuthor + "</a></span>"
    else:
      htmlFileContent += "<span class='fieldValue'>" + sceneryObject.conversionAuthor + "</span>"

    htmlFileContent += "</li>\n"

  if (not sceneryObject.description == ""):
    htmlFileContent += "<li><span class='fieldTitle'>Description:</span> <span class='fieldValue'>" + sceneryObject.description + "</span></li>\n"
  
  if (not sceneryObject.width == "" and not sceneryObject.height == "" and not sceneryObject.depth == ""):
    htmlFileContent += "<li><span class='fieldTitle'>Dimensions:</span>\n"
    htmlFileContent += "<ul class='dimensions'>\n"
    htmlFileContent += "<li id='width'><span class='fieldTitle'>w:</span> " + sceneryObject.width + "</li>\n"
    htmlFileContent += "<li id='height'><span class='fieldTitle'>h:</span> " + sceneryObject.height + "</li>\n"
    htmlFileContent += "<li id='depth'><span class='fieldTitle'>d:</span> " + sceneryObject.depth + "</li>\n"
    htmlFileContent += "</ul>\n"
    htmlFileContent += "</li>\n"

  if (sceneryObject.tutorial):
    htmlFileContent += "<li><span class='fieldTitle'>Tutorial:</span> <span class='fieldValue'><a href='" + urllib.pathname2url(sceneryObject.title + " Tutorial.pdf") + "' class='nounderline' title='View Tutorial' target='_blank'><img src='../doc/pdf.gif' class='icon' alt='PDF File Icon' /></a>&nbsp;<a href='" + urllib.pathname2url(sceneryObject.title + " Tutorial.pdf") + "' title='View Tutorial' target='_blank'>View Tutorial</a></span></li>\n"
    
  htmlFileContent += "</ul>\n"
  htmlFileContent += "</div>"

  htmlFileHandle = open(classes.Configuration.osxFolder + os.sep + "doc" + os.sep + sceneryObject.title + ".html", "w")
  htmlFileHandle.write(getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", sceneryObject.title))
  htmlFileHandle.write(htmlFileContent)
  htmlFileHandle.write(getHTMLFooter(""))
  htmlFileHandle.close()
  
  htmlFileHandle = open(classes.Configuration.osxWebsiteFolder + os.sep + "doc" + os.sep + sceneryObject.title + ".html", "w")
  htmlFileHandle.write(getHTMLHeader("", "OpenSceneryX Object Library for X-Plane&reg;", sceneryObject.title))
  htmlFileHandle.write(htmlFileContent)
  htmlFileHandle.write(getHTMLFooter(""))
  htmlFileHandle.close()
  
  return 1





def getHTMLHeader(documentationPath, mainTitle, titleSuffix):
  result = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"\n"
  result += "          \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n"
  result += "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\"><head><title>" + mainTitle
  if titleSuffix != "":
    result += " - " + titleSuffix
  result += "</title>\n"
  result += "<link rel='stylesheet' href='" + documentationPath + "all.css' type='text/css'/>\n"
  result += "<link rel='stylesheet' href='" + documentationPath + "tabbo.css' type='text/css'/>\n"
  result += "<link rel='stylesheet' href='" + documentationPath + "collapso.css' type='text/css'/>\n"
  result += "<script type='text/javascript' src='" + documentationPath + "tabbo.js'></script>\n"
  result += "<script type='text/javascript' src='" + documentationPath + "collapso.js'></script>\n"
  result += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>"
  result += "</head>\n"
  result += "<body>\n"
  result += "<div id='header'>\n"
  result += "<h1>" + mainTitle + "</h1>\n"
  result += "<p id='version'><strong>Library Version:</strong> <a href='" + documentationPath + "ReleaseNotes.html'>" + classes.Configuration.versionNumber + "</a> - <strong>Built on: </strong>" + classes.Configuration.versionDate + "</p>\n"
  result += "</div>\n"
  return result





def getHTMLFooter(documentationPath):
  result = "<div id='footer'>"
  result += "<div style='float:left; margin-right:1em;'><a rel='license' class='nounderline' href='http://creativecommons.org/licenses/by-nc-nd/3.0/' target='_blank'><img alt='Creative Commons License' class='icon' src='" + documentationPath + "cc_logo.png'/></a></div>"
  result += "The OpenSceneryX library is licensed under a <a rel='license' href='http://creativecommons.org/licenses/by-nc-nd/3.0/' target='_blank'>Creative Commons Attribution-Noncommercial-No Derivative Works 3.0 License</a>. 'The Work' is defined as the library as a whole and by using the library you signify agreement to these terms. <strong>You must obtain the permission of the author(s) if you wish to distribute individual files from this library for any purpose</strong>, as this constitutes a derivative work under the licence."
  result += "</div>"
  result += "</body></html>"
  return result



def getHTMLTOC(rootCategory):
  result = "<div id='toc'>\n"
  result += "<h2>Contents</h2>\n"
  result += "<div class='tabber'>\n"
  
  for mainSceneryCategory in rootCategory.childSceneryCategories:
    result += "<div class='tabberTab'>\n"
    result += "<h3>" + mainSceneryCategory.title + "</h3>\n"
    
    if len(mainSceneryCategory.childSceneryCategories) > 0:
      for subSceneryCategory in mainSceneryCategory.childSceneryCategories:
        result += "<h4>" + subSceneryCategory.title + "</h4>\n"
        result += "<ul class='inline'>\n"
        
        if len(subSceneryCategory.childSceneryCategories) > 0:
          # We have another level of categorisation, show a category list where each link takes the user to a
          # landing page for that category
          for subsubSceneryCategory in subSceneryCategory.childSceneryCategories:
            result += "<li><a href='doc/c_" + subsubSceneryCategory.title + ".html'>" + subsubSceneryCategory.title + "</a>"
            result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/variations.gif'><span>Multiple variants available</span></a>"
            result += "</li>\n"
  
          # Also show the list of objects directly in this category
          sceneryObjects = subSceneryCategory.getSceneryObjects(0)
          result += getHTMLSceneryObjects(sceneryObjects)
          
        else:
          # No more category levels, show the list of objects
          sceneryObjects = subSceneryCategory.getSceneryObjects(1)
          result += getHTMLSceneryObjects(sceneryObjects)

        result += "</ul>\n"
        
    else:
      # No categorisation, show the list of objects
      result += "<ul class='inline'>\n"
      sceneryObjects = mainSceneryCategory.getSceneryObjects(1)
      result += getHTMLSceneryObjects(sceneryObjects)        
      result += "</ul>\n"

    result += "</div>\n"
    
  result += "</div>\n"
  result += "</div>\n"

  return result



def getHTMLSceneryObjects(sceneryObjects):
  result = ""
  for sceneryObject in sceneryObjects:
    result += "<li><a class='hoverimage' href='doc/" + urllib.pathname2url(sceneryObject.title + ".html") + "'>" + sceneryObject.shortTitle
    if (sceneryObject.screenshotFilePath != ""):
      result += "<span><img src='" + os.path.join(sceneryObject.filePathRoot, "screenshot.jpg") + "' /></span>"
    else:
      result += "<span><img src='doc/screenshot_missing.png' /></span>"
    result += "</a>"
   
    if (sceneryObject.tutorial):
      result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/tutorial.gif'><span>Tutorial available</span></a>"

    if (sceneryObject.animated):
      result += " <a class='tooltip' href='#'><img class='attributeicon' src='doc/animated.gif'><span>Animated</span></a>"

    result += "</li>\n"
    
  return result



def getLibraryHeader():
  result = "A\n"
  result += "800\n"
  result += "LIBRARY\n"
  return result



def matchesAny(name, tests):
  for test in tests:
    if fnmatch.fnmatch(name, test):
      return True
  return False



def caseinsensitive_sort(stringList):
  """case-insensitive string comparison sort
  usage: stringList = caseinsensitive_sort(stringList)"""
  tupleList = [(x.lower(), x) for x in stringList]
  tupleList.sort()
  stringList[:] = [x[1] for x in tupleList]



def displayMessage(message, type="message"):
  if (type == "error"):
    pcrt.fg(pcrt.RED)
    print "ERROR: " + message,
  elif (type == "warning"):
    pcrt.fg(pcrt.YELLOW)
    print "WARNING: " + message,
  elif (type == "note"):
    pcrt.fg(pcrt.CYAN)
    print "NOTE: " + message,
  elif (type == "message"):
    pcrt.fg(pcrt.WHITE)
    print message,



def getInput(message, maxSize):
  return raw_input(message)
