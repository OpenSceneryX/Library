#!/usr/local/bin/bash
# NOTE THIS REQUIRES BASH 4. Hence the specific bash path above - use e.g. brew to install if required.
#
# This script traverses the set of vegetation supplied by Dr Ropeless (Barry Drake).  For each plant, it copies
# and renames the object file, placing it in an appropriate folder.  It looks up the full species name
# from the short name via a mapping file, and copies in a template info.txt file, filling in the details.
# Finally a screenshot is created.

# Setup and arguments
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MYDIR=$1
VEGETATIONROOTDIR=$SCRIPTDIR/../files/objects/vegetation
FORESTROOTDIR=$SCRIPTDIR/../files/forests/trees
MAPPINGFILE=$SCRIPTDIR/tree_mappings.txt

if [ -z "$MYDIR" ] || [[ ! -d "$MYDIR" ]]
then
    echo "Usage: process_dr_ropeless_trees.sh path_containing_individual_vegetation_objects"
    exit
elif [[ ! -f $MYDIR/info.txt ]]
then
    echo "No template info.txt file found at path, cannot continue"
    exit
else
    echo "Processing $MYDIR"
    cd "$MYDIR"
fi

echo "========================"
echo "Script dir: " $SCRIPTDIR
echo "Working dir: " $MYDIR
echo "Vegetation root dir: " $VEGETATIONROOTDIR
echo "Forest root dir: " $FORESTROOTDIR
echo "========================"

# Load mapping file
declare -A CATEGORYMAPPINGS
declare -A TITLEMAPPINGS
declare -A DESCRIPTIONMAPPINGS
declare -A FILENAMEMAPPINGS
  
while IFS=\| read key category title description filename
do
    if [[ ${key} = [\#]* ]]; then continue; fi  # Comments
    if [[ ${key} = "" ]]; then continue; fi     # Empty lines

    CATEGORYMAPPINGS[$key]=$category
    TITLEMAPPINGS[$key]=$title
    DESCRIPTIONMAPPINGS[$key]=$description
    FILENAMEMAPPINGS[$key]=$filename
done < $MAPPINGFILE

for F in $(find . -name '*.obj')
do
    FILENAME=$(basename "$F")
    MAINPARTS=(${FILENAME//_/ })
    SUBPARTS=(${MAINPARTS//./ })

    if [[ $FILENAME =~ (.*)_([0-9.]*).obj ]]; then
        CODE=${BASH_REMATCH[1]}
        HEIGHT="$(printf "%g" ${BASH_REMATCH[2]})" # Parse the number as double, removing leading and trailing '0's
        CATEGORY=${CATEGORYMAPPINGS[${CODE}]}
        TITLE=${TITLEMAPPINGS[${CODE}]}
        DESCRIPTION=${DESCRIPTIONMAPPINGS[${CODE}]}
        FILENAME=${FILENAMEMAPPINGS[${CODE}]}

        if [ -z "$TITLE" ]; then
            #echo "Skipping $F - No mapping found"
            continue
        fi

        DESTINATIONCONTAINERPATH="${VEGETATIONROOTDIR}/${FILENAME}"
        DESTINATIONOBJECTPATH="${DESTINATIONCONTAINERPATH}/${HEIGHT}m"
        # Calculate depth of object path by counting number of "/" in path
        DESTINATIONOBJECTPATHDEPTH=$(awk -F"/" '{print NF}' <<< "${FILENAME}")
        # Build texture path by repeating "../" the same number of times as the depth
        TEXTUREPATH="../../../$(seq -f '../' -s '' $DESTINATIONOBJECTPATHDEPTH)forests/trees/"

        echo "Processing file $F into folder $DESTINATIONOBJECTPATH"

        if [ ! -d "$DESTINATIONCONTAINERPATH" ]; then
            mkdir -p "$DESTINATIONCONTAINERPATH"
            cp category.txt "$DESTINATIONCONTAINERPATH/category.txt"
            sed -i '' -E -e "s|Title:|Title: ${CATEGORY}|" $DESTINATIONCONTAINERPATH/category.txt
        fi

        mkdir -p "$DESTINATIONOBJECTPATH"
        cp info.txt "$DESTINATIONOBJECTPATH/info.txt"
        cp $F "$DESTINATIONOBJECTPATH/object.obj"

        sed -i '' -E -e "s|Title:|Title: ${TITLE}, ${HEIGHT}m|" $DESTINATIONOBJECTPATH/info.txt
        sed -i '' -E -e "s|Description:|Description: An individual ${DESCRIPTION}, height ${HEIGHT}m.|" $DESTINATIONOBJECTPATH/info.txt
        sed -i '' -E -e "s|TEXTURE ../(.*)|TEXTURE ${TEXTUREPATH}\1|" $DESTINATIONOBJECTPATH/object.obj

        if [ ! -f "${DESTINATIONOBJECTPATH}/screenshot.jpg" ]; then
            $SCRIPTDIR/generate_screenshots.sh $DESTINATIONOBJECTPATH
        fi
    else
        echo "Unable to parse string $FILENAME"
    fi
done

echo "========================"
