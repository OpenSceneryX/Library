#!/usr/local/bin/python

# classes.py
# Classes
# Version: $Revision$

import datetime
import string

#
# Class to hold configuration values
#
class Configuration:
  """Generic container for shared variables."""
  versionTag = ""
  versionNumber = ""
  versionDate = datetime.datetime.now().strftime("%c")
  
  def setVersionTag(cls, versionTag):
    cls.versionTag = versionTag
    cls.versionNumber = string.replace(cls.versionTag, "-", ".")
    cls.osxFolder = "tags/" + cls.versionNumber + "/OpenSceneryX-" + cls.versionNumber
    cls.osxPlaceholderFolder = "tags/" + cls.versionNumber + "/OpenSceneryX-Placeholder-" + cls.versionNumber

  setVersionTag = classmethod(setVersionTag)