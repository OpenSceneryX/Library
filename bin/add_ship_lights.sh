#!/bin/bash
# This script is based on a version supplied by Florian (PilotFlo), the author of
# MarineTrafficX, to automatically append navigation lights to all appropriate 
# OpenSceneryX objects.
#
# It should be run from the /bin folder and is intelligent in that it will insert the
# lights between two comments and if the script is re-run it will replace this section.

LIBRARY_ROOT=../files
PATTERN_START="# START Automatically added by add_ship_lights script"
PATTERN_END="# END Automatically added by add_ship_lights script"

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/container/1/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0.1227001 34.66044998 185.78469849" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.07769966 36.18114853 174.44863892" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.0246 19.72499847 6.38310003" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -16.89209938 27.36674881 166.22239685" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 16.97750092 27.4368 166.209198" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/container/2/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_left -16.89209938 27.36674881 166.22239685" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 16.97750092 27.4368 166.209198" >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0.1227001 34.66044998 185.78469849" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.07769966 36.18114853 174.44863892" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.0246 19.72499847 6.38310003" >> $FILE
echo $PATTERN_END >> $FILE


FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/cruise/1/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -1.01090002 42.82320023 224.54899597" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -1.01090002 42.82320023 224.54899597" >> $FILE
echo "LIGHT_NAMED	ship_nav_tail -0.49389982 7.16260004 254.32519531" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.00989997 45.11439896 42.28044891" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 15.02404976 32.72800064 34.00109863" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -14.93284988 32.72800064 34.05940247" >> $FILE
echo $PATTERN_END >> $FILE
 
FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/cruise/2/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0.31072497 7.99762487 285.35998535" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.37540001 40.66529846 193.80540466" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.10409999 45.7690506 64.36019897" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -14.41349983 34.79270172 51.57324982" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 14.4034996 34.76515198 51.54940033" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/cruise/3/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.12545 55.65494919 101.0738678" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.09980001 19.28064919 2.72650003" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 18.140625 33.61944962 68.18276978" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -18.46010017 33.61944962 68.05262756" >> $FILE
echo "LIGHT_NAMED	ship_nav_tail -0.78184986 14.96749973 258.24829102" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/cruise/4/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0 12.2062006 119.27009583" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 8.94999981 16.71500015 35.28499985" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.02639997 20.87005043 46.4280014" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.24509999 20.53499985 87.28549957" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -8.94999981 16.75499916 35.29499817" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/ferries/1/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_tail -10.2536993 10.32874966 152.11000061" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.03000021 30.39310074 27.42824936" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -15.41404915 21.83440018 22.54759979" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 15.39624977 21.69260025 22.55944824" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/power/1/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_tail -0.00497499 1.28999996 18.11720085" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.03084999 4.6328001 11.10885048" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -2.42000008 3.49720001 10.38860035" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 2.48000002 3.477 10.38449955" >> $FILE
echo $PATTERN_END >> $FILE
 
FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/tour/1/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.13389999 10.71629906 10.60849953" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -3.27469993 7.18000031 10.45944977" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 3.11039996 7.18000031 10.45265007" >> $FILE
echo "LIGHT_NAMED	ship_nav_tail -0.06980002 2 28.62660027" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/tour/2/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.0345 7.27904987 14.76029968" >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0.08290005 1.70655 31.78009987" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -1.74450004 8.03707504 15.83772564" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 1.65550005 8.03457451 15.83522511" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/tour/3/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0.01160002 2 26.37660217" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.0134 9.68810081 10.66965008" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -4.63880014 6.29085016 9.63059998" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 4.671 6.29374981 9.58880043" >> $FILE
echo $PATTERN_END >> $FILE

FILE="$LIBRARY_ROOT/objects/vehicles/boats_ships/vehicle_carriers/1/object.obj"
sed -i '' "/$PATTERN_START/,/$PATTERN_END/d" $FILE
echo $PATTERN_START >> $FILE
echo "LIGHT_NAMED	ship_mast_powered 0.40954971 37.08437347 152.03379822" >> $FILE
echo "LIGHT_NAMED	ship_nav_tail 0 18.55820084 190" >> $FILE
echo "LIGHT_NAMED	ship_mast_powered -0.0223 42.18984985 38.20820236" >> $FILE
echo "LIGHT_NAMED	ship_nav_left -19.20999908 34.77590179 18.21360016" >> $FILE
echo "LIGHT_NAMED	ship_nav_right 19.22999954 34.80329895 18.25670052" >> $FILE
echo $PATTERN_END >> $FILE
