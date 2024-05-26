#!/bin/bash

set -x
set -e

source /home/lh/spd/spw/Python/pythonEnv/bin/activate

nohup python test.py &

tail -f nohup.out

