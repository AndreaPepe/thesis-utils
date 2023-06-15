#!/usr/bin/bash

if [ $# -eq 0 ]
    then
        echo "No argument supplied"
        exit 1
fi

file="$1"
filename=$(basename $file)
out="${filename}.csv"

# write csv header
echo "elapsed,user,system" > $out

for i in {1..10}
do
    # /usr/bin/time uses the stderr as output channel
    /usr/bin/time -f "%e,%U,%S" $file 2>> $out
    echo "$i: done"
    sleep 10
done