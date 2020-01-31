#!/bin/bash

function banner {
    echo "###"
    echo "### $1"
    echo "###"
}

banner "Data Extraction "
python ./src/data_prep.py

banner "Data Exploration "
python ./src/data_exploration.py

banner "Complete!"
echo "* Results in:   ./reports"
