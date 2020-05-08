#!/bin/bash
# This script walks through every object in the library and re-generates its screenshot(s). This includes seasonal
# screenshots where seasonal variants are present.
#
# Prerequisites:
#   - Must be run on a Mac
#   - For 'auto' mode, Marginal's quick previewer for X-Plane .obj files from here: https://github.com/Marginal/QLXPlaneObj
#   - For 'auto3js' mode, a web server running the OpenSceneryX website (point SCREENSHOTURL to the URL for screenshot generation)
#   - ImageOptim from here: https://github.com/ImageOptim/ImageOptim
#   - ImageOptim-CLI from here: https://github.com/JamieMason/ImageOptim-CLI
#
# Usage: generate_screenshots [manual|auto|auto3js|resize] [PATH]
#   - auto3js: Look for .for, .fac, .lin, .obj and .pol files and create a screenshot for each using the 3js renderer, optimised
#   - auto: Look for .obj files and create a screenshot for each, optimised
#   - manual: Look for Mac-generated screenshots to process where filename starts with 'Screenshot ', just convert to jpg, rename and optimise
#   - resize: Look for screenshot.jpg files and resize them proportionally to 500 pixels wide

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
BASEDIR=$(dirname "$0")
MODE=$1
MYDIR=$2
SCREENSHOTURL=http://osx.local/three.js-screenshot/

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
elif [ "$MODE" == "auto" ]
then
    echo "Automatic screenshots"
    echo "---------------------"

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

        # Generate thumbnail (as filename with png extension)
        qlmanage -t "$f" -s 500 -o "$DIR"

        # Convert to jpeg
        sips -s format jpeg "$SCREENSHOT_PNG" --out "$SCREENSHOT_JPEG"

        # Optimise
        imageoptim -Q "$SCREENSHOT_JPEG"

        # Remove PNG
        rm "$SCREENSHOT_PNG"
    done
elif [ "$MODE" == "auto3js" ]
then
    echo "Automatic screenshots, threejs"
    echo "------------------------------"

    find . -type f \( -iname \*.fac -o -iname \*.for -o -iname \*.lin -o -iname \*.obj -o -iname \*.pol \)|while read f
    do
        DIR=$(dirname "$f")
        FILE=$(basename "$f")
        FILEBASE=${FILE%.*}
        REPODIR="$( cd "$SCRIPTDIR/../files/" && pwd )"
        URLBASE=${MYDIR#"$REPODIR"}

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
        echo "URL: $SCREENSHOTURL?path=$URLBASE$f"

        # Generate screenshot
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --screenshot="$MYDIR/$SCREENSHOT_PNG" --hide-scrollbars --window-size=500,500 --virtual-time-budget=10000 "$SCREENSHOTURL?path=$URLBASE$f"

        # Convert to jpeg
        sips -s format jpeg "$SCREENSHOT_PNG" --out "$SCREENSHOT_JPEG"

        # Optimise
        imageoptim -Q "$SCREENSHOT_JPEG"

        # Remove PNG
        rm "$SCREENSHOT_PNG"
    done
else
    echo "Invalid mode: $MODE"
fi