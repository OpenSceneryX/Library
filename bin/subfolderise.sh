#!/bin/bash
# This script walks through every x-plane file in a given folder, creates a subfolder, either
# incrementally numbered or named with the same name as the object
# and moves the x-plane file into the folder.  It re-writes the TEXTURE definition to replace the texture path
# with one specified as an argument. In addition, it copies a template info.txt file into each
# subfolder, and it expects this template info.txt file to be in the same folder. It generates a
# screenshot if it's a .obj and finally it reports all unique textures used.

# Setup and arguments
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
USEFILENAMEASFOLDER=false
MOVEFILES=false

# Functions
show_help() {
cat << EOF
Usage: ${0##*/} [-hn] [-t TEXTUREPATH] [DIR]...
Walks through every x-plane file in a given directory DIR, creates a subfolder, either incrementally numbered or named after the source file.

    -h              display this help and exit
    -t TEXTUREPATH  the relative path to shared textures, this path is injected into the TEXTURE definition. If this is omitted, the textures are assumed to be local and are moved into the subfolders.
    -n              name the subfolders after the source file, default is to number folders incrementally
    -m              move rather than copy files (best to use only when certain the operation is working)

EOF
}

die() {
    printf '%s\n' "$1" >&2
    exit 1
}

handle_textures () {
    if [ -z $TEXTUREPATH ]
    then
        # Move the texture
        TEXTURENAME=($(sed -n -E -e "s~TEXTURE[[:space:]]+([A-Za-z0-9_-]+)\.[A-Za-z]{3}~\1~p" $NEWFILE))
        if [ "$MOVEFILES" = true ]
        then
            mv $TEXTURENAME.png $FOLDERNAME/$TEXTURENAME.png
            mv $TEXTURENAME.dds $FOLDERNAME/$TEXTURENAME.dds
        else
            cp $TEXTURENAME.png $FOLDERNAME/$TEXTURENAME.png
            cp $TEXTURENAME.dds $FOLDERNAME/$TEXTURENAME.dds
        fi
    else
        # Replace the texture reference
        sed -i '' -E -e "s~TEXTURE[[:space:]]+(.*\/|[[:space:]])([A-Za-z0-9_-]+\.[A-Za-z]{3})~TEXTURE $TEXTUREPATH/\2~" $NEWFILE
        TEXTUREPATHS+=($(grep -E "TEXTURE[[:space:]]+(.*\/|[[:space:]])([A-Za-z0-9_-]+\.[A-Za-z]{3})" $NEWFILE))
    fi
}

# Handle parameters
while :; do
    case $1 in
        -h|-\?|--help)
            show_help    # Display a usage synopsis.
            exit
            ;;
        -t|--texturepath)       # Takes an option argument; ensure it has been specified.
            if [ "$2" ]; then
                TEXTUREPATH=$2
                shift
            else
                die 'ERROR: "--texturepath" requires a non-empty option argument.'
            fi
            ;;
        --texturepath=?*)
            TEXTUREPATH=${1#*=} # Delete everything up to "=" and assign the remainder.
            ;;
        --texturepath=)         # Handle the case of an empty --file=
            die 'ERROR: "--texturepath" requires a non-empty option argument.'
            ;;
        -n|--namefolders)
            USEFILENAMEASFOLDER=true
            ;;
        -m|--move)
            MOVEFILES=true
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
    FILEROOT="${FILENAME%.*}"

    if [ "$USEFILENAMEASFOLDER" = true ]
    then
        FOLDERNAME=$FILEROOT # New folder is the root of the filename without extension
    else
        FOLDERNAME=$N # New folder is a sequential integer
    fi

    echo Processing file $F into folder $FOLDERNAME/

    mkdir $FOLDERNAME
    cp info.txt $FOLDERNAME/info.txt

    case $F in
        *fac)
            NEWFILE=$FOLDERNAME/facade.fac
            if [ "$MOVEFILES" = true ]
            then
                mv $F $NEWFILE
            else
                cp $F $NEWFILE
            fi
            handle_textures
            ;;
        *for)
            NEWFILE=$FOLDERNAME/forest.for
            if [ "$MOVEFILES" = true ]
            then
                mv $F $NEWFILE
            else
                cp $F $NEWFILE
            fi
            handle_textures
            ;;
        *lin)
            NEWFILE=$FOLDERNAME/line.lin
            if [ "$MOVEFILES" = true ]
            then
                mv $F $NEWFILE
            else
                cp $F $NEWFILE
            fi
            handle_textures
            ;;
        *obj)
            NEWFILE=$FOLDERNAME/object.obj
            if [ "$MOVEFILES" = true ]
            then
                mv $F $NEWFILE
            else
                cp $F $NEWFILE
            fi
            handle_textures
            # It's a .obj file, generate screenshot
            $SCRIPTDIR/generate_screenshots.sh auto $MYDIR/$FOLDERNAME/
            ;;
        *pol)
            NEWFILE=$FOLDERNAME/polygon.pol
            if [ "$MOVEFILES" = true ]
            then
                mv $F $NEWFILE
            else
                cp $F $NEWFILE
            fi
            handle_textures
            ;;
        *)
    esac

    # Include original filename at beginning of Title line inside info.txt for reference
    sed -i '' -E -e "s|Title: (.*)|Title: ---$FILENAME--- \1|" $FOLDERNAME/info.txt

    N=$(($N+1))
done

# Restore the old input file separator
IFS="$OLDIFS"

echo "========================"
echo "Unique textures in this set of files:"
eval TEXTUREPATHS=($(printf "%q\n" "${TEXTUREPATHS[@]}" | sort -u))
printf "%s\n" "${TEXTUREPATHS[@]}"
echo "========================"
