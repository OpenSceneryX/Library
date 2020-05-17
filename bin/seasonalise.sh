#!/bin/bash
# This script walks through every x-plane file in a given folder, duplicates it and names the new file
# correctly for the season.  It re-writes the TEXTURE definition to inject the season into the texture path
# (note it assumes the seasonal texture is one folder down from the original texture).

# Setup and arguments
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
SEASON=$1
MYDIR=$2

# Functions
handle_textures () {
    # Replace the texture reference
    sed -i '' -E -e "s~TEXTURE[[:space:]]+(.*\/|[[:space:]])([A-Za-z0-9_]+\.[A-Za-z]{3})~TEXTURE \1$SEASON/\2~" $FILEPATH/$NEWFILE
}

if [ -z $SEASON ]
then
    echo "Usage: seasonalise [season] path"
    exit
fi

if [ -z $MYDIR ] || [[ ! -d $MYDIR ]]
then
    echo "Usage: seasonalise [season] path"
    exit
else
    echo "Processing $MYDIR"
    cd $MYDIR
fi

echo "========================"
echo "Script dir: " $SCRIPTDIR
echo "Working dir: " $MYDIR
echo "========================"


# Store the input file separator and set it to newline.  Need to do this so we can store items containing
# spaces in our array
OLDIFS="$IFS"
IFS=$'\n'

for F in $(find . -type f -name 'facade.fac' -o -name 'forest.for' -o -name 'line.lin' -o -name 'object.obj' -o -name 'polygon.pol' | sort -V)
do
    FILENAME=$(basename "$F")
    FILEPATH=$(dirname "$F")

    echo Processing file $F

    case $F in
        *fac)
            NEWFILE=facade_$SEASON.fac
            cp $F $FILEPATH/$NEWFILE
            handle_textures
            ;;
        *for)
            NEWFILE=forest_$SEASON.for
            cp $F $FILEPATH/$NEWFILE
            handle_textures
            ;;
        *lin)
            NEWFILE=line_$SEASON.lin
            cp $F $FILEPATH/$NEWFILE
            handle_textures
            ;;
        *obj)
            NEWFILE=object_$SEASON.obj
            cp $F $FILEPATH/$NEWFILE
            handle_textures
            ;;
        *pol)
            NEWFILE=polygon_$SEASON.pol
            cp $F $FILEPATH/$NEWFILE
            handle_textures
            ;;
        *)
    esac
done

# Restore the old input file separator
IFS="$OLDIFS"

echo "========================"
echo "Done"
echo "========================"
