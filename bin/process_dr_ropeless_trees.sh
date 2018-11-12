#!/usr/local/bin/bash
# NOTE THIS REQUIRES BASH 4. Hence the specific bash path above - use e.g. brew to install if required.
#
# This script traverses the set of trees supplied by Dr Ropeless (Barry Drake).  For each tree, it copies
# and renames the object file, placing it in an appropriate folder.  It looks up the full species name
# from the short name via a mapping file, and copies in a template info.txt file, filling in the details.
# Finally a screenshot is created.

# Setup and arguments
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MYDIR=$1
TREEROOTDIR=$SCRIPTDIR/../files/objects/vegetation/trees
FORESTROOTDIR=$SCRIPTDIR/../files/forests/trees
MAPPINGFILE=$SCRIPTDIR/tree_mappings.txt

if [ -z "$MYDIR" ] || [[ ! -d "$MYDIR" ]]
then
    echo "Usage: process_dr_ropeless_trees.sh path_containing_individual_tree_objects"
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
echo "Tree root dir: " $TREEROOTDIR
echo "Forest root dir: " $FORESTROOTDIR
echo "========================"

# Load mapping file
declare -A TREECATEGORYMAPPINGS
declare -A TREETITLEMAPPINGS
declare -A TREEDESCRIPTIONMAPPINGS
declare -A TREEFILENAMEMAPPINGS
  
while IFS=\| read key category title description filename
do
    if [[ ${key} = [\#]* ]]; then continue; fi  # Comments
    if [[ ${key} = "" ]]; then continue; fi     # Empty lines

    TREECATEGORYMAPPINGS[$key]=$category
    TREETITLEMAPPINGS[$key]=$title
    TREEDESCRIPTIONMAPPINGS[$key]=$description
    TREEFILENAMEMAPPINGS[$key]=$filename
done < $MAPPINGFILE

for F in $(find . -name '*.obj')
do
    FILENAME=$(basename "$F")
    MAINPARTS=(${FILENAME//_/ })
    SUBPARTS=(${MAINPARTS//./ })

    if [[ $FILENAME =~ (.*)_([0-9.]*).obj ]]; then
        TREECODE=${BASH_REMATCH[1]}
        TREEHEIGHT=${BASH_REMATCH[2]}
        TREECATEGORY=${TREECATEGORYMAPPINGS[${TREECODE}]}
        TREETITLE=${TREETITLEMAPPINGS[${TREECODE}]}
        TREEDESCRIPTION=${TREEDESCRIPTIONMAPPINGS[${TREECODE}]}
        TREEFILENAME=${TREEFILENAMEMAPPINGS[${TREECODE}]}

        if [ -z "$TREETITLE" ]; then
            #echo "Skipping $F - No mapping found"
            continue
        fi

        DESTINATIONCONTAINERPATH="${TREEROOTDIR}/${TREEFILENAME}"
        DESTINATIONOBJECTPATH="${DESTINATIONCONTAINERPATH}/${TREEHEIGHT}m"
        echo "Processing file $F into folder $DESTINATIONOBJECTPATH"

        if [ ! -d "$DESTINATIONCONTAINERPATH" ]; then
            mkdir -p "$DESTINATIONCONTAINERPATH"
            cp category.txt "$DESTINATIONCONTAINERPATH/category.txt"
            sed -i '' -E -e "s|Title:|Title: ${TREECATEGORY}|" $DESTINATIONCONTAINERPATH/category.txt
        fi

        mkdir -p "$DESTINATIONOBJECTPATH"
        cp info.txt "$DESTINATIONOBJECTPATH/info.txt"
        cp $F "$DESTINATIONOBJECTPATH/object.obj"

        sed -i '' -E -e "s|Title:|Title: ${TREETITLE}, ${TREEHEIGHT}m|" $DESTINATIONOBJECTPATH/info.txt
        sed -i '' -E -e "s|Description:|Description: An individual ${TREEDESCRIPTION}, height ${TREEHEIGHT}m.|" $DESTINATIONOBJECTPATH/info.txt
        sed -i '' -E -e "s|TEXTURE ../(.*)|TEXTURE ../../../../../forests/trees/\1|" $DESTINATIONOBJECTPATH/object.obj

        # $SCRIPTDIR/generate_screenshots.sh $DESTINATIONOBJECTPATH
    else
        echo "Unable to parse string $FILENAME"
    fi
done

echo "========================"
