#!/bin/bash
# This script walks through every object in the library and re-generates its screenshot.
#
# Prerequisites:
#   - Must be run on a Mac
#   - Marginal's quick previewer for X-Plane .obj files from here: https://github.com/Marginal/QLXPlaneObj
#   - ImageOptim from here: https://github.com/ImageOptim/ImageOptim
#   - ImageOptim-CLI from here: https://github.com/JamieMason/ImageOptim-CLI
#
# Usage: generate_screenshots [manual|auto|resize] [PATH]
#   - manual: Look for Mac-generated screenshots to process where filename starts with 'Screenshot ', just convert to jpg, rename and optimise
#   - auto (default): Look for .obj files and create a screenshot for each, optimised
#   - resize: Look for screenshot.jpg files and resize them proportionally to 500 pixels wide

BASEDIR=$(dirname "$0")
MODE=$1
MYDIR=$2

echo "========================"

if [ -z $MYDIR ] || [[ ! -d $MYDIR ]]
then
    echo "Second argument is not a directory"
    exit
else
    echo "Generating screenshots for all objects within $MYDIR"
    cd $MYDIR
fi

echo "========================"

if [ "$MODE" == "manual" ]
then
    echo "Processing manual screenshots"
    echo "-----------------------------"

    find . -name "Screenshot *.png"|while read f
    do
        DIR=$(dirname "$f")
        SCREENSHOT_PNG="$f"
        SCREENSHOT_JPEG=$DIR"/screenshot.jpg"

        echo "PNG: $SCREENSHOT_PNG"
        echo "JPEG: $SCREENSHOT_JPEG"

        # Convert to jpeg and resize
        sips -s format jpeg "$SCREENSHOT_PNG" --resampleWidth 500 --out "$SCREENSHOT_JPEG"

        # Optimise
        imageoptim -Q "$SCREENSHOT_JPEG"

        # Remove PNG
        rm "$SCREENSHOT_PNG"
    done
elif [ "$MODE" == "resize" ]
then
    echo "Resizing screenshots"
    echo "--------------------"

    find . -name "screenshot.jpg"|while read f
    do
        echo "SCREESHOT: $f"

        # Convert to jpeg and resize
        sips "$f" --resampleWidth 500

        # Optimise
        imageoptim -Q "$f"
    done
else
    echo "Processing automatic screenshots"
    echo "--------------------------------"

    find . -name "*.obj"|while read f
    do
        DIR=$(dirname "$f")
        FILE=$(basename "$f")
        FILEBASE=${FILE%.*}

        sep='_'
        case $FILEBASE in
        (*"$sep"*)
            LEFT=${FILEBASE%%"$sep"*}
            RIGHT=${FILEBASE#*"$sep"}
            SCREENSHOT_JPEG=$DIR"/screenshot_"$RIGHT".jpg"
            ;;
        (*)
            SCREENSHOT_JPEG=$DIR"/screenshot.jpg"
            ;;
        esac
        SCREENSHOT_PNG=$DIR"/"$FILE".png"

        echo "PNG: $SCREENSHOT_PNG"
        echo "JPEG: $SCREENSHOT_JPEG"

        # Generate thumbnail
        qlmanage -t "$f" -s 500 -o "$DIR"

        # Convert to jpeg
        sips -s format jpeg "$SCREENSHOT_PNG" --out "$SCREENSHOT_JPEG"

        # Optimise
        imageoptim -Q "$SCREENSHOT_JPEG"

        # Remove PNG
        rm "$SCREENSHOT_PNG"
    done
fi