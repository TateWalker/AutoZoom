#!/bin/bash

open $1
y=$(($2*60))
sleep $y
x=$(pgrep zoom)
kill $x
echo "finished"