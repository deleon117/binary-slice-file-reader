#!/bin/bash

if [ ! -d $1 ]; then
  echo "Directory does not exist!"
  echo "  $1"
  exit 1
fi

numFills=0
numContours=0
summFileName="`date -Ins`.summ"

for F in $1/*.bin;
do
  echo $F
  # Get summary file
  dotnet run $F $summFileName
  # Count fill and contours scans in summary file
  out="`python count_scans_contours.py $summFileName`"
  # Sum up totals
  fills="`echo $out | cut -d ' ' -f 4`"
  contours="`echo $out | cut -d ' ' -f 8`"
  numFills=$((numFills + fills))
  numContours=$((numContours + contours))
  rm $summFileName
  echo "Fills: $fills Contours: $contours PrefixFills: $numFills  PrefixContours: $numContours"
done

echo "Number of fill scans:     $numFills"
echo "Number of contour scans:  $numContours"
