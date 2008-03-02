#!/bin/sh

# Create a tarball of OpenSceneryX Installer but exclude resource forks
# Mac OS 10.4 and earlier: export COPY_EXTENDED_ATTRIBUTES_DISABLE=true
export COPYFILE_DISABLE=true
zip -r OpenSceneryX\ Installer\ Windows.zip OpenSceneryX\ Installer
