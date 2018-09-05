#!/bin/bash
# This script walks through every x-plane file in a given folder, creates a subfolder, incrementally numbered
# and moves the x-plane file into the folder.  It re-writes the TEXTURE definition to replace the texture path
# with one specified as an argument. In addition, it copies a template info.txt file into each
# subfolder, and it expects this template info.txt file to be in the same folder. It generates a
# screenshot if it's a .obj and finally it reports all unique textures used.

# Setup and arguments
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
TEXTUREPATH=$1
MYDIR=$2

# Functions
handle_textures () {
    # Replace the texture reference
    sed -i '' -E -e "s|TEXTURE[[:space:]]+.*\/([^/]+\.[A-Za-z]{3})|TEXTURE $TEXTUREPATH/\1|" $NEWFILE
    TEXTUREPATHS+=($(grep -E "TEXTURE[[:space:]]+.*\/([^/]+\.[A-Za-z]{3})" $NEWFILE))
}


if [ -z TEXTUREPATH ]
then
    echo "Usage: subfolderise relative-texture-path path"
    exit
fi

if [ -z $MYDIR ] || [[ ! -d $MYDIR ]]
then
    echo "Usage: subfolderise relative-texture-path path"
    exit
elif [[ ! -f $MYDIR/info.txt ]]
then
    echo "No template info.txt file found at path, cannot continue"
    exit
else
    echo "Processing $MYDIR"
    cd $MYDIR
fi

echo "========================"
echo "Script dir: " $SCRIPTDIR
echo "Working dir: " $MYDIR
echo "========================"

# Find the highest numbered subfolder that already exists
N=1
while [[ -d "$MYDIR/$N" ]] ; do
    N=$(($N+1))
done

# N is now the next incremental folder number

TEXTUREPATHS=()

# Store the input file separator and set it to newline.  Need to do this so we can store items containing
# spaces in our array
OLDIFS="$IFS"
IFS=$'\n'

for F in $(find . -type f -maxdepth 1 -name '*.fac' -o -name '*.for' -o -name '*.lin' -o -name '*.obj' -o -name '*.pol' | sort -V)
do
    FILENAME=$(basename "$F")

    echo Processing file $F into folder $N/
    
    mkdir $N
    cp info.txt $N/info.txt

    case $F in
        *fac)
            NEWFILE=$N/facade.fac
            cp $F $NEWFILE
            handle_textures
            ;;
        *for)
            NEWFILE=$N/forest.for
            cp $F $NEWFILE
            handle_textures
            ;;
        *lin)
            NEWFILE=$N/line.lin
            cp $F $NEWFILE
            handle_textures
            ;;
        *obj)
            NEWFILE=$N/object.obj
            cp $F $NEWFILE
            handle_textures
            # It's a .obj file, generate screenshot
            $SCRIPTDIR/generate_screenshots.sh $MYDIR/$N/
            ;;
        *pol)
            NEWFILE=$N/polygon.pol
            cp $F $NEWFILE
            handle_textures
            ;;
        *)
    esac

    # Include original filename at beginning of Title line inside info.txt for reference
    sed -i '' -E -e "s|Title: (.*)|Title: ---$FILENAME--- \1|" $N/info.txt

    N=$(($N+1))
done

# Restore the old input file separator
IFS="$OLDIFS"

echo "========================"
echo "Unique textures in this set of files:"
eval TEXTUREPATHS=($(printf "%q\n" "${TEXTUREPATHS[@]}" | sort -u))
printf "%s\n" "${TEXTUREPATHS[@]}"
echo "========================"
