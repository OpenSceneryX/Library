#!/bin/sh

# Create a tarball of OpenSceneryX Installer but exclude resource forks
# Mac OS 10.4 and earlier: export COPY_EXTENDED_ATTRIBUTES_DISABLE=true
export COPYFILE_DISABLE=true
tar -cf OpenSceneryX\ Installer\ Linux.tar OpenSceneryX\ Installer
gzip OpenSceneryX\ Installer\ Linux.tar
