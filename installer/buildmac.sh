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

# Code signing
/usr/libexec/PlistBuddy -c "Delete :CFBundleIdentifier" OpenSceneryX\ Installer.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Delete :NSHumanReadableCopyright" OpenSceneryX\ Installer.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Delete :LSApplicationCategoryType" OpenSceneryX\ Installer.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Add :CFBundleIdentifier string 'com.AustinGoudge.OpenSceneryX'" OpenSceneryX\ Installer.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Add :NSHumanReadableCopyright string '© 2012, Austin Goudge'" OpenSceneryX\ Installer.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Add :LSApplicationCategoryType string 'public.app-category.simulation-games'" OpenSceneryX\ Installer.app/Contents/Info.plist
codesign --signature-size 6400 -f -v -s 'Austin Goudge' OpenSceneryX\ Installer.app

zip -r ../../OpenSceneryX-Installer-Mac.zip OpenSceneryX\ Installer.app
