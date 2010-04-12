#!/bin/sh

echo
echo ------------------------
echo Compressing Windows Installer
echo ------------------------
echo

# Create a zip of OpenSceneryX Installer but exclude resource forks
# Mac OS 10.4 and earlier: export COPY_EXTENDED_ATTRIBUTES_DISABLE=true
export COPYFILE_DISABLE=true

cd Builds\ -\ Installer.rbvcp/Windows/
zip -r ../../OpenSceneryX-Installer-Windows.zip OpenSceneryX\ Installer
