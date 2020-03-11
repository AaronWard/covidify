#!/bin/bash
function banner {
    echo "###"
    echo "### $1"
    echo "###"
}

ENV=$1
OUT_FDR=$2
SOURCE=$3
COUNTRY=$4

set -e

mkdir -p $OUT_FDR

banner "Job arguments:"
echo "ENV: $ENV"
echo "OUTPUT FOLDER: $OUT_FDR"
echo "DATA SOURCE: $SOURCE"
echo "COUNTRIES: $COUNTRY"

banner "Data Extraction"
python $ENV/data_prep.py --output_folder $OUT_FDR --source $SOURCE --country $COUNTRY

banner "Data Exploration"
python $ENV/data_exploration.py --output_folder $OUT_FDR --country $COUNTRY

banner "Complete!"
echo "* Results in: $OUT_FDR" 
