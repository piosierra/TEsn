#!/bin/bash

# Creates a single file out of the exits of cram_explorer.py adding a 
# column for the sample name.

# $1 is the directory with the samples directories
# $2 is the name of the exit file (created right below $1)

# missing: removal of merge folder


if [ ! -d $1 ]; then
  echo "Merge error: $1 does not exist"
  exit 1
fi

cd $1
mkdir -p "../merge"

for d in */ ; do
    cd $d
    echo "$d"
    for f in *; do
        sed -i '1d' $f #removes header of each file. Needs to be ad later when they are read.
        cat * > "../../merge/"${d::-1}
    done    
    cd ..
done
cd ../merge
for f in *; do
    sed -i "s/$/\t$f/" $f

    done
pwd
ls
cat * > "../../"$2
