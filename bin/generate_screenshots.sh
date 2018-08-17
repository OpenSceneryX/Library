#!/bin/bash
# This script walks through every object in the library and re-generates its screenshot.
# 
# Prerequisites:
#   - Must be run on a Mac
#   - Marginal's quick previewer for X-Plane .obj files from here: https://github.com/Marginal/QLXPlaneObj
#   - ImageOptim from here: https://github.com/ImageOptim/ImageOptim
#   - ImageOptim-CLI from here: https://github.com/JamieMason/ImageOptim-CLI

BASEDIR=$(dirname "$0")
MYDIR=$1

echo "========================"
if [ -z $MYDIR ] || [[ ! -d $MYDIR ]]
then
    echo "Passed argument is not a directory, generating screenshots for entire library"
    cd $BASEDIR/../files/objects
else
    echo "Generating screenshots for all objects within $MYDIR"
    cd $MYDIR
fi
echo "========================"

for f in $(find . -name '*.obj')
do
    DIR=$(dirname "$f")
    SCREENSHOT_PNG=$DIR"/object.obj.png"
    SCREENSHOT_JPEG=$DIR"/screenshot.jpg"

    echo "PNG: $SCREENSHOT_PNG"
    echo "JPEG: $SCREENSHOT_JPEG"

    # Generate thumbnail
    qlmanage -t $f -s 500 -o $DIR

    # Convert to jpeg
    sips -s format jpeg $SCREENSHOT_PNG --out $SCREENSHOT_JPEG

    # Optimise
    imageoptim -Q $SCREENSHOT_JPEG 

    # Remove PNG
    rm $SCREENSHOT_PNG
done