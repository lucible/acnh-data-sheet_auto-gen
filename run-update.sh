#!/bin/bash
# https://unix.stackexchange.com/a/505342
# argument switching code borrowed from the above link - many thanks!

helpFunction()
{
   echo ""
   echo "Usage: $0 -a folderID -b accessTK -c version"
   echo -e "\t-f Google Drive folder ID"
   echo -e "\t-t OAuth 2.0 Playground Access Token"
   echo -e "\t-v Version number without periods"
   exit 1 # Exit script after printing help
}

while getopts "f:t:v:" opt
do
   case "$opt" in
      f ) folderID="$OPTARG" ;;
      t ) accessTK="$OPTARG" ;;
      v ) version="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$folderID" ] || [ -z "$accessTK" ]  || [ -z "$version" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct

echo "Downloading BCSVs..."

# prep folders
mkdir ./data/game_raw/bcsv/${version} || true
mkdir ./temp || true

# begin BCSV download
cd ./temp
gdrive download --recursive ${folderID} --access-token ${accessTK}

# move BCSVs to correct location
mv ./Bcsv/* ../data/game_raw/bcsv/${version}/

# clean up
cd ..
rm -r ./temp

echo "Building ${version} specs file..."

cd ./cylindrical-earth

python ./build_specs.py ../data/game_raw/bcsv/${version}/ enumData130.json > ./specs_${version}.py

echo "Parsing ${version} BCSVs..."

python ./dump_all_bcsvs.py ../data/game_raw/bcsv/${version}/ ../data/game_parsed/ specs_${version}.py

cd ..

echo "Updating message repo..."

cd ./data/game_parsed/acnh-message-usen/
git pull origin master || true
cd ../../../

echo "Dumping new item table..."

python ./auto-gen.py --update ${version}

echo "Done!"