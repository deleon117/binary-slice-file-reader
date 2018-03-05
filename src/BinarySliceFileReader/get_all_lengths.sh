#!/bin/bash

if [ ! -d $1 ]; then
  echo "Directory does not exist!"
  echo "  $1"
  exit 1
fi

lengthFileName="`date -Ins`.lengths"
summFileName="`date -Ins`.summ"

echo "Avg.,Dev.,Max,Min,Med" >> $lengthFileName
for F in $1/*.bin;
do
  echo $F
  # Get summary file
  dotnet run $F $summFileName
  python contour_distance.py $summFileName >> $lengthFileName
  rm $summFileName
done
