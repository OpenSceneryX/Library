#!/bin/bash
# This script walks through every PNG file in a given folder, and if no corresponding DDS file exists
# it uses ImageMagick to convert the PNG to DDS.

# Setup and arguments
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# Functions
show_help() {
cat << EOF
Usage: ${0##*/} [-h] [DIR]...
Walks through every PNG file in a given folder, and if no corresponding DDS file exists it creates one by converting the PNG.

    -h              display this help and exit

EOF
}

die() {
    printf '%s\n' "$1" >&2
    exit 1
}

# Handle parameters
while :; do
    case $1 in
        -h|-\?|--help)
            show_help    # Display a usage synopsis.
            exit
            ;;
        --)              # End of all options.
            shift
            break
            ;;
        -?*)
            printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
            ;;
        *)               # Default case: No more options, so break out of the loop.
            break
    esac

    shift
done

MYDIR=$@ # Remaining parameters are filepath

if [ -z $MYDIR ] || [[ ! -d $MYDIR ]]
then
    show_help
    exit
else
    echo "Processing $MYDIR"
    cd $MYDIR
fi

echo "========================"
echo "Script dir: " $SCRIPTDIR
echo "Working dir: " $MYDIR
echo "========================"

for F in $(find . -type f -name '*.png' | sort -V)
do
    FILENAME=$(basename -- "$F")
    FILEPATH=$(dirname -- "$F")
    FILEROOT="${FILENAME%.*}"
    DDSFILE=$FILEROOT.dds

    if [[ ! -f $FILEPATH/$DDSFILE ]]
    then
        echo Processing PNG: $F
        echo Output DDS: $FILEPATH/$DDSFILE

        convert -format dds -define dds:compression=dxt5 $F $FILEPATH/$DDSFILE
    else
        echo Skipping $F, DDS found
    fi
done

echo "========================"
echo "Finished"
echo "========================"
