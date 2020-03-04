#!/bin/bash
function banner {
    echo "###"
    echo "### $1"
    echo "###"
}

ENV=$1
OUT_FDR=$2
SOURCE=$3

mkdir -p $OUT_FDR

banner "Job arguments:"
echo "ENV: $ENV"
echo "OUTPUT FOLDER: $OUT_FDR"
echo "DATA SOURCE: $SOURCE"

banner "Data Extraction"
python $ENV/data_prep.py --output_folder $OUT_FDR

banner "Data Exploration"
python $ENV/data_exploration.py --output_folder $OUT_FDR

banner "Complete!"
echo "* Results in: $OUT_FDR" 
