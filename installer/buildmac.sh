#!/bin/sh

echo
echo ------------------------
echo Compressing Mac Installer
echo ------------------------
echo

# Create a zip of OpenSceneryX Installer but exclude resource forks
# Mac OS 10.4 and earlier: export COPY_EXTENDED_ATTRIBUTES_DISABLE=true
export COPYFILE_DISABLE=true

cd Builds\ -\ Installer.rbvcp/Mac\ OS\ X\ \(Intel\)/
zip -r ../../OpenSceneryX-Installer-Mac.zip OpenSceneryX\ Installer.app
