#!/bin/sh

set -e

function banner {
    echo "###"
    echo "### $1"
    echo "###"
}

ENV="$(dirname "$(realpath "$0")")" # current directory
OUT_FDR="${1:-/tmp/data/}"
SOURCE="${SOURCE:-github}"

mkdir -p $OUT_FDR

banner "Job arguments:"
echo "ENV: $ENV"
echo "OUTPUT FOLDER: $OUT_FDR"
echo "SOURCE: $SOURCE"

banner "Data Extraction"
python $ENV/data_prep.py --output_folder $OUT_FDR

banner "Data Exploration"
python $ENV/data_exploration.py --output_folder $OUT_FDR

banner "Complete!"
echo "* Results in: $OUT_FDR"
