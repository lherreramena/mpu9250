#!/bin/bash

set -x
set -e

FIND_PATH=$(find ~/ -name pythonEnv)

for folder in $FIND_PATH
do
    if [ -f $folder/bin/activate ]; then
        PYTHONENV_PATH=$folder
        break
done 

source $PYTHONENV_PATH/bin/activate

#source /home/lh/spd/spw/Python/pythonEnv/bin/activate
OUTPUT_FILE=test_acel.log
echo -e "Starting ..." > $OUTPUT_FILE
tail -f $OUTPUT_FILE

nohup python test_acel.py > $OUTPUT_FILE


