#!/bin/bash
# Script to build a library release
# Version: $Revision $

# Include common functions
. functions.sh

VERSION=""

if [ ! -d "../files" ] || [ ! -d "../../tags" ]; then
  echo "Error: This script must be run from the 'trunk/bin' directory inside a full checkout of the scenery library"
  exit
fi

cd "../.."

echo
echo "========================"
echo "OpenScenery Release"
echo "========================"

until [ "$VERSION" != "" ]; do
  read -p "Enter the release number (e.g. 1-0-1): " VERSION
done
  
read -p "Do you want to update the 'files' directory before release? [Y/n]: " UPDATE

if [ "$UPDATE" == "" ] || [ "$UPDATE" == "Y" ] || [ "$UPDATE" == "y" ]; then
  svn update trunk/files
fi

echo "------------------------"
echo "Creating release tag"
echo "svn mkdir tags/$VERSION"
#svn mkdir tags/$VERSION
mkdir tags/$VERSION

echo "------------------------"
echo "Creating library.txt"
echo "A" 1>tags/$VERSION/library.txt
echo "800" 1>>tags/$VERSION/library.txt
echo "LIBRARY" 1>>tags/$VERSION/library.txt

echo "------------------------"
echo "Copying files"

traverse "trunk/files" "tags/$VERSION" 0 ""

#find . -name '*.obj' -print -exec cp {} \;

echo "Complete"
echo "========================"
echo