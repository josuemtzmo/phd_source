#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'
module load conda/analysis3
dataorigin=$1
timeinit=$2
timeend=$3
logdir=$4

echo $logdir

if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  for i in `seq $timeinit $timeend`;
  do
    nohup python trackeddy_$dataorigin.py $i > "${logdir}${dataorigin}_nohup${i}.txt" &
  done
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi


