#!/usr/local/bin/python

# classes.py
# Classes
# Version: $Revision$

import datetime
import string
import os

#
# Class to hold configuration values
#
class Configuration:
  "Generic container for shared variables."
  versionTag = ""
  versionNumber = ""
  versionDate = datetime.datetime.now().strftime("%c")
  
  def setVersionTag(self, versionTag):
    self.versionTag = versionTag
    self.versionNumber = string.replace(self.versionTag, "-", ".")
    self.releaseFolder = "tags/" + self.versionNumber
    self.osxFolder = self.releaseFolder + "/OpenSceneryX-" + self.versionNumber
    self.osxDeveloperPackFolder = self.releaseFolder + "/OpenSceneryX-DeveloperPack-" + self.versionNumber
    self.osxPlaceholderFolder = self.osxDeveloperPackFolder + "/OpenSceneryX-Placeholder-" + self.versionNumber
    self.osxWebsiteFolder = self.releaseFolder + "/OpenSceneryX-Website-" + self.versionNumber

  def makeFolders(self):
    if not os.path.isdir(self.releaseFolder):
      os.mkdir(self.releaseFolder)
    if not os.path.isdir(self.osxFolder):
      os.mkdir(self.osxFolder)
    if not os.path.isdir(self.osxFolder + "/doc"):
      os.mkdir(self.osxFolder + "/doc")
    if not os.path.isdir(self.osxDeveloperPackFolder):
      os.mkdir(self.osxDeveloperPackFolder)
    if not os.path.isdir(self.osxDeveloperPackFolder + "/doc"):
      os.mkdir(self.osxDeveloperPackFolder + "/doc")
    if not os.path.isdir(self.osxPlaceholderFolder):
      os.mkdir(self.osxPlaceholderFolder)
    if not os.path.isdir(self.osxPlaceholderFolder + "/opensceneryx"):
      os.mkdir(self.osxPlaceholderFolder + "/opensceneryx")
    if not os.path.isdir(self.osxWebsiteFolder):
      os.mkdir(self.osxWebsiteFolder)
    if not os.path.isdir(self.osxWebsiteFolder + "/doc"):
      os.mkdir(self.osxWebsiteFolder + "/doc")

  setVersionTag = classmethod(setVersionTag)
  makeFolders = classmethod(makeFolders)
  


#
# Class to hold information about an X-Plane scenery object
#
class SceneryObject:
  "An X-Plane scenery object"
  
  def __init__(self, filePathRoot, fileName):
    self.filePathRoot = filePathRoot
    self.fileName = fileName
    self.title =""
    self.author = ""
    self.textureAuthor = ""
    self.conversionAuthor = ""
    self.email = ""
    self.textureEmail = ""
    self.conversionEmail = ""
    self.url = ""
    self.textureUrl = ""
    self.conversionUrl = ""
    self.height = ""
    self.width = ""
    self.depth = ""
    self.description = ""
    self.virtualPaths = []
    self.tutorial = 0
    self.animated = 0
    self.exportPropagate = -1
    self.infoFilePath = ""
    self.screenshotFilePath = ""
    self.deprecatedVirtualPaths = []

  def getFilePath(self):
    return os.path.join(self.filePathRoot, self.fileName)

  def __cmp__(self, other):
    return cmp(self.title, other.title)
