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
    echo "Usage: process_dr_ropeless_treee.sh path"
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
declare -A TREEMAPPINGS
  
while IFS=\| read key value
do
    if [[ ${key} = [\#]* ]]; then continue; fi  # Comments
    if [[ ${key} = "" ]]; then continue; fi     # Empty lines

    TREEMAPPINGS[$key]=$value
done < $MAPPINGFILE

# Find the highest numbered subfolder that already exists in TREEROOTIR
N=1
while [[ -d "$TREEROOTDIR/$N" ]] ; do
    N=$(($N+1))
done

# N is now the next incremental folder number

for F in $(find . -name '*.obj')
do
    FILENAME=$(basename "$F")
    MAINPARTS=(${FILENAME//_/ })
    SUBPARTS=(${MAINPARTS//./ })

    if [[ $FILENAME =~ (.*)_([0-9.]*).obj ]]; then
        TREECODE=${BASH_REMATCH[1]}
        TREEHEIGHT=${BASH_REMATCH[2]}

        echo "$FILENAME"
        echo "  Full Name: ${TREEMAPPINGS[${TREECODE}]}"
        echo "  Height   : $TREEHEIGHT"
    else
        echo "unable to parse string $FILENAME"
    fi

    #echo Processing file $F into folder $TREEROOTDIR/$N/

    # This hunts for the location of this file in the forest dir.  Don't need to do this because 
    # we're using a simple mapping file now
    #echo Searching for ${PARTS[0]} in $FORESTROOTDIR
    #G=$(grep -a -m 1 -r "${PARTS[0]}" $FORESTROOTDIR | head -1 )

    #break;
    # mkdir $N
    # cp info.txt $N/info.txt

    # case $F in
    #     *fac)
    #         NEWFILE=$N/facade.fac
    #         cp $F $NEWFILE
    #         handle_textures
    #         ;;
    #     *for)
    #         NEWFILE=$N/forest.for
    #         cp $F $NEWFILE
    #         handle_textures
    #         ;;
    #     *lin)
    #         NEWFILE=$N/line.lin
    #         cp $F $NEWFILE
    #         handle_textures
    #         ;;
    #     *obj)
    #         NEWFILE=$N/object.obj
    #         cp $F $NEWFILE
    #         handle_textures
    #         # It's a .obj file, generate screenshot
    #         $SCRIPTDIR/generate_screenshots.sh $MYDIR/$N/
    #         ;;
    #     *pol)
    #         NEWFILE=$N/polygon.pol
    #         cp $F $NEWFILE
    #         handle_textures
    #         ;;
    #     *)
    # esac

    # # Include original filename at beginning of Title line inside info.txt for reference
    # sed -i '' -E -e "s|Title: (.*)|Title: ---$FILENAME--- \1|" $N/info.txt

    N=$(($N+1))

done


echo "========================"

echo "========================"
