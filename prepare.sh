#!/bin/bash

# step 1: generating dirty data
python3 generate_dirty_data.py

# step 2: cleaning dirty data
# remove comment lines, empty lines, and empty commas; extract essential columns 
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | sed -e 's/, ,/,/g' | cut -d ',' -f1,2,4,5,6 > ms_data.csv

# step 3: creating insurance file
echo -e "insurance_type\nBronze\nSilver\nGold" > insurance.lst

# step 4: summarizing processed data
rows=$(tail -n +2 ms_data.csv | wc -l) # ignore header
echo "Total number of visits: $rows"

echo "First 5 records:"
head -n 6 ms_data.csv