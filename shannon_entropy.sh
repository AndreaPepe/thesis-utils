#!/bin/bash

# function to compute Shannon entropy of a file
compute_entropy() {
    local file="$1"

    # Array for characters frequencies
    declare -a frequencies

    # Count the total number of chars in the file
    local total_chars=0

    # Read the file byte by byte and increase occurencies
    while LANG=C IFS= read -r -d '' -n1 char; do
        if [ "$char" == "" ]; then
            value=0
        else
            value=$(printf "%d" "'$char")
        fi
        ((frequencies[$value]++))
        ((total_chars=total_chars+1))
    done < "$file"

    # Compute entropy
    local entropy=0

    for char in "${!frequencies[@]}"; do
        local count=${frequencies[$char]}
        local probability=$(awk "BEGIN {printf \"%.10f\", $count / $total_chars}")
        local log_probability=$(awk "BEGIN {printf \"%.10f\", log($probability)/log(2)}")
        local product=$(awk "BEGIN {printf \"%.10f\", $probability * $log_probability}")
        entropy=$(awk "BEGIN {printf \"%.10f\", $entropy - $product}")
    done

    echo "Entropia di Shannon del file '$file': $entropy"
}

# Check passed argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

# Check file existance
if [ ! -f "$1" ]; then
    echo "'$1' does not exist."
    exit 1
fi

# Compute shannon entropy
compute_entropy "$1"
