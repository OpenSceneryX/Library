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
  
  def setVersionTag(cls, versionTag):
    cls.versionTag = versionTag
    cls.versionNumber = string.replace(cls.versionTag, "-", ".")
    cls.osxFolder = "tags/" + cls.versionNumber + "/OpenSceneryX-" + cls.versionNumber
    cls.osxPlaceholderFolder = "tags/" + cls.versionNumber + "/OpenSceneryX-Placeholder-" + cls.versionNumber

  setVersionTag = classmethod(setVersionTag)
  

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
    self.email = ""
    self.url = ""
    self.height = ""
    self.width = ""
    self.depth = ""
    self.description = ""
    self.virtualPaths = []
    self.tutorial = 0

  def getFilePath(self):
    return os.path.join(self.filePathRoot, self.fileName)

  def __cmp__(self, other):
    return cmp(self.title, other.title)
