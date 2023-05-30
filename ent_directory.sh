#!/bin/bash

# This script runs the 'ent' program on every file in a directory and outputs the results to a csv file

# Check if the user has provided a directory
if [ $# -ne 1 ]; then
	echo "Usage: $0 <directory>"
	exit 1
fi

dir_path="$1"
# Check if the directory exists
if [ ! -d "$dir_path" ]; then
	echo "Error: $dir_path is not a directory"
	exit 1
fi

#default output file
output_file="ent_output.csv"

# Write the CSV header to the output file
echo "Filename,Bytes,Entropy,Chi-square,Mean,Monte-Carlo-Pi,Serial-Correlation" > "$output_file"
# Run 'ent' on every file in the directory
for file_path in "$dir_path"/*; do
	file_name=$(basename "$file_path")
	# let's get the second line of the output and replace the first column with the filename
	output=$(ent -t "$file_path" | awk "NR==2" | awk -F',' -v name="$file_name" '{OFS=","; $1=name; print}')
	echo $output >> "$output_file"
done