#!/bin/bash
# Script for run the trackeddy algorithm in multiple cores.

# dataorigin should be 'model' or 'satellite'

dataorigin=$1
files=$2
rundir=$3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/analysis_trackeddy/"

if [ "$dataorigin" == "model" ] || [ "$dataorigin" == "satellite" ];
then
  for i in ${files[@]};
  do
    echo "/g/data3/hh5/public/apps/miniconda3/envs/analysis3/bin/python ${cdir}trackeddy_$dataorigin.py $i" >> $cdir$rundir/config.$((i-timeinit))
    echo "Running at $((i-timeinit)).  File: $cdir$rundir/config.$((i-timeinit))"
    pbsdsh -v -n $((i-timeinit))*2  -- bash $cdir$rundir/config.$((i-timeinit)) > $cdir$rundir/nohup.$((i-timeinit)) &
  done
  wait
else
  echo "First argument (dataorigin) should be 'model' or 'satellite'"
fi


