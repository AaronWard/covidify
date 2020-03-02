#!/bin/bash
function banner {
    echo "###"
    echo "### $1"
    echo "###"
}

ENV=$1

banner "Data Extraction "
python $ENV/data_prep.py

banner "Data Exploration "
python $ENV/data_exploration.py

banner "Complete!"
echo "* Results in:   Desktop/reports"
