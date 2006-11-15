# functions.sh
# Common functions
# Version: $Revision $

traverse() {
  # Traverse a directory
  # Takes three arguments:
  #  1. The root of the source folder structure
  #  2. The root of the target folder structure
  #  3. The current depth
  #  4. The working directory within the source structure

  if [ -z $4 ]; then
    local source_folder=$1
    local target_folder=$2
  else
    local source_folder=$1/$4
    local target_folder=$2/$4
  fi

  ls "$source_folder" | while read i
  do
    if [ -d "$source_folder/$i" ]; then
      # Directory
      
      if [ -f "$source_folder/$i/object.obj" ]; then
        # Object file found, locate the texture and info files
        local texture=$(grep "TEXTURE" "$source_folder/$i/object.obj" | awk '{print $2}')
        local export_override=$(grep "Export:" "$source_folder/$i/info.txt" | awk '{print $2}')

        if [ -f "$source_folder/$i/$texture" ]; then
          echo "Object file found with texture: $source_folder/$i/object.obj"
          
          mkdir -p $target_folder/$i
          cp $source_folder/$i/object.obj $target_folder/$i/object.obj
          cp $source_folder/$i/$texture $target_folder/$i/$texture
          
          # Write to library.txt file
          if [[ $export_override != "" ]]; then
            echo "Export overridden: '$export_override'"
            echo "EXPORT openscenery/$4/$export_override $4/$i/object.obj" 1>>$2/library.txt
          else
            echo "EXPORT openscenery/$4/$i $4/$i/object.obj" 1>>$2/library.txt
          fi          
        else
          echo "Error: '$source_folder/$i/object.obj' contains a reference to the texture '$texture' but it cannot be found, object excluded"
        fi
        
      elif [ -f "$source_folder/$i/facade.fac" ]; then
      
        echo "Facade file found - Facades not handled yet"
        
      elif [ -f "$source_folder/$i/forest.for" ]; then

        echo "Forest file found - Forests not handled yet"

      fi
      
      if [ -z $4 ]; then
        local working_folder=$i
      else
        local working_folder=$4/$i
      fi
      
      traverse "$1" "$2" `expr $3 + 1` "$working_folder"
    # else 
      # echo File
    fi
  done
}
