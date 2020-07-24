#!/bin/bash
#
# You can use this shell script to generate the ./output/results.csv file
# Note that this bash script assumes you are currently inside the top level directory
# and it assumes you have a file named complaints.csv located inside ./input 

python3.7 ./src/consumer_complaints.py ./input/complaints.csv ./output/results.csv
