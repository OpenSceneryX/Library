#!/bin/bash
# This script walks through every x-plane file in a given folder, creates a subfolder, incrementally numbered
# and moves the file into the folder.  In addition, it copies a template info.txt file into each
# subfolder, and it expects this template info.txt file to be in the same folder.  Finally, it generates a
# screenshot if it's a .obj

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MYDIR=$1

echo "Script dir: " $SCRIPTDIR
echo "Working dir: " $MYDIR

echo "========================"
if [ -z $MYDIR ] || [[ ! -d $MYDIR ]]
then
    echo "Passed argument is not a directory, cannot continue"
    exit
elif [[ ! -f $MYDIR/info.txt ]]
then
    echo "No template info.txt file found, cannot continue"
    exit
else
    echo "Processing $MYDIR"
    cd $MYDIR
fi
echo "========================"

# Find the highest numbered subfolder that already exists
N=1
while [[ -d "$MYDIR/$N" ]] ; do
    N=$(($N+1))
done

# N is now the next incremental folder number

for F in $(find . -type f -maxdepth 1 -name '*.fac' -o -name '*.for' -o -name '*.lin' -o -name '*.obj' -o -name '*.pol')
do
    FILENAME=$(dirname "$F")

    echo Processing file $F into folder $N/
    
    mkdir $N
    cp info.txt $N/info.txt

    case $F in
        *fac)
            mv $F $N/facade.fac
            ;;
        *for)
            mv $F $N/forest.for
            ;;
        *lin)
            mv $F $N/line.lin
            ;;
        *obj)
            mv $F $N/object.obj
            # It's a .obj file, generate screenshot
            $SCRIPTDIR/generate_screenshots.sh $MYDIR/$N/
            ;;
        *pol)
            mv $F $N/polygon.pol
            ;;
        *)
    esac

    N=$(($N+1))
done